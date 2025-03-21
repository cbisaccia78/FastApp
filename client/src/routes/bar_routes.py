from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from src.database import db

from src.schemas.bar_schemas import BarCreate, BarRead, BarUpdate
from src.models import Bar

bar_bp = Blueprint('bar_bp', __name__)

@bar_bp.route('', methods=['GET'])
def get_bars():
    bars = Bar.query.all()
    bars = [BarRead.model_validate(bar).model_dump() for bar in bars]
    return jsonify([bar for bar in bars]), 200

@bar_bp.route('/<int:bar_id>', methods=['GET'])
def get_bar(bar_id):
    bar = db.session.get(Bar, bar_id)
    if not bar:
        return jsonify({'error': 'Bar not found'}), 404
    bar = BarRead.model_validate(bar).model_dump()
    return jsonify(bar), 200

@bar_bp.route('', methods=['POST'])
def create_bar():
    try:
        data = request.get_json()
        bar = BarCreate(**data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 422
    
    bar = Bar(name=bar.name)
    db.session.add(bar)
    db.session.commit()
    bar = BarRead.model_validate(bar).model_dump()
    return jsonify(bar), 201

@bar_bp.route('/<int:bar_id>', methods=['PUT'])
def update_bar(bar_id):
    bar = db.session.get(Bar, bar_id)
    if not bar:
        return jsonify({'error': 'Bar not found'}), 404
    
    try:
        data = request.get_json()
        bar_data = BarUpdate(**data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 422
    
    if bar_data.name:
        bar.name = bar_data.name
    
    if bar_data.description:
        bar.description = bar_data.description
    
    db.session.commit()
    bar = BarRead.model_validate(bar).model_dump()
    return jsonify(bar), 200

@bar_bp.route('/<int:bar_id>', methods=['DELETE'])
def delete_bar(bar_id):
    bar = db.session.get(Bar, bar_id)
    if not bar:
        return jsonify({'error': 'Bar not found'}), 404
    
    foos = bar.foos
    for foo in foos:
        db.session.delete(foo)
    
    db.session.delete(bar)
    db.session.commit()
    return jsonify({'message': 'Bar deleted'}), 200