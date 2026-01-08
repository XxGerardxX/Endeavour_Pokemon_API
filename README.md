
<h1>⭐ The MCP Server ⭐</h1>

*   **MCP Server:** A FastAPI-based server that exposes PokeAPI data as standardized MCP tools.
*   **MCP Client:** A FastAPI service running that coordinates between the user, the Google Gemini LLM, and the MCP tools.
*   **PokeRepository:** A central data access layer using `aiohttp` with persistent session management to ensure asynchronous data retrieval.
*   **Models:** Python Dataclass storage for Pokémon character stats, abilities, moves, and Berry data.

.  **Clone the repository:**
    ```bash
    git clone https://github.com/XxGerardxX/Endeavour_Pokemon_API.git
    cd Endeavour_Pokemon_API
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables:**
    - Create a file named `.env` in the root directory.
    - Add your Gemini API key:
      ```text
      GEMINI_API_KEY=your_actual_key_here
      ```


Start both the MCP server and the MCP client. From there go to http://localhost:8001/docs#/ and fill in the text in the message area.
