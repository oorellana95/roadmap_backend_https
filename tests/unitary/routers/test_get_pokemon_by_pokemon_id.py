from fastapi.testclient import TestClient

from project.main import app, repository_dependency
from tests.unitary.routers.support.mock_pokemons_repository import override_pokemons_repository

client = TestClient(app)


app.dependency_overrides[repository_dependency] = override_pokemons_repository


def test_given_pokemon_when_get_pokemon_by_id_then_return_pokemon():
    response = client.get("/pokemons/f83b9c14-e003-4362-b6bf-962995df9b02")
    assert response.status_code == 200
    assert response.json() == {'id': 'f83b9c14-e003-4362-b6bf-962995df9b02',
                               'life_percent': 100.0,
                               'name': 'Bulbasaur',
                               'pokedex_number': 1,
                               'types': ['poison', 'plant']}


def test_given_pokemon_when_get_pokemon_by_fake_id_then_return_error():
    response = client.get("/pokemons/random_id")
    assert response.status_code == 422
    assert response.json() == {'code': 'ERROR.RESPONSE',
                               'message': 'Failed to execute method GET: '
                                          'http://testserver/pokemons/random_id. Pokemon with pokemon id '
                                          'random_id not found.'}
