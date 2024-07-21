from typing import Type, List, TypeVar, Any, Optional
from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import inspect

Base = declarative_base()

T = TypeVar('T')

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def add(cls, session, **kwargs):
        try:
            instance = cls()
            for key, value in kwargs.items():
                if not hasattr(instance, key):
                    raise AttributeError(f"Invalid attribute: {key}")
                setattr(instance, key, value)
            session.add(instance)
            session.commit()
            return instance
        except AttributeError as e:
            print(e)
        except Exception as e:
            print("An error occurred: ", e)
            session.rollback()
            
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
    
    @classmethod
    def filter_by_column_value(cls: Type[T], session: Session, column_name: str, value: Any, skip: int = 0, limit: int = 10) -> List[T]:
        try:
            mapper = inspect(cls)
            if column_name not in mapper.columns:
                raise ValueError(f"Column '{column_name}' does not exist in class '{cls.__name__}'")
    
            filter_args = {column_name: value}
            query = session.query(cls).filter_by(**filter_args).offset(skip).limit(limit).all()
            return query
        except Exception as e:
            session.rollback()
            raise e
