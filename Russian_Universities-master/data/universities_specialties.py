import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Universities_Specialties(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'universities_specialties'

    university_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("universities.id"),
                                      primary_key=True)
    specialty_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("specialties.id"),
                                     primary_key=True)
    budgetary_places = sqlalchemy.Column(sqlalchemy.Integer,
                                         nullable=True)
    universities = orm.relation("Universities", back_populates='specialties')
    specialties = orm.relation("Specialties", back_populates='universities')