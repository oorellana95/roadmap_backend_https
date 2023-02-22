from enum import Enum

from project.repositories.pokemons_repository_json_implementation import PokemonsRepositoryJsonImplementation


class PokemonsRepositoryImplementation(Enum):
    JSON = "json"

    @staticmethod
    def dictionary(role):
        """Given the implementation value returns the implementation object."""
        dictionary = {
            PokemonsRepositoryImplementation.JSON.value: PokemonsRepositoryJsonImplementation
        }
        return dictionary.get(role)
