from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session, declarative_base
from typing import Type, TypeVar, List, Optional

Base = declarative_base()
T = TypeVar('T', bound='BaseModel')

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    @classmethod
    def get_by_id(cls: Type[T], session: Session, obj_id: int) -> Optional[T]:
        try:
            return session.query(cls).filter_by(id=obj_id).one_or_none()
        except Exception as e:
            session.rollback()
            raise e
    
    @classmethod
    def get_all(cls: Type[T], session: Session, skip: int = 0, limit: int = 10) -> List[T]:
        try:
            return session.query(cls).offset(skip).limit(limit).all()
        except Exception as e:
            session.rollback()
            raise e
    
    @classmethod
    def update_by_id(cls: Type[T], session: Session, obj_id: int, **kwargs) -> Optional[T]:
        try:
            obj = session.query(cls).filter_by(id=obj_id).one_or_none()
            if not obj:
                return None
            
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
                else:
                    raise ValueError(f"Invalid attribute '{key}' for {cls.__name__}")
            
            session.commit()
            return obj
        except Exception as e:
            session.rollback()
            raise e
    
    @classmethod
    def delete_by_id(cls: Type[T], session: Session, obj_id: int) -> bool:
        try:
            obj = session.query(cls).filter_by(id=obj_id).one_or_none()
            if obj:
                session.delete(obj)
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            raise e
