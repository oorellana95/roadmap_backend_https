from fastapi.testclient import TestClient

from project.main import app, repository_dependency
from tests.unitary.routers.support.mock_pokemons_repository import MockPokemonsRepository

client = TestClient(app)


async def override_dependency():
    return MockPokemonsRepository()


app.dependency_overrides[repository_dependency] = override_dependency


def test_given_pokemon_id_and_life_percent_when_patch_pokemon_life_percent_then_return_pokemon_updated():
    response = client.patch("/pokemons/8093c4c8-08af-4ee8-8741-5ab5e76f7b3d", json={'life_percent': 30.0})
    assert response.status_code == 200
    assert response.json() == {'id': '8093c4c8-08af-4ee8-8741-5ab5e76f7b3d',
                               'life_percent': 30.0,
                               'name': 'PokemonTest',
                               'pokedex_number': 1,
                               'types': ['type_test1', 'type_test2']}


def test_given_pokemon_fake_id_when_patch_pokemon_life_percent_then_return_error():
    response = client.patch("/pokemons/fake", json={'life_percent': 30.0})
    assert response.status_code == 422
    assert response.json() == {'code': 'ERROR.RESPONSE',
                               'message': 'Failed to execute method PATCH: http://testserver/pokemons/fake. '
                                          'Pokemon with id fake not found.'}


def test_given_pokemon_id_but_no_life_percent_when_patch_pokemon_life_percent_then_return_error():
    response = client.patch("/pokemons/8093c4c8-08af-4ee8-8741-5ab5e76f7b3d", json={})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'life_percent'],
                                           'msg': 'field required',
                                           'type': 'value_error.missing'}]}
