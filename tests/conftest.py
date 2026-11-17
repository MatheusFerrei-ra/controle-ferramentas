
import pytest

from app import create_app, db
from app.models import Ferramenta, Colaborador


@pytest.fixture
def app(tmp_path):
    banco_teste = tmp_path / "teste.db"

    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "chave-teste",
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{banco_teste}",
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        ferramenta = Ferramenta(
            patrimonio="PAT-TESTE-001",
            descricao="Furadeira de teste",
            area="Manutenção",
            local="Almoxarifado",
            disponivel=True
        )

        colaborador = Colaborador(
            nome="João Teste",
            matricula="99901",
            area="Manutenção"
        )

        db.session.add_all([ferramenta, colaborador])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
