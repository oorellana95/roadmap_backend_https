from fastapi.testclient import TestClient

from project.main import app

client = TestClient(app)


def test_given_no_query_params_when_options_pokemons_then_return_headers():
    response = client.options("/pokemons")
    assert response.status_code == 200
    assert response.headers["Allow"] == "GET, POST, PUT, PATCH, DELETE"
    assert response.headers["Content-Type"] == "application/json"
    assert response.headers["Content-Language"] == "en-US"
    assert response.headers["Allowed-Path-Parameters"] == "[{'methods':['GET'], 'parameters': ['pokedex_number']}, " \
                                                          "{'methods':['PATCH', 'DELETE'], 'parameters': [" \
                                                          "'pokemon_id']}]"


def test_given_query_param_get_when_options_pokemons_then_return_specific_headers():
    response = client.options("/pokemons/?method=get")
    assert response.status_code == 200
    assert response.headers["Allow"] == "GET"
    assert response.headers["Allowed-Path-Parameters"] == "['pokedex_number']"


def test_given_query_param_delete_when_options_pokemons_then_return_specific_headers():
    response = client.options("/pokemons/?method=delete")
    assert response.status_code == 200
    assert response.headers["Allow"] == "DELETE"
    assert response.headers["Allowed-Path-Parameters"] == "['pokemon_id']"


def test_given_query_param_patch_when_options_pokemons_then_return_specific_headers():
    response = client.options("/pokemons/?method=patch")
    assert response.status_code == 200
    assert response.headers["Allow"] == "PATCH"
    assert response.headers["Allowed-Path-Parameters"] == "['pokemon_id']"
