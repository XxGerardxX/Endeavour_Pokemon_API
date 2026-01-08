import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
import uvicorn
from google import genai
from google.genai import types



load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

app = FastAPI()

chat_sessions ={}
cached_tools = None

class ChatRequest(BaseModel):
    message: str
    thread_id: str = None


def get_gemini_tools(mcp_tools):
    """Gets the necessary tools for information gathering of pokemon and berry entities"""
    list_of_blueprints = []

    for tool in mcp_tools:
        paper = types.FunctionDeclaration(
            name=tool.name,
            description=tool.description,
            parameters=tool.inputSchema
        )
        list_of_blueprints.append(paper)

    tool_folder = types.Tool(function_declarations=list_of_blueprints)
    final_toolbox = [tool_folder]
    return final_toolbox


@app.post("/chat")
async def test_handshake(request: ChatRequest):
    """Connects to the client and creates a chat session"""
    server_url = "http://localhost:8000/mcp"


    thread_id = request.thread_id or str(uuid.uuid4())
    if thread_id not in chat_sessions:
        chat_sessions[thread_id] = []

    history = chat_sessions[thread_id]
    history.append({"role": "user", "parts": [{"text": request.message}]})


    async with (streamable_http_client(url=server_url) as (read, write,_)):
        async with ClientSession(read,write) as session:
            await session.initialize()

            global cached_tools

            system_instructions = ["You are a helpful assistant. You have access to a Pokemon database. "
                                   "If the user asks about anything, use your tools to try to get the facts. "
                                   "If the user asks about anything else (like programming or general jokes), answer normally using your own knowledge."]


            if cached_tools is None:
                print("Fetching tools")
                mcp_resp = await session.list_tools()
                cached_tools = get_gemini_tools(mcp_resp.tools)
            else:
                print("DEBUG: Already have tools. Skipping sequential wait.")



            ## use or gemini-2.5-flash-lite or gemini-2.5-flash,
            response = client.models.generate_content(
                model = "gemini-2.5-flash",
                contents = history,
                config=types.GenerateContentConfig(tools=cached_tools, system_instruction = system_instructions)

            )


            ai_thought = response.candidates[0].content.parts[0]
            if ai_thought.function_call:

                call = ai_thought.function_call
                tool_result = await session.call_tool(call.name, call.args)
                data = tool_result.content[0].text
                history.append(response.candidates[0].content)
                history.append({
                    "role": "tool",
                    "parts": [{"function_response": {"name": call.name, "response": {"result": data}}}]
                })

                final_talk = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=history
                )
                return {"gemini_says": final_talk.text}

            else:
                ai_final_text = response.text
                history.append({"role": "model", "parts": [{"text": ai_final_text}]})
                return {"gemini_says": response.text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

