from pydantic import BaseModel
from typing import List
from uuid import uuid4

from project.schemas.pokemon_in import PokemonIn


class Pokemon(BaseModel):
    id: str
    pokedex_number: int
    name: str
    types: List[str]

    @classmethod
    def from_pokemon_in(cls, pokemon_in: PokemonIn):
        """Create  class from pokemon in"""
        id = str(uuid4())
        pokedex_number = pokemon_in.pokedex_number
        name = pokemon_in.name
        types = pokemon_in.types
        return cls(id=id, pokedex_number=pokedex_number, name=name, types=types)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

