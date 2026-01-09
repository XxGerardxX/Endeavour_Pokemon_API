from mcp.server.fastmcp import FastMCP
from data.poke_repository import Poke_Repo


mcp = FastMCP("Poke-API", json_response=True)
repo = Poke_Repo()

@mcp.tool()
async def get_berry_info(berry_id: int) -> str:
    """Gives information about a specific berry given their ID"""
    try:
        berry = await repo.get_berry_info(berry_id)
        return f"Found {berry.name} with id {berry.id} and growth time {berry.growth_time} and {berry.flavors}"

    except Exception as e:
        return f"An error occurred while looking for berry {berry_id}: {e}"

@mcp.tool()
async def get_pokemon_info(name_or_id: str) -> str:
    """ Retrieves full character data for a Pokémon.
    - name_or_id: Can be the Pokémon's name (e.g., 'pikachu')
      or their Pokedex ID number as a string (e.g., '3' or '25')."""
    try:
        p = await repo.get_pokemon_info(name_or_id)
        if not p:
            return f"Pokemon {name_or_id} not found."


        return (
            f"POKEMON: {p.name} (ID: {p.id})\n"
            f"Types: {', '.join(p.types)}\n"
            f"Stats: HP:{p.stats.hp}, ATK:{p.stats.attack}, DEF:{p.stats.defense}, "
            f"SP-ATK:{p.stats.special_attack}, SP-DEF:{p.stats.special_defense}, SPD:{p.stats.speed}\n"
            f"Abilities: {', '.join(p.abilities)} (Hidden: {', '.join(p.hidden_abilities)})\n"
            f"Natural Moves: {', '.join(p.natural_moves)}"
        )
    except Exception as e:
        return f"Error: {str(e)}"



if __name__ == "__main__":
    mcp.run(transport="streamable-http")
