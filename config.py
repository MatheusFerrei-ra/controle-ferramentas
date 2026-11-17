import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-desenvolvimento")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///controle_ferramentas.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False