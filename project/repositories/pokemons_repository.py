from typing import List

from project.config import get_settings
from project.schemas.pokemon import Pokemon
from project.serializers.pokemon_serializer import serializer_dict_to_pokemons, deserializer_pokemons_to_dict
from project.utils.File.file_json import read_json_file, add_to_json_file

# Import settings
settings = get_settings()


def get_pokemons() -> List[Pokemon]:
    """Return pokemons from the database."""
    return serializer_dict_to_pokemons(read_json_file(settings.LOCATION_POKEDEX))


def insert_pokemon(pokemon: Pokemon) -> bool:
    """Insert a pokemon to the database."""
    dict_pokemon = deserializer_pokemons_to_dict(pokemon)
    add_to_json_file(settings.LOCATION_POKEDEX, dict_pokemon)
    return True
