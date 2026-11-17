
from app import db
from app.models import Ferramenta, Movimentacao


def test_pagina_inicial_abre(client):
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert b"Painel inicial" in resposta.data


def test_consulta_de_ferramentas(client):
    resposta = client.get("/ferramentas")

    assert resposta.status_code == 200
    assert b"PAT-TESTE-001" in resposta.data
    assert b"Furadeira de teste" in resposta.data


def test_registrar_retirada(client, app):
    resposta = client.post("/movimentacoes", data={
        "tipo": "RETIRADA",
        "ferramenta_id": "1",
        "colaborador_id": "1",
        "area_destino": "Manutenção",
        "local_destino": "Setor de campo"
    }, follow_redirects=True)

    assert resposta.status_code == 200

    with app.app_context():
        ferramenta = db.session.get(Ferramenta, 1)
        movimentacao = Movimentacao.query.filter_by(
            ferramenta_id=1,
            tipo="RETIRADA"
        ).first()

        assert ferramenta.disponivel is False
        assert movimentacao is not None


def test_impedir_retirada_duplicada(client, app):
    client.post("/movimentacoes", data={
        "tipo": "RETIRADA",
        "ferramenta_id": "1",
        "colaborador_id": "1",
        "area_destino": "Manutenção",
        "local_destino": "Setor de campo"
    })

    resposta = client.post("/movimentacoes", data={
        "tipo": "RETIRADA",
        "ferramenta_id": "1",
        "colaborador_id": "1",
        "area_destino": "Manutenção",
        "local_destino": "Setor de campo"
    }, follow_redirects=True)

    assert resposta.status_code == 200
    assert "já está emprestada".encode() in resposta.data


def test_registrar_devolucao(client, app):
    client.post("/movimentacoes", data={
        "tipo": "RETIRADA",
        "ferramenta_id": "1",
        "colaborador_id": "1",
        "area_destino": "Manutenção",
        "local_destino": "Setor de campo"
    })

    resposta = client.post("/movimentacoes", data={
        "tipo": "DEVOLUCAO",
        "ferramenta_id": "1",
        "colaborador_id": "1"
    }, follow_redirects=True)

    assert resposta.status_code == 200

    with app.app_context():
        ferramenta = db.session.get(Ferramenta, 1)

        assert ferramenta.disponivel is True

        retiradas = Movimentacao.query.filter_by(
            ferramenta_id=1,
            tipo="RETIRADA"
        ).count()

        devolucoes = Movimentacao.query.filter_by(
            ferramenta_id=1,
            tipo="DEVOLUCAO"
        ).count()

        assert retiradas == 1
        assert devolucoes == 1
