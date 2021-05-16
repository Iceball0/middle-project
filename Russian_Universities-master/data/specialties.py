import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Specialties(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'specialties'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    code = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=False)

    universities = orm.relation("Universities_Specialties", back_populates='specialties')