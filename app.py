# API para controle de dieta diária, a Daily Diet API
from flask import Flask, jsonify, request
from database import db
from models.user import User
from datetime import datetime
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet-api'

db.init_app(app)

@app.route("/create", methods=['POST'])
def criar_refeicoes():
    data = request.get_json() # Acessa os dados enviados na requesição
    data_hora_str = data['data_hora']
    data_hora = datetime.strptime(data_hora_str, '%d-%m-%Y %H:%M:%S')
    try:
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
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Erro: Dados duplicados"}), 409
    except:
        return jsonify({"message": "Dados inválidos"}), 400
     
# Editar refeição, podendo alterar todos os dados [PUT]
@app.route("/editar/<int:id>", methods=['PUT'])
def editar_refeicoes(id):
    data = request.get_json()
    refeicao = User.query.get(id)
      
    if not refeicao:
        return jsonify({"error": "Refeição não encotrada"}), 404
    
    if 'nome' in data:
        refeicao.nome = data['nome']
    if 'data_hora' in data:
        data_hora_str = data['data_hora']
        refeicao.data_hora = datetime.strptime(data_hora_str, '%d-%m-%Y %H:%M:%S') # Convertendo padrão string para datetime
    if 'descricao' in data:
        refeicao.descricao = data['descricao']
    if 'dieta' in data:
        refeicao.dieta = data['dieta']
    
    nova_refeicao = User(
       nome=data['nome'],
       data_hora=data_hora,
       descricao=data['descricao'],
       dieta=data['dieta']
    )
    db.session.add(nova_refeicao)
    db.session.commit()
    
    return jsonify({"message": "Refeicão editada com sucesso!"})
#- apagar uma refeição (id) [DELETE]
@app.route("/delete/<int:id>", methods=['DELETE'])
def deletar_refeicoes(id):
    user = User.query.get(id)
    
    if user:
        db.session.delete(user) 
        db.session.commit()
        return jsonify({"message": f"A dieta do cliente id: ({id}) foi deletado com sucesso!"})

    return jsonify({"message": f"Cliente não encontrado."}), 404

if __name__ == '__main__':
    app.run(debug=True)