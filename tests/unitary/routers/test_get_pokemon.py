from fastapi.testclient import TestClient

from project.main import app, repository_dependency
from tests.unitary.routers.support.mock_pokemons_repository import override_pokemons_repository

client = TestClient(app)


app.dependency_overrides[repository_dependency] = override_pokemons_repository


def test_given_pokemon_when_get_pokemons_then_return_all():
    response = client.get("/pokemons")
    assert response.status_code == 200
    assert response.json() == [
        {'id': 'f83b9c14-e003-4362-b6bf-962995df9b02',
         'life_percent': 100.0,
         'name': 'Bulbasaur',
         'pokedex_number': 1,
         'types': [
             'poison',
             'plant'
         ]
         },
        {
            'id': '8b7c1fdf-bed5-4ff7-8a8d-5c74b10d4639',
            'life_percent': 100.0,
            'name': 'Charmander',
            'pokedex_number': 4,
            'types': [
                'fire'
            ]
        },
        {
            'id': 'b2b64ab8-003d-4398-859f-1bb075116e10',
            'life_percent': 100.0,
            'name': 'Squirtle',
            'pokedex_number': 7,
            'types': [
                'water'
            ]
        },
        {
            'id': '6b600c1f-a02e-4ce3-9595-e7f52de7fe8b',
            'life_percent': 100.0,
            'name': 'Wartortle',
            'pokedex_number': 8,
            'types': [
                'water'
            ]
        }
    ]


def test_given_pokemon_when_get_pokemons_of_type_water_then_return_water_pokemons():
    response = client.get("/pokemons/?types=water")
    assert response.status_code == 200
    assert response.json() == [{
        'id': 'b2b64ab8-003d-4398-859f-1bb075116e10',
        'life_percent': 100.0,
        'name': 'Squirtle',
        'pokedex_number': 7,
        'types': [
            'water'
        ]
    },
        {
            'id': '6b600c1f-a02e-4ce3-9595-e7f52de7fe8b',
            'life_percent': 100.0,
            'name': 'Wartortle',
            'pokedex_number': 8,
            'types': [
                'water'
            ]
        }
    ]
