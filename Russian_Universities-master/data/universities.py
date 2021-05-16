import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Universities(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'universities'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    city = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    placeInRussianTop = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    specialties = orm.relation("Universities_Specialties", back_populates='universities')
    reviews = orm.relation("Reviews", back_populates='universities')

    def __repr__(self):
        return f'<Universities> {self.id} {self.name} {self.city} {self.placeInRussianTop}'