from pydantic import BaseModel
from typing import List
from uuid import uuid4

from project.schemas.pokemon_in import PokemonIn


class Pokemon(BaseModel):
    id: str
    pokedex_number: int
    name: str
    types: List[str]
    life_percent: float

    @classmethod
    def from_pokemon_in(cls, pokemon_in: PokemonIn):
        """Create  class from pokemon in"""
        id = str(uuid4())
        pokedex_number = pokemon_in.pokedex_number
        name = pokemon_in.name
        types = pokemon_in.types
        life_percent = pokemon_in.life_percent
        return cls(id=id, pokedex_number=pokedex_number, name=name, types=types, life_percent=life_percent)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

