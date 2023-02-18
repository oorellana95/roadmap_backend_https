"""PokemonFilter."""
from enum import Enum
from typing import List

from starlette.datastructures import QueryParams

from project.utils.query_params_func import query_param_to_list_str, query_param_to_list_int


class PokemonFilterQueryParams(str, Enum):
    POKEDEX_NUMBERS = 'pokedex_numbers',
    NAMES = 'names',
    TYPES = 'types'


class PokemonFilter:
    def __init__(self, pokedex_numbers: List[int] = None, names: List[str] = None, types: List[str] = None):
        self.pokedex_numbers = pokedex_numbers
        self.names = names
        self.types = types

    @classmethod
    def from_query_params(cls, query_params: QueryParams):
        """Create class from query params"""
        pokedex_numbers = query_param_to_list_int(query_param_key=PokemonFilterQueryParams.POKEDEX_NUMBERS,
                                                  query_param_value=query_params.get(
                                                      PokemonFilterQueryParams.POKEDEX_NUMBERS))
        names = query_param_to_list_str(query_param_value=query_params.get(PokemonFilterQueryParams.NAMES))
        types = query_param_to_list_str(query_param_value=query_params.get(PokemonFilterQueryParams.TYPES))

        if pokedex_numbers or names or types:
            return cls(pokedex_numbers, names, types)
        return None
