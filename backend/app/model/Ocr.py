from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey


class Ocr(Base):
    __tablename__ = 'ocrs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    new_owner_name = Column(String(100))
    new_owner_address_main = Column(String(100))
    new_owner_address_street = Column(Integer)
    new_owner_address_number = Column(String(50))
    raw_text = Column(Text)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at  = Column(DateTime)
    deleted_at = Column(DateTime)