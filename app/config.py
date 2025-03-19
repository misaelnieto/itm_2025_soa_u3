"""Configuration module for the application settings.

This module defines the Settings class for managing application configuration
using environment variables and default values. You can also set custom values for each setting by creating a `.env` file in the project directory.

For more information about .env files, you can visit:
https://12factor.net/config

For the pydantic_settings documentation, you can visit:
https://docs.pydantic.dev/latest/usage/settings/
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings configuration class for the application.

    Attributes:
        model_config (SettingsConfigDict): Configuration for loading environment variables.
        verbose (bool): Flag to enable verbose logging.
        database_url (str): URL for the database connection.
        site_title (str): Title of the site.
        site_description (str): Description of the site.
        site_version (str): Version of the site.

    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    verbose: bool = True
    database_url: str = "sqlite:///./database.db"
    site_title: str = "Unidad 3 - Aplicaciones web con REST"
    site_summary: str = "Esta aplicación reune todos los proyectos de los estudiantes de la unidad 3"
    site_description: str = """
        En esta aplicación vamos a reunir todos los proyectos de los estudiantes.
        Cada estudiante tiene asignado un módulo donde deberá implementar su API REST de acuerdo a su
        proyecto asigado.
    """
    site_version: str = "0.1"


settings = Settings()
"""Import this object to get easy access to site-wide settings."""
