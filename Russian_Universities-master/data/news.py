import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    university_id = sqlalchemy.Column(sqlalchemy.Integer,
                                      sqlalchemy.ForeignKey("universities.id"), primary_key=True)
    url = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    news_url = sqlalchemy.Column(sqlalchemy.Text, nullable=False)