
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from app import db
from app.models import Ferramenta, Colaborador, Movimentacao

main = Blueprint("main", __name__)


@main.route("/")
def inicio():
    total = Ferramenta.query.count()
    disponiveis = Ferramenta.query.filter_by(disponivel=True).count()
    emprestadas = Ferramenta.query.filter_by(disponivel=False).count()

    return render_template(
        "base.html",
        total=total,
        disponiveis=disponiveis,
        emprestadas=emprestadas
    )


@main.route("/ferramentas")
def ferramentas():
    busca = request.args.get("busca", "").strip()

    consulta = Ferramenta.query

    if busca:
        consulta = consulta.filter(
            or_(
                Ferramenta.patrimonio.ilike(f"%{busca}%"),
                Ferramenta.descricao.ilike(f"%{busca}%")
            )
        )

    lista = consulta.order_by(Ferramenta.descricao).all()

    return render_template(
        "ferramentas.html",
        ferramentas=lista,
        busca=busca
    )


@main.route("/movimentacoes", methods=["GET", "POST"])
def movimentacoes():

    if request.method == "POST":
        try:
            tipo = request.form.get("tipo", "").strip().upper()

            ferramenta_id = int(request.form.get("ferramenta_id", ""))
            colaborador_id = int(request.form.get("colaborador_id", ""))

            area_destino = request.form.get(
                "area_destino", ""
            ).strip()

            local_destino = request.form.get(
                "local_destino", ""
            ).strip()

        except (ValueError, TypeError):
            flash("Informe dados válidos para a movimentação.", "danger")
            return redirect(url_for("main.movimentacoes"))

        try:
            ferramenta = db.session.get(Ferramenta, ferramenta_id)
            colaborador = db.session.get(Colaborador, colaborador_id)

            if not ferramenta or not colaborador or not colaborador.ativo:
                flash("Ferramenta ou colaborador inválido.", "danger")
                return redirect(url_for("main.movimentacoes"))

            if tipo == "RETIRADA":

                if not ferramenta.disponivel:
                    flash("Esta ferramenta já está emprestada.", "danger")
                    return redirect(url_for("main.movimentacoes"))

                if not area_destino or not local_destino:
                    flash("Informe a área e o local de destino.", "danger")
                    return redirect(url_for("main.movimentacoes"))

                ferramenta.disponivel = False

            elif tipo == "DEVOLUCAO":

                if ferramenta.disponivel:
                    flash("Esta ferramenta não está emprestada.", "danger")
                    return redirect(url_for("main.movimentacoes"))

                ultima_movimentacao = Movimentacao.query.filter_by(
                    ferramenta_id=ferramenta.id
                ).order_by(
                    Movimentacao.data_movimentacao.desc(),
                    Movimentacao.id.desc()
                ).first()

                if (
                    not ultima_movimentacao
                    or ultima_movimentacao.tipo != "RETIRADA"
                    or ultima_movimentacao.colaborador_id != colaborador.id
                ):
                    flash(
                        "Não foi encontrada uma retirada ativa para este colaborador.",
                        "danger"
                    )
                    return redirect(url_for("main.movimentacoes"))

                ferramenta.disponivel = True
                area_destino = ferramenta.area
                local_destino = ferramenta.local

            else:
                flash("Tipo de movimentação inválido.", "danger")
                return redirect(url_for("main.movimentacoes"))

            movimentacao = Movimentacao(
                ferramenta_id=ferramenta.id,
                colaborador_id=colaborador.id,
                tipo=tipo,
                area_destino=area_destino,
                local_destino=local_destino
            )

            db.session.add(movimentacao)
            db.session.commit()

            flash("Movimentação registrada com sucesso!", "success")

        except Exception:
            db.session.rollback()
            flash(
                "Não foi possível registrar a movimentação. Tente novamente.",
                "danger"
            )

        return redirect(url_for("main.movimentacoes"))

    ferramentas = Ferramenta.query.order_by(
        Ferramenta.descricao
    ).all()

    colaboradores = Colaborador.query.filter_by(
        ativo=True
    ).order_by(Colaborador.nome).all()

    historico = Movimentacao.query.order_by(
        Movimentacao.data_movimentacao.desc(),
        Movimentacao.id.desc()
    ).all()

    return render_template(
        "movimentacoes.html",
        ferramentas=ferramentas,
        colaboradores=colaboradores,
        historico=historico
    )
