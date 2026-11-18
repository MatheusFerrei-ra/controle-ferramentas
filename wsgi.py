
from run import app, criar_dados_iniciais

with app.app_context():
    criar_dados_iniciais()
