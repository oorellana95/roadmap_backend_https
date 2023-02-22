from fastapi.testclient import TestClient

from project.main import app, repository_dependency
from tests.unitary.routers.support.mock_pokemons_repository import MockPokemonsRepository

client = TestClient(app)


async def override_dependency():
    return MockPokemonsRepository()


app.dependency_overrides[repository_dependency] = override_dependency


def test_given_pokemon_id_when_delete_pokemon_then_proceed():
    response = client.delete("/pokemons/8093c4c8-08af-4ee8-8741-5ab5e76f7b3d")
    assert response.status_code == 200
    assert response.json() == 'Pokemon with id 8093c4c8-08af-4ee8-8741-5ab5e76f7b3d has been removed'


def test_given_pokemon_with_fake_id_when_put_pokemon_then_return_error():
    response = client.delete("/pokemons/fake")
    assert response.status_code == 422
    assert response.json() == {'code': 'ERROR.VALIDATION',
                               'message': 'Failed to execute method DELETE: http://testserver/pokemons/fake. '
                                          'The id should be an UUID valid.'}
