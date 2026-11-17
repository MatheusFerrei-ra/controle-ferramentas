
from app import create_app, db
from app.models import Ferramenta, Colaborador, Movimentacao

app = create_app()


def criar_dados_iniciais():
    # Cadastro das ferramentas
    if Ferramenta.query.count() == 0:
        ferramentas = [
            Ferramenta(
                patrimonio="PAT-00125",
                descricao="Furadeira Bosch",
                area="Manutenção",
                local="Almoxarifado",
                disponivel=True
            ),
            Ferramenta(
                patrimonio="PAT-00126",
                descricao="Parafusadeira Makita",
                area="Manutenção",
                local="Almoxarifado",
                disponivel=True
            ),
            Ferramenta(
                patrimonio="PAT-00127",
                descricao="Esmerilhadeira",
                area="Serviços de Campo",
                local="Equipe externa",
                disponivel=False
            ),
        ]

        db.session.add_all(ferramentas)
        db.session.flush()

    # Cadastro dos colaboradores
    if Colaborador.query.count() == 0:
        colaboradores = [
            Colaborador(
                nome="João da Silva",
                matricula="00145",
                area="Manutenção"
            ),
            Colaborador(
                nome="Carlos Souza",
                matricula="00146",
                area="Serviços de Campo"
            ),
        ]

        db.session.add_all(colaboradores)
        db.session.flush()

    # Registro da retirada inicial da PAT-00127
    ferramenta_teste = Ferramenta.query.filter_by(
        patrimonio="PAT-00127"
    ).first()

    colaborador_teste = Colaborador.query.filter_by(
        matricula="00146"
    ).first()

    if ferramenta_teste and colaborador_teste and not ferramenta_teste.disponivel:
        retirada_existente = Movimentacao.query.filter_by(
            ferramenta_id=ferramenta_teste.id,
            tipo="RETIRADA"
        ).first()

        if not retirada_existente:
            db.session.add(
                Movimentacao(
                    ferramenta_id=ferramenta_teste.id,
                    colaborador_id=colaborador_teste.id,
                    tipo="RETIRADA",
                    area_destino="Serviços de Campo",
                    local_destino="Equipe externa"
                )
            )

    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        criar_dados_iniciais()

    app.run(debug=True)
