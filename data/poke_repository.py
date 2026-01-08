import aiohttp
import asyncio
import json
from typing import Optional
from dataclasses import fields
from models.berry_dataclass import Berry,BerryFlavor
from models.pokemon_dataclass import Pokemon, PokeStats


#TODO: Give link to user when asking for the pokemon ogg or sprite..


class Poke_Repo:
    def __init__(self):
        self.standard_url = "https://pokeapi.co/api/v2"
        self._session = None

    async def get_session(self) -> aiohttp.ClientSession:
        """Loads a single, persistent session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def fetch_json_data(self, endpoint: str) -> Optional[dict]:
        """Fetches a JSON data from an endpoint."""
        session = await self.get_session()
        data_url = f"{self.standard_url}/{endpoint}/"
        async with session.get(data_url) as response:
            if response.status != 200:
                return None
            return await response.json()

    async def get_berry_info(self, berry_id: int) -> Berry:
        berry_data = await self.fetch_json_data(f"berry/{berry_id}")
        berry_flavor_values = {}
        used_flavors = []

        for field_data in fields(BerryFlavor):
            used_flavors.append(field_data.name)

        for item in berry_data["flavors"]:
            key = item["flavor"]["name"]
            value = item["potency"]
            # if a new flavor is added then it stays at the old ones so it doesnt trip up..?
            if key in used_flavors:
                berry_flavor_values[key] = value
        all_flavor_values = BerryFlavor(**berry_flavor_values)

        return Berry(id= berry_data["id"],
                     name = berry_data["name"],
                     growth_time = berry_data["growth_time"],
                     flavors = all_flavor_values)


    async def get_pokemon_info(self, name_or_id: str) -> Pokemon:

        poke_data = await self.fetch_json_data(f"pokemon/{str(name_or_id).lower().strip()}")
        weight_and_height_conversion = 10 #to converto to kg and meters

        name = poke_data["name"]
        weight = poke_data["weight"] / weight_and_height_conversion
        height = poke_data["height"] / weight_and_height_conversion
        poke_id = poke_data["id"]
        poke_base_experience = poke_data["base_experience"]

        poke_types = poke_data["types"]
        all_poke_types = []
        for i in poke_types:
            all_poke_types.append(i["type"]["name"])

        normal_abilities = []
        hidden_abilities = []
        for i in poke_data["abilities"]:
            if i["is_hidden"]:
                hidden_abilities.append(i["ability"]["name"])
            else:
                normal_abilities.append(i["ability"]["name"])

        poke_all_abilities = poke_data["moves"]
        all_natural_moves = {}
        all_non_natural_moves = {}

        for i in poke_all_abilities:
            details = i["version_group_details"][0]
            if details["move_learn_method"]["name"] == "level-up":
                # print(details["level_learned_at"])
                all_natural_moves[i["move"]["name"]] = details["level_learned_at"]
                # print(i["move"]["name"])
            else:
                all_non_natural_moves[i["move"]["name"]] = details["level_learned_at"]

        formatted_natural_moves = [f"{m_name} (Lv. {lv})" for m_name, lv in all_natural_moves.items()]

        dict_poke_stats = {}
        for i in poke_data["stats"]:
            dict_poke_stats[i["stat"]["name"]] = [i["base_stat"], i["effort"]]

        flat_params = {}

        for stat_key, vals in dict_poke_stats.items():
            clean_stat_name = stat_key.replace("-", "_")
            flat_params[clean_stat_name] = vals[0]
            flat_params[f"{clean_stat_name}_effort"] = vals[1]


        stats_box = PokeStats(**flat_params)

        # print(all_poke_types)
        # print(name,poke_id,weight,height,all_poke_types,normal_abilities,hidden_abilities,formatted_natural_moves,poke_base_experience)
        return Pokemon(
            name=name,
            id=poke_id,
            weight=weight,
            height=height,
            types=all_poke_types,
            abilities=normal_abilities,
            hidden_abilities=hidden_abilities,
            natural_moves=formatted_natural_moves,
            base_experience=poke_base_experience,
            stats=stats_box
        )







if __name__ == "__main__":
    test_url = "https://pokeapi.co/api/v2/pokemon/charizard"

    extracted_flavours = {}

    async def test_info():
        async with aiohttp.ClientSession() as session:
            test_url

            async with session.get(test_url) as response:
                test_data  = await response.json()



    asyncio.run(test_info())