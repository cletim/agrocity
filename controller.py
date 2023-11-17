from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import text, select
from database.connection import db
from .model import cliente

bp = Blueprint("Cliente",__name__)

@bp.route("/Cliente/lista")
def lista():
    lista = db.session.scalars(select(cliente))

    #Função lambda cria funçõesde 1 linha só    
    # meida = lambda telefone,cpf,palestra: telefone*.3+cpf*.35+palestra*.35
    def media(telefone, cpf, palestra):
        return telefone*.3+cpf*.35+palestra*.35
    
    return render_template("Cliente/lista.html", lista=lista, media=media)

@bp.route("/Cliente/add", methods=("GET", "POST"))
def add ():
    erros = []
    

    if request.method=="POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone = float(request.form.get("telefone"))
        cpf = float(request.form.get("cpf"))
        palestra = float(request.form.get("palestra"))

        
        if not nome: erros.append("Nome é um campo obrigatório")
        if not email: erros.append("Email é um campo obrigatório")
        if not telefone or telefone <0 or telefone> 10: erros.append("Trabalho é um campo obrigatório ou valores não entre 0-10")
        if not cpf or cpf <0 or cpf> 10: erros.append("Prova 1 é um campo obrigatório ou valores não entre 0-10")
        if not palestra or palestra <0 or palestra> 10: erros.append("Prova 2 é um campo obrigatório ou valores não entre 0-10")

        if len(erros) == 0:
            # salva usuário no banco de dados
            cliente = cliente(**{"nome": nome, "email": email, "telefone": telefone
            , "cpf": cpf, "palestra": palestra })
            db.session.add(cliente)
            db.session.commit() # persiste no banco
            flash(f"Usuário {nome}, salvo com sucesso!")

            return redirect(url_for("cliente.edit", id=cliente.id))
    return render_template("comprar/form.html", erros=erros)


@bp.route("/Cliente/<int:id>/delete", methods=("GET", "POST"))
def delete(id):
    cliente=cliente.query.filter_by(id=id).first()

    if request.method == "POST" and request.form.get("apagar") == "sim":
        db.session.delete(cliente) # deleta o cliente
        db.session.commit()

        return redirect(url_for("cliente.lista"))

    return render_template("Cliente/delete.html", id=id, cliente=cliente)

@bp.route("/cliente/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    erros = []
    cliente = cliente.query.filter_by(id=id).first()

    if request.method=="POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone = float(request.form.get("telefone"))
        cpf = float(request.form.get("cpf"))
        palestra = float(request.form.get("palestra"))

        if not nome: erros.append("Nome é um campo obrigatório")
        if not email: erros.append("Email é um campo obrigatório")
        if not telefone or telefone <0 or telefone> 10: erros.append("Trabalho é um campo obrigatório ou valores não entre 0-10")
        if not cpf or cpf <0 or cpf> 10: erros.append("Prova 1 é um campo obrigatório ou valores não entre 0-10")
        if not palestra or palestra <0 or palestra> 10: erros.append("Prova 2 é um campo obrigatório ou valores não entre 0-10")

        if len(erros) == 0:
            # altera usuário no banco de dados
            cliente.nome = nome
            cliente.email = email
            cliente.telefone = telefone
            cliente.cpf = cpf
            cliente.palestra = palestra
            db.session.add(cliente)
            db.session.commit()

            flash(f"usuário {nome}, salvo com sucesso!")

            return redirect(url_for("cliente.edit", id=id))
    return render_template("Cliente/form.html", id=id, cliente=cliente, erros=erros)