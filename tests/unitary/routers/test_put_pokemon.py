from fastapi.testclient import TestClient

from project.main import app, repository_dependency
from tests.unitary.routers.support.mock_pokemons_repository import MockPokemonsRepository

client = TestClient(app)


async def override_dependency():
    return MockPokemonsRepository()


app.dependency_overrides[repository_dependency] = override_dependency


def test_given_pokemon_when_put_pokemon_then_return_pokemon_inserted():
    inserted_pokemon_json = {'id': '8093c4c8-08af-4ee8-8741-5ab5e76f7b3d',
                             'life_percent': 100.0,
                             'name': 'InsertedPokemonFromPut',
                             'pokedex_number': 100,
                             'types': ['random']}
    response = client.put("/pokemons", json=inserted_pokemon_json)
    assert response.status_code == 201
    assert response.json() == inserted_pokemon_json


def test_given_pokemon_with_fake_id_when_put_pokemon_then_return_error():
    inserted_pokemon_json = {'id': 'fake',
                             'life_percent': 100.0,
                             'name': 'InsertedPokemonFromPut',
                             'pokedex_number': 100,
                             'types': ['random']}
    response = client.put("/pokemons", json=inserted_pokemon_json)
    assert response.status_code == 422
    assert response.json() == {'code': 'ERROR.VALIDATION',
                               'message': 'Failed to execute method PUT: http://testserver/pokemons. Pokemon '
                                          'invalid. Verify the id.'}
