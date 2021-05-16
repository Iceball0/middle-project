from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.specialties import Specialties


class SpecialtiesResource(Resource):
    def get(self, specialty_id):
        abort_if_specialty_not_found(specialty_id)
        db_sess = db_session.create_session()
        specialty = db_sess.query(Specialties).get(specialty_id)
        return jsonify(
            {
                'specialty': specialty.to_dict(only=(
                    'name', 'code', 'universities.budgetary_places', 'universities.universities.name',
                    'universities.universities.description',
                    'universities.universities.city', 'universities.universities.image',
                    'universities.universities.placeInRussianTop'))
            }
        )


class SpecialtiesListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        specialty = db_sess.query(Specialties).all()
        return jsonify(
            {
                'specialties':
                    [item.to_dict(only=('name', 'description', 'code'))
                     for item in specialty]
            }
        )


def abort_if_specialty_not_found(specialty_id):
    session = db_session.create_session()
    specialty = session.query(Specialties).get(specialty_id)
    if not specialty:
        abort(404, message=f"Specialty {specialty_id} not found")