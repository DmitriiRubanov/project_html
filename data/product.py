import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)