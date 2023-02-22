from fastapi.testclient import TestClient

from project.main import app, repository_dependency
from project.schemas import pokemon
from tests.unitary.routers.support.mock_pokemons_repository import MockPokemonsRepository

client = TestClient(app)


async def override_dependency():
    return MockPokemonsRepository()


app.dependency_overrides[repository_dependency] = override_dependency


def test_given_pokemon_when_post_pokemon_then_return_pokemon_inserted(monkeypatch):
    monkeypatch.setattr(pokemon, "uuid4", lambda: "a89f1280-44e0-4081-ac23-406d3417ebcf")
    response = client.post("/pokemons", json={'life_percent': 100.0,
                                              'name': 'InsertedPokemonFromPost',
                                              'pokedex_number': 100,
                                              'types': ['random']})
    assert response.status_code == 201
    assert response.json() == {'id': "a89f1280-44e0-4081-ac23-406d3417ebcf",
                               'life_percent': 100.0,
                               'name': 'InsertedPokemonFromPost',
                               'pokedex_number': 100,
                               'types': ['random']}


def test_given_pokemon_with_missing_fields_when_post_pokemon_then_return_error():
    response = client.post("/pokemons", json={
        'name': 'InsertedPokemonFromPut',
        'pokedex_number': 100,
        'types': ['random']})
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'life_percent'],
                                           'msg': 'field required',
                                           'type': 'value_error.missing'}]}
