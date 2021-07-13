from flask import Blueprint, request, jsonify, make_response
from api.schema.mapel import MapelSchema
from api.models import Mapel, Jurusan
from api import db
from flask_jwt_extended import jwt_required

mapel = Blueprint('mapel', __name__)

@mapel.route('/mapel', methods=['GET', 'POST'])
@jwt_required()
def get_post_jurusan():
    # GET ALL JURUSAN
    if request.method == "GET":
        all_jurusan = db.session.query(Mapel).join(Jurusan).all()
        schema = MapelSchema(many=True)
        result = schema.dump(all_jurusan)
        return make_response(jsonify({"jurusan": result}), 200)
    # POST JURUSAN
    elif request.method == "POST":
        params = request.form
        # Validate the form
        if not params.get('nama_mapel'):
            return make_response(jsonify({'error': 'Nama mapel diperlukan!'}), 400)
        if not params.get('id_jurusan'):
            return make_response(jsonify({'error': 'ID Jurusan diperlukan!'}), 400)
        # Query to the model
        schema = MapelSchema()
        mapel = schema.load(params)
        db.session.add(mapel)
        db.session.commit()
        # make JSON response
        result = schema.dump(mapel)
        return make_response(jsonify({'message': 'post success', 'data': result}), 201)

@mapel.route('/mapel/<id_mapel>', methods=["GET", "DELETE", "PUT"])
@jwt_required()
def mapel_by_id(id_mapel):
    # GET ONE MAPEL
    if request.method == "GET":
        get_mapel = db.session.query(Mapel).get(id_mapel)
        schema = MapelSchema()
        result = schema.dump(get_mapel)
        if not result:
            return make_response(jsonify({'error': 'data not found!'}), 404)
        return make_response(jsonify({'result': result}), 200)
    # UPDATE ONE MAPEL
    elif request.method == "PUT":
        params = request.form
        # if mapel doesn't exist, reject request
        get_mapel = db.session.query(Mapel).get(id_mapel)
        if get_mapel is None:
            return make_response(jsonify({'error': 'Mapel not found!'}), 404)
        # Update mapel based on params
        for p in params:
            setattr(get_mapel, p, request.form[p])
        db.session.commit()
        # Create JSON response
        schema = MapelSchema()
        result = schema.dump(get_mapel)
        return make_response(jsonify({'message': 'update successful', 'result': result}), 200)
    # DELETE ONE MAPEL
    if request.method == "DELETE":
        get_mapel = db.session.query(Mapel).get(id_mapel)
        db.session.delete(get_mapel)
        db.session.commit()
        return make_response(jsonify({'message': 'delete successful'}), 204)