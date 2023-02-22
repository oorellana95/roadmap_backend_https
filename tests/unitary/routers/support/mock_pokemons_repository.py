from project.repositories.pokemons_repository import PokemonsRepository
from project.schemas.pokemon import Pokemon
from project.utils.general_functions import set_object_attributes_from_kwargs


async def override_pokemons_repository():
    return MockPokemonsRepository()


class MockPokemonsRepository(PokemonsRepository):
    def get_pokemons(self):
        return [
            Pokemon(id='f83b9c14-e003-4362-b6bf-962995df9b02', pokedex_number=1, name='Bulbasaur',
                    types=['poison', 'plant'],
                    life_percent=100.0),
            Pokemon(id='8b7c1fdf-bed5-4ff7-8a8d-5c74b10d4639', pokedex_number=4, name='Charmander', types=['fire'],
                    life_percent=100.0),
            Pokemon(id='b2b64ab8-003d-4398-859f-1bb075116e10', pokedex_number=7, name='Squirtle', types=['water'],
                    life_percent=100.0),
            Pokemon(id='6b600c1f-a02e-4ce3-9595-e7f52de7fe8b', pokedex_number=8, name='Wartortle', types=['water'],
                    life_percent=100.0)]

    def insert_pokemon(self, pokemon: Pokemon) -> bool:
        return True

    def upgrade_pokemon(self, pokemon_to_upgrade: Pokemon) -> Pokemon:
        return pokemon_to_upgrade

    def update_pokemon_fields(self, pokemon_id: str, **kwargs) -> Pokemon:
        pokemon_to_update = Pokemon(id=pokemon_id, pokedex_number=1, name='PokemonTest',
                                    types=['type_test1', 'type_test2'], life_percent=100.0)
        set_object_attributes_from_kwargs(object_to_update=pokemon_to_update, kwargs=kwargs)
        return pokemon_to_update

    def remove_pokemon(self, pokemon_id: str) -> bool:
        return True
