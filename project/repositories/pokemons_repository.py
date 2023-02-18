from typing import List

from project.config import get_settings
from project.schemas.pokemon import Pokemon
from project.serializers.pokemon_serializer import serializer_dict_to_pokemons, deserializer_pokemons_to_dict
from project.utils.File.file_json import read_json_file, add_to_json_file, rewrite_json_file

# Import settings
settings = get_settings()


def get_pokemons() -> List[Pokemon]:
    """Return pokemons from the database."""
    return serializer_dict_to_pokemons(read_json_file(settings.LOCATION_POKEDEX))


def insert_pokemon(pokemon: Pokemon) -> bool:
    """Given a pokemon, it is inserted to the database."""
    add_to_json_file(settings.LOCATION_POKEDEX, deserializer_pokemons_to_dict(pokemon))
    return True


def upgrade_pokemon(pokemon_to_upgrade: Pokemon) -> bool:
    """Given a pokemon, upgrades it to the database."""
    is_new_pokemon = True
    pokemons = get_pokemons()
    for idx, pokemon in enumerate(pokemons):
        if pokemon.id == pokemon_to_upgrade.id:
            pokemons[idx] = pokemon_to_upgrade
            is_new_pokemon = False
            break
    if is_new_pokemon:
        insert_pokemon(pokemon_to_upgrade)
    else:
        rewrite_json_file(settings.LOCATION_POKEDEX, deserializer_pokemons_to_dict(pokemons))
    return True


def remove_pokemon(pokemon_id: str) -> bool:
    """Given a pokemon_id, deletes it from the database."""
    pokemons = get_pokemons()
    for pokemon in pokemons:
        if pokemon.id == pokemon_id:
            pokemons.remove(pokemon)
            rewrite_json_file(settings.LOCATION_POKEDEX, deserializer_pokemons_to_dict(pokemons))
            return True
    return False
