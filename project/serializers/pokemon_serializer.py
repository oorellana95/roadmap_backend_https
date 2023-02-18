from typing import List, Union

from project.schemas.pokemon import Pokemon


def serializer_dict_to_pokemons(pokemons_dict: Union[List[dict], dict]) -> Union[List[Pokemon], Pokemon]:
    """Serialize pokemon object from dict."""
    if isinstance(pokemons_dict, dict):
        return Pokemon(id=pokemons_dict.get('id'), pokedex_number=int(pokemons_dict.get('pokedex_number')),
                       name=pokemons_dict.get('name'), types=pokemons_dict.get('types'))
    return [Pokemon(id=pokemon_dict.get('id'), pokedex_number=int(pokemon_dict.get('pokedex_number')),
                    name=pokemon_dict.get('name'), types=pokemon_dict.get('types')) for pokemon_dict in pokemons_dict]


def deserializer_pokemons_to_dict(pokemons: Union[List[Pokemon], Pokemon]) -> Union[List[dict], dict]:
    """Deserialize pokemon object to dict."""
    if isinstance(pokemons, Pokemon):
        return {"id": pokemons.id, "pokedex_number": pokemons.pokedex_number, "name": pokemons.name,
                "types": pokemons.types}
    return [{"id": pokemon.id, "pokedex_number": pokemon.pokedex_number, "name": pokemon.name, "types": pokemon.types}
            for pokemon in pokemons]
