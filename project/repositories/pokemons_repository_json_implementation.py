from typing import List, Optional

from project.config import get_settings
from project.repositories.pokemons_repository import PokemonsRepository
from project.schemas.pokemon import Pokemon
from project.serializers.pokemon_serializer import serializer_dict_to_pokemons, deserializer_pokemons_to_dict
from project.utils.File.file_json import read_json_file, add_to_json_file, rewrite_json_file
from project.utils.general_functions import set_object_attributes_from_kwargs

# Import settings
settings = get_settings()


class PokemonsRepositoryJsonImplementation(PokemonsRepository):
    def get_pokemons(self) -> List[Pokemon]:
        """Return pokemons from the database."""
        return serializer_dict_to_pokemons(read_json_file(settings.LOCATION_POKEDEX))

    def insert_pokemon(self, pokemon: Pokemon) -> bool:
        """Given a pokemon, it is inserted to the database."""
        add_to_json_file(settings.LOCATION_POKEDEX, deserializer_pokemons_to_dict(pokemon))
        return True

    def upgrade_pokemon(self, pokemon_to_upgrade: Pokemon) -> Pokemon:
        """Given a pokemon, upgrades it to the database."""
        pokemons = self.get_pokemons()
        idx_pokemon = [idx for idx, pokemon in enumerate(pokemons) if pokemon.id == pokemon_to_upgrade.id]
        if len(idx_pokemon) == 1:
            pokemons[idx_pokemon[0]] = pokemon_to_upgrade
            rewrite_json_file(settings.LOCATION_POKEDEX, deserializer_pokemons_to_dict(pokemons))
        else:
            self.insert_pokemon(pokemon_to_upgrade)
        return pokemon_to_upgrade

    def update_pokemon_fields(self, pokemon_id: str, **kwargs) -> Optional[Pokemon]:
        """Given a pokemon, updates it to the database."""
        pokemons = self.get_pokemons()
        idx_pokemon = [idx for idx, pokemon in enumerate(pokemons) if pokemon.id == pokemon_id]
        if len(idx_pokemon) == 1:
            set_object_attributes_from_kwargs(object_to_update=pokemons[idx_pokemon[0]], kwargs=kwargs)
            rewrite_json_file(settings.LOCATION_POKEDEX, deserializer_pokemons_to_dict(pokemons))
            return pokemons[idx_pokemon[0]]
        return None

    def remove_pokemon(self, pokemon_id: str) -> bool:
        """Given a pokemon_id, deletes it from the database."""
        pokemons = self.get_pokemons()
        for pokemon in pokemons:
            if pokemon.id == pokemon_id:
                pokemons.remove(pokemon)
                rewrite_json_file(settings.LOCATION_POKEDEX, deserializer_pokemons_to_dict(pokemons))
                return True
        return False
