from flask import Blueprint
from flask import request
from flask import jsonify
from rest_script.helpers import token_required
from rest_script.models import db
from rest_script.models import User
from rest_script.models import Gunpla
from rest_script.models import gunpla_schema
from rest_script.models import gunplas_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 800}

@api.route('/gunplas', methods = ['POST'])
@token_required
def create_gunpla(current_user_token):
    name = request.json['name']
    description = request.json['description']
    customize_price = request.json['customize_price']
    creation_time = request.json['creation_time']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    gunpla = Gunpla(name, description, customize_price, creation_time, user_token = user_token)

    db.session.add(gunpla)
    db.session.commit()

    response = gunpla_schema.dump(gunpla)
    return jsonify(response)

@api.route('/gunplas', methods = ['GET'])
@token_required
def get_gunplas(current_user_token):
    owner = current_user_token.token
    gunplas = Gunpla.query.filter_by(user_token = owner).all()
    response = gunplas_schema.dump(gunplas)
    return jsonify(response)

@api.route('/gunplas/<id>', methods = ['GET']) 
@token_required
def get_gunpla(current_user_token, id):
    gunpla = Gunpla.query.get(id)
    response = gunpla_schema.dump(gunpla)
    return jsonify(response)

@api.route('/gunplas/<id>', methods = ['POST'])
@token_required
def update_gunpla(current_user_token, id):
    gunpla = Gunpla.query.get(id)
    print(gunpla)
    if gunpla:
        gunpla.name = request.json['name']
        gunpla.description = request.json['description']
        gunpla.customize_price = request.json['customize_price']
        gunpla.creation_time = request.json['creation_time']
        gunpla.user_token = current_user_token.token
        db.session.commit()

        response = gunpla_schema.dump(gunpla)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That drone does not exist!'})

@api.route('/gunplas/<id>', methods = ['DELETE'])
@token_required
def delete_gunpla(current_user_token, id):
    gunpla = Gunpla.query.get(id)
    if gunpla:
        db.session.delete(gunpla)
        db.session.commit()

        response = gunpla_schema.dump(gunpla)
        return jsonify(response)
    else:
        return jsonify({'Error': 'That drone does not exist!'})