from abc import (ABC, abstractmethod)
from typing import List

from project.schemas.pokemon import Pokemon


class PokemonsRepository(ABC):
    @abstractmethod
    def get_pokemons(self) -> List[Pokemon]:
        raise NotImplementedError()

    @abstractmethod
    def insert_pokemon(self, pokemon: Pokemon) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def upgrade_pokemon(self, pokemon_to_upgrade: Pokemon) -> Pokemon:
        raise NotImplementedError()

    @abstractmethod
    def update_pokemon_fields(self, pokemon_id: str, **kwargs) -> Pokemon:
        raise NotImplementedError()

    @abstractmethod
    def remove_pokemon(self, pokemon_id: str) -> bool:
        raise NotImplementedError()
