from pydantic import BaseModel
from typing import List


class PokemonIn(BaseModel):
    pokedex_number: int
    name: str
    types: List[str]
    life_percent: float
