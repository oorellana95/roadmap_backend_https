from typing import Union

from fastapi import FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from project.config import get_settings
from project.exceptions.exception_handler import register_exceptions_handler
from project.exceptions.response_exception import NotFoundException
from project.repositories import pokemons_repository
from project.repositories.pokemons_repository import insert_pokemon
from project.schemas.pokedex import Pokedex
from project.schemas.pokemon import Pokemon
from project.schemas.pokemon_filter import PokemonFilter
from project.schemas.pokemon_in import PokemonIn
from project.serializers.pokemon_serializer import deserializer_pokemons_to_dict
from project.utils.File.file_json import read_json_file, rewrite_json_file, add_to_json_file

# Import settings
settings = get_settings()

# Create the app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.DOMAIN_FRONTEND],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register igs_classes handler
register_exceptions_handler(app)


@app.head("/")
async def health():
    pass


@app.options("/pokemons", status_code=200)
def options_pokemons(access_control_request_method: Union[str, None] = Header(default=None)):
    """The OPTIONS method describes the communication options for the target resource."""
    headers = {
        "Content-Language": "en-US",
        "Content-Type": "application/json",
        "Allowed-Path-Parameters": "[{'methods':['GET'], 'parameters': ['pokedex_number']}, "
                                   "{'methods':['PATCH', 'DELETE'], 'parameters': ['pokemon_id']}]"
    }
    if access_control_request_method is None:
        headers["Allow"] = "GET, POST, PUT, PATCH, DELETE"

    if is_allowed_http_crud_method(access_control_request_method):
        headers["Allow"] = access_control_request_method

    return JSONResponse(content=None, headers=headers)


def is_allowed_http_crud_method(method: str):
    if method == "GET" or method == "POST" or method == "PUT" or method == "PATCH" or method == "DELETE":
        return True
    return False


@app.get("/pokemons")
def read_pokemons(request: Request):
    """Retrieves the pokemons in the pokedex."""
    pokemon_filter = PokemonFilter.from_query_params(request.query_params)
    pokedex = Pokedex(pokemons=pokemons_repository.get_pokemons(), pokemon_filter=pokemon_filter)
    pokemons = pokedex.pokemons if pokemon_filter is None else pokedex.get_pokemons_using_filter()
    return JSONResponse(
        status_code=200,
        content=deserializer_pokemons_to_dict(pokemons)
    )


@app.get("/pokemons/{pokemon_id}")
def read_pokemon_by_pokemon_id(pokemon_id: str):
    """Retrieves the specific pokemon with the corresponding pokemon_id."""
    pokedex = Pokedex(pokemons=pokemons_repository.get_pokemons())
    pokemon = pokedex.get_pokemon_by_pokemon_id(pokemon_id)
    if pokemon:
        return JSONResponse(
            status_code=200,
            content=deserializer_pokemons_to_dict(pokemon)
        )
    raise NotFoundException(f"Pokemon with pokedex number {pokemon_id} not found.")


@app.post("/pokemons", status_code=201)
def post_pokemon(pokemon_in: PokemonIn):
    """The POST method submits a new entity to the specified resource, often causing a change in state or side effects
    on the server."""
    pokemon = Pokemon.from_pokemon_in(pokemon_in)
    insert_pokemon(pokemon)
    return JSONResponse(
        status_code=201,
        content=deserializer_pokemons_to_dict(pokemon)
    )


@app.put("/pokemons")
def put_pokemon(input_pokemon: Pokemon):
    """The PUT method replaces all current representations of the target resource with the request payload."""
    pokemons = read_json_file(settings.LOCATION_POKEDEX)
    for idx, pokemon in enumerate(pokemons):
        if pokemon.get('id') == input_pokemon.id:
            pokemons[idx] = input_pokemon.to_dict()
            rewrite_json_file(settings.LOCATION_POKEDEX, pokemons)
            return JSONResponse(
                status_code=200,
                content=input_pokemon
            )
    raise NotFoundException(f"Pokemon with id {input_pokemon.id} not found.")


@app.patch("/pokemons/{pokemon_id}", status_code=200)
def patch_pokemon(pokemon_id: int):
    """The PATCH method applies partial modifications to a resource."""
    return {"pokemon_id": pokemon_id}


@app.delete("/pokemons/{pokemon_id}", status_code=200)
def delete_pokemon(pokemon_id: str):
    """The PUT method replaces all current representations of the target resource with the request payload."""
    pokemons = read_json_file(settings.LOCATION_POKEDEX)
    for pokemon in pokemons:
        if pokemon.get('id') == pokemon_id:
            pokemons.remove(pokemon)
            rewrite_json_file(settings.LOCATION_POKEDEX, pokemons)
            return JSONResponse(
                status_code=200,
                content=f"Pokemon with id {pokemon_id} has been removed"
            )
    raise NotFoundException(f"Pokemon with id {pokemon_id} not found.")


@app.trace("/")
def trace_root():
    """The TRACE method performs a message loop-back test along the path to the target resource."""
    return {"Hello": "World"}
