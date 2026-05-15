
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"sslmode": "require"}
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TESTE DE CONEXÃO: Adicione Apenas nesse moemnto
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("✅ SUCESSO: O Python conectou no PostgreSQL!")
    except Exception as e:
        print(f"❌ ERRO: Não conectou. Motivo: {e}")