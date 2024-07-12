# API para controle de dieta diária, a Daily Diet API
from flask import Flask, jsonify, request
from database import db
from models.user import User
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet-api'

db.init_app(app)

@app.route("/create", methods=['POST'])
def criar_refeicoes():
    data = request.get_json() # Acessa os dados enviados na requesição
    data_hora_str = data['data_hora']
    data_hora = datetime.strptime(data_hora_str, '%d-%m-%Y %H:%M:%S')
    
    
    nova_refeicao = User(
       nome=data['nome'],
       data_hora=data_hora,
       descricao=data['descricao'],
       dieta=data['dieta']
    )
    db.session.add(nova_refeicao)
    db.session.commit()
    return jsonify({"message": "Dieta cadastrada com sucesso!"})
if __name__ == '__main__':
    app.run(debug=True)