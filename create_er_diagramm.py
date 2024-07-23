from sqlalchemy import create_engine
from sqlalchemy_schemadisplay import create_schema_graph
from src.models.base import BaseModel

def generate_erd():
    # Létrehozzuk az SQLAlchemy engine-t
    engine = create_engine('sqlite:///C:\\Users\\tarno\\automoso_dev\\CarWash\\db\\car_wash.db')

    # Alap adatbázis séma generálás
    BaseModel.metadata.create_all(engine)

    # Generáljuk az ER diagramot
    graph = create_schema_graph(engine = engine,metadata=BaseModel.metadata)
    graph.write_png('erd_diagram.png')

generate_erd()