from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from src.database import db

from src.schemas.foo_schemas import FooCreate, FooRead, FooUpdate
from src.models import Foo


foo_bp = Blueprint('foo_bp', __name__)

@foo_bp.route('', methods=['GET'])
def get_foos():
    foos = Foo.query.all()
    foos = [FooRead.model_validate(foo).model_dump() for foo in foos]
    return jsonify([foo for foo in foos]), 200

@foo_bp.route('/<int:foo_id>', methods=['GET'])
def get_foo(foo_id):
    foo = db.session.get(Foo, foo_id)
    if not foo:
        return jsonify({'error': 'Foo not found'}), 404
    foo = FooRead.model_validate(foo).model_dump()
    return jsonify(foo), 200

@foo_bp.route('', methods=['POST'])
def create_foo():
    try:
        data = request.get_json()
        foo = FooCreate(**data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 422
    
    foo = Foo(name=foo.name)
    db.session.add(foo)
    db.session.commit()
    
    foo = FooRead.model_validate(foo).model_dump()

    foo['created_at'] = str(foo['created_at'])
    if 'updated_at' in foo:
        foo['updated_at'] = str(foo['updated_at'])

    return jsonify(foo), 201

@foo_bp.route('/<int:foo_id>', methods=['PUT'])
def update_foo(foo_id):
    foo = db.session.get(Foo, foo_id)
    if not foo:
        return jsonify({'error': 'Foo not found'}), 404
    
    try:
        data = request.get_json()
        foo_data = FooUpdate(**data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 422
    
    if foo_data.name:
        foo.name = foo_data.name
    
    if foo_data.description:
        foo.description = foo_data.description
    
    
    db.session.commit()
    foo = FooRead.model_validate(foo).model_dump()
    return jsonify(foo), 200

@foo_bp.route('/<int:foo_id>', methods=['DELETE'])
def delete_foo(foo_id):
    foo = db.session.get(Foo, foo_id)
    if not foo:
        return jsonify({'error': 'Foo not found'}), 404
    db.session.delete(foo)
    db.session.commit()
    return jsonify({'message': 'Foo deleted'}), 200