from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.db.base import Base
from app.db.base import SessionLocal

class Ocr(Base):
    __tablename__ = 'ocrs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    new_owner_name = Column(String(100))
    new_owner_address_main = Column(String(100))
    new_owner_address_street = Column(String(50))
    new_owner_address_number = Column(String(50))
    raw_text = Column(Text)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at  = Column(DateTime)
    deleted_at = Column(DateTime, nullable=True)

    @classmethod
    def create(cls, **kwargs):
        ocr_record = cls(**kwargs)
        print("Ocr.create に渡されたデータ:", kwargs)
        try:
            with SessionLocal() as session:
                session.add(ocr_record)
                session.commit()
                session.refresh(ocr_record)
            return ocr_record
        except Exception as e:
            print(f"エラーが発生しました。{e}")
            return None
        
    @classmethod
    def get_by_user(cls, user_id):
        with SessionLocal() as session:
            return session.query(cls).filter(cls.user_id == user_id, cls.deleted_at.is_(None)).all()
        
    @classmethod
    def get_by_id(cls, ocr_id):
        with SessionLocal() as session:
         return session.query(cls).filter(cls.id == ocr_id).first()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now(ZoneInfo('Asia/Tokyo'))
        print(f"[OCR UPDATE] ID: {self.id} が更新されました")
        try:
            with SessionLocal() as session:
                session.merge(self)
                session.commit()
        except Exception as e:
            print(f"エラーが発生しました。{e}")


    def delete(self):
        self.deleted_at = datetime.now(ZoneInfo('Asia/Tokyo'))
        try:
            with SessionLocal() as session:
                session.merge(self)
                session.commit()
        except Exception as e:
            print(f"[削除エラー]{e}")
