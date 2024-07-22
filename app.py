# API para controle de dieta diária, a Daily Diet API
from flask import Flask, jsonify, request
from database import db
from models.user import User, Refeicao
from datetime import datetime
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet-api'

db.init_app(app)

# Criar Usuário
@app.route("/create_user", methods=['POST'])
def criar_usuario():
    data = request.get_json()
    novo_usuario = User(nome=data['nome'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso!", "user_id": novo_usuario.id}), 201

@app.route("/create", methods=['POST'])
def criar_refeicoes(user_id):
    try:
        data = request.get_json() # Acessa os dados enviados na requesição
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        data_hora_str = data['data_hora']
        data_hora = datetime.strptime(data_hora_str, '%d-%m-%Y %H:%M:%S')
        
        nova_refeicao = Refeicao(
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
    refeicao = Refeicao.query.get(id)
      
    if not refeicao:
        return jsonify({"error": "Refeição não encotrada"}), 404
    
    if 'descricao' in data:
        refeicao.descricao = data['descricao']
    if 'data_hora' in data:
        data_hora_str = data['data_hora']
        refeicao.data_hora = datetime.strptime(data_hora_str, '%d-%m-%Y %H:%M:%S') # Convertendo padrão string para datetime
    if 'dieta' in data:
        refeicao.dieta = data['dieta']
    
    db.session.commit()
    
    return jsonify({"message": "Refeicão editada com sucesso!"})

# Buscar refeicões individuais
@app.route("/list/<int:id>", methods=['GET'])
def buscar_refeicao(id):
    refeicao = User.query.get(id)
    
    if not refeicao:
        return jsonify({"message": "Refeição não encontrada"}), 404
    
    refeicao_data = {
        "id": refeicao.id,
        "nome": refeicao.nome,
        "descricao": refeicao.descricao,
        "data_hora": refeicao.data_hora.strftime('%d-%m-%Y %H:%M:%S'),  # Converte datetime para string
        "dieta": refeicao.dieta,
        "user_id": refeicao.user_id
    }
    
    return jsonify(refeicao_data), 200

# Listar todas as refeições de um usuário
@app.route("/get_refeicoes/<int:user_id>", methods=['GET'])
def listar_refeicoes(user_id):
    user = User.query.get(user_id) 
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404   
    
    refeicoes = Refeicao.query.filter_by(user_id=user_id).all() 

    refeicoes_data = []
    for refeicao in refeicoes:
        refeicoes_data.append({
            "id": refeicao.id,
            "descricao": refeicao.descricao,
            "data_hora": refeicao.data_hora.strftime('%d-%m-%Y %H:%M:%S'),  # Converte datetime para string
            "dieta": refeicao.dieta,
            "user_id": refeicao.user_id
        })
        
    return jsonify(refeicoes_data)
# Apagar uma refeição (id) [DELETE]
@app.route("/delete/<int:id>", methods=['DELETE'])
def deletar_refeicao(id):
    try:
        refeicao = Refeicao.query.get(id)  
        if not refeicao:
            return jsonify({"error": "Refeição não encontrada"}), 404

        db.session.delete(refeicao)
        db.session.commit()

        return jsonify({"message": "Refeição apagada com sucesso!"}), 200   
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)