"""AppSettings config."""
from functools import lru_cache
from pydantic import BaseSettings

from project.repositories.pokemons_repository import PokemonsRepository


class AppSettings(BaseSettings):
    # General
    APP_NAME: str = "Roadmap Backend HTTP"

    # Cors Origins
    DOMAIN_FRONTEND: str = "http://localhost:8080"

    # Data
    LOCATION_POKEDEX: str = "data/pokedex.json"
    POKEMONS_REPOSITORY_IMPLEMENTATION: str = "json"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return AppSettings()
