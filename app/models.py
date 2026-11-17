
from datetime import datetime
from app import db


class Ferramenta(db.Model):
    __tablename__ = "ferramentas"

    id = db.Column(db.Integer, primary_key=True)
    patrimonio = db.Column(db.String(30), unique=True, nullable=False)
    descricao = db.Column(db.String(120), nullable=False)
    area = db.Column(db.String(80), nullable=False)
    local = db.Column(db.String(80), nullable=False)
    disponivel = db.Column(db.Boolean, default=True, nullable=False)
    observacao = db.Column(db.Text)

    movimentacoes = db.relationship(
        "Movimentacao",
        backref="ferramenta",
        lazy=True
    )


class Colaborador(db.Model):
    __tablename__ = "colaboradores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    matricula = db.Column(db.String(30), unique=True, nullable=False)
    area = db.Column(db.String(80), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    movimentacoes = db.relationship(
        "Movimentacao",
        backref="colaborador",
        lazy=True
    )


class Movimentacao(db.Model):
    __tablename__ = "movimentacoes"

    id = db.Column(db.Integer, primary_key=True)
    ferramenta_id = db.Column(
        db.Integer,
        db.ForeignKey("ferramentas.id"),
        nullable=False
    )
    colaborador_id = db.Column(
        db.Integer,
        db.ForeignKey("colaboradores.id"),
        nullable=False
    )
    tipo = db.Column(db.String(20), nullable=False)
    data_movimentacao = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )
    area_destino = db.Column(db.String(80))
    local_destino = db.Column(db.String(80))
