from __future__ import annotations
from sqlalchemy import DateTime, Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from src.database.db import Base, db_session
import uuid

class Record(Base): #Sprint 1
    __tablename__ = 'record'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    category = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)
    date = Column(DateTime, nullable=True)
    extraInfo = Column(String(255), nullable=True)
    paymentType = Column(String(255), nullable=True)
    place = Column(String(255), nullable=True)
    
    budget_id = Column(UUID(as_uuid=True), ForeignKey('budget.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, name, category, value, date, extraInfo, paymentType, place, budgetId):
        self.name = name
        self.category = category
        self.value = value
        self.date = date
        self.extraInfo = extraInfo
        self.paymentType = paymentType
        self.place = place
        self.budget_id = budgetId

    def __repr__(self):
        return f'<Record {self.name!r}>'
    
    def save(self):
        if not self.id:
            db_session.add(self)
        db_session.commit()
        # db_session.expunge() # REVIEW necessary when using a single session?
    
    def as_dict(self):
        record = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        record['id'] = str(record['id'])
        record['budget_id'] = str(record['budget_id'])
        record['date'] = str(record['date'])
        return record
    
    @staticmethod
    def all():
        return Record.query.all()

    @staticmethod
    def get(Record_id) -> Record:
        return Record.query.get(Record_id)

    @staticmethod
    def get_by_date(Record_dateTime) -> Record:
        return Record.query.filter_by(dateTime=Record_dateTime)
    
    @staticmethod
    def delete_one(record_id):
        to_delete = Record.query.get(record_id)
        db_session.delete(to_delete)
        db_session.commit()

    @staticmethod
    def exists(Record_id) -> bool:
        return Record.query.filter_by(id=Record_id).first() is not None

