import click 
from flask import Flask, render_template, request, url_for, redirect, flash
from flask.cli import with_appcontext
from sqlalchemy import select
from database.connection import db
from model import Cliente


def create_app(): # cria uma função para definir o aplicativo
    app = Flask(__name__) # instancia o Flask
    app.secret_key = "abax"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://root:5e5i_123@localhost:3306/dataagrocity"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.cli.add_command(init_db_command)

    @app.route("/") # cria uma rota
    def index(): # função que gerencia rota
        return render_template("index.html") # combina o python com html
    
    @app.route("/ingressos")
    def ingressos():
        return render_template("ingressos.html")
    
    @app.route("/cronograma")
    def cronograma():
        return render_template("cronograma.html")
    
    
    @app.route("/local")
    def local():
        return render_template("local.html")
    
    @app.route("/contato")
    def contato():
        return render_template("contato.html")
    
    @app.route("/comprar", methods=("GET", "POST"))
    def comprar():

        erros=[]

        if request.method=="POST":
            nome = request.form.get("firstname")
            email = request.form.get("email")
            telefone = request.form.get("telefone")
            cpf = request.form.get("cpf")
            palestra = request.form.get("palestra")

            
            if not nome: erros.append("Nome é um campo obrigatório")
            if not email: erros.append("Email é um campo obrigatório")
            if not telefone: erros.append("Trabalho é um campo obrigatório ou valores não entre 0-10")
            if not cpf: erros.append("Prova 1 é um campo obrigatório ou valores não entre 0-10")
            if not palestra: erros.append("Prova 2 é um campo obrigatório ou valores não entre 0-10")

            if len(erros) == 0:
                # salva usuário no banco de dados
                cliente = Cliente(**{"nome": nome, "email": email, "telefone": telefone, "cpf": cpf, "palestra": palestra })
                db.session.add(cliente)
                db.session.commit() # persiste no banco
                flash(f"Usuário {nome}, salvo com sucesso!")

                return redirect(url_for("pagamento", id=cliente.idcliente))
        
        return render_template("comprar.html", erros=erros)

    @app.route("/pagamento")
    def pagamento():
        return render_template("pagamento.html")
    
    @app.route("/test")
    def test():
        lista = db.session.scalars(select(Cliente))
        return render_template("test.html", lista = lista) 
        
    
    # from usuarios.controller import bp
    # app.register_blueprint(bp)

    # from alunos.controller import bp
    # app.register_blueprint(bp)

    return app # retorna o app criado

    

def init_db():
    # db.drop_all()
    # db.create_all()
    # db.reflect()
    pass

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""

    init_db()
    click.echo("Initialized the database.")  
    
      
if __name__ == "__main__": # 'função principal' do python
    create_app().run(debug=True) # executa o flask na porta http://127.0.0.1:5000