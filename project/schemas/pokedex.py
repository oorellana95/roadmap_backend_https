from typing import List, Optional

from project.schemas.pokemon import Pokemon
from project.schemas.pokemon_filter import PokemonFilter


class Pokedex:
    pokemons: List[Pokemon]
    pokemon_filter: PokemonFilter

    def __init__(self, pokemons, pokemon_filter=None):
        self.pokemons = pokemons
        self.pokemon_filter = pokemon_filter

    def get_pokemon_by_id(self, id: str) -> Optional[Pokemon]:
        """Get registered pokemon in the pokedex by its id."""
        for pokemon in self.pokemons:
            if pokemon.id == id:
                return pokemon
        return None

    def get_pokemons_using_filter(self):
        filtered_pokemons = self.pokemons
        if self.pokemon_filter.pokedex_numbers is not None:
            filtered_pokemons = self._get_pokemons_by_pokedex_number(filtered_pokemons)
        if self.pokemon_filter.names is not None:
            filtered_pokemons = self._get_pokemons_by_name(filtered_pokemons)
        if self.pokemon_filter.types is not None:
            filtered_pokemons = self._get_pokemons_by_type(filtered_pokemons)
        return filtered_pokemons

    def _get_pokemons_by_pokedex_number(self, pokemons: Optional[List[Pokemon]] = None) -> List[Pokemon]:
        return [pokemon for pokemon in pokemons if pokemon.pokedex_number in self.pokemon_filter.pokedex_numbers]

    def _get_pokemons_by_name(self, pokemons: Optional[List[Pokemon]] = None) -> List[Pokemon]:
        return [pokemon for pokemon in pokemons if pokemon.name in self.pokemon_filter.names]

    def _get_pokemons_by_type(self, pokemons: Optional[List[Pokemon]] = None) -> List[Pokemon]:
        filtered_pokemons = []
        for pokemon_type in self.pokemon_filter.types:
            filtered_pokemons.extend([pokemon for pokemon in pokemons if pokemon_type in pokemon.types])
        filtered_pokemons = list(set(filtered_pokemons))
        filtered_pokemons.sort(key=lambda x: x.pokedex_number)
        return filtered_pokemons
