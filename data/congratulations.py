import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


# объект поздравления
class Congratulations(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'congratulations'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    send_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                  default=datetime.datetime.now)

    sender_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("users.id"),
                                  nullable=False)

    accepter_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("users.id"),
                                    nullable=False)
    holiday_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("holidays.id"))
    # __mapper_args__ = {'polymorphic_identity': 'congratulations', 'inherit_condition': id == User.id}
    sender = orm.relation('User', foreign_keys=[sender_id])
    accepter = orm.relation('User', foreign_keys=[accepter_id])

    holiday = orm.relation('Holidays')
