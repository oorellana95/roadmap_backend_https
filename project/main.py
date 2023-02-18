from typing import Union

from fastapi import FastAPI, Header, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from project.config import get_settings
from project.exceptions.exception_handler import register_exceptions_handler
from project.exceptions.response_exception import NotFoundException
from project.exceptions.validation_exception import InputValidationException
from project.repositories import pokemons_repository
from project.repositories.pokemons_repository import insert_pokemon, upgrade_pokemon, remove_pokemon, \
    update_pokemon_fields
from project.schemas.pokedex import Pokedex
from project.schemas.pokemon import Pokemon
from project.schemas.pokemon_filter import PokemonFilter
from project.schemas.pokemon_in import PokemonIn
from project.serializers.pokemon_serializer import deserializer_pokemons_to_dict
from project.utils.uuid_functions import is_valid_uuid

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
def get_pokemons(request: Request):
    """Retrieves the pokemons from the pokedex."""
    pokemon_filter = PokemonFilter.from_query_params(request.query_params)
    pokedex = Pokedex(pokemons=pokemons_repository.get_pokemons(), pokemon_filter=pokemon_filter)
    pokemons = pokedex.pokemons if pokemon_filter is None else pokedex.get_pokemons_using_filter()
    return JSONResponse(
        status_code=200,
        content=deserializer_pokemons_to_dict(pokemons)
    )


@app.get("/pokemons/{pokemon_id}")
def get_pokemon_by_pokemon_id(pokemon_id: str):
    """Retrieves a specific pokemon with the corresponding pokemon_id."""
    pokedex = Pokedex(pokemons=pokemons_repository.get_pokemons())
    pokemon = pokedex.get_pokemon_by_id(pokemon_id)
    if pokemon:
        return JSONResponse(
            status_code=200,
            content=deserializer_pokemons_to_dict(pokemon)
        )
    raise NotFoundException(f"Pokemon with pokedex number {pokemon_id} not found.")


@app.post("/pokemons", status_code=201)
def post_pokemon(pokemon_in: PokemonIn):
    """Submits a new pokemon to the specified resource."""
    pokemon = Pokemon.from_pokemon_in(pokemon_in)
    insert_pokemon(pokemon)
    return JSONResponse(
        status_code=201,
        content=deserializer_pokemons_to_dict(pokemon)
    )


@app.put("/pokemons")
def put_pokemon(input_pokemon: Pokemon):
    """Replaces or creates the pokemon with the request payload."""
    if is_valid_uuid(input_pokemon.id):
        upgraded_pokemon = upgrade_pokemon(input_pokemon)
        return JSONResponse(
            status_code=201,
            content=deserializer_pokemons_to_dict(upgraded_pokemon)
        )

    raise InputValidationException(f"Pokemon invalid. Verify the id.")


@app.patch("/pokemons/{pokemon_id}", status_code=200)
def patch_pokemon_life_percent(pokemon_id: str, life_percent: float = Body(..., embed=True)):
    """Updates the pokemons life_percent field."""
    kwargs = {"life_percent": life_percent}
    pokemon_updated = update_pokemon_fields(pokemon_id, **kwargs)
    if pokemon_updated:
        return JSONResponse(
            status_code=200,
            content=deserializer_pokemons_to_dict(pokemon_updated)
        )
    raise NotFoundException(f"Pokemon with id {pokemon_id} not found.")


@app.delete("/pokemons/{pokemon_id}", status_code=200)
def delete_pokemon(pokemon_id: str):
    """The DELETES method removes the target resource."""
    if is_valid_uuid(pokemon_id):
        is_deleted = remove_pokemon(pokemon_id)
        if is_deleted:
            return JSONResponse(
                status_code=200,
                content=f"Pokemon with id {pokemon_id} has been removed"
            )
        raise NotFoundException(f"Pokemon with id {pokemon_id} not found.")
    raise InputValidationException(f"The id should be an UUID valid.")


@app.trace("/")
def trace_root():
    """The TRACE method performs a message loop-back test along the path to the target resource."""
    return {"Hello": "World"}
