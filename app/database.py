from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    """Cria o arquivo tasks.db e as tabelas de todos os modelos com table=True."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Abre uma sessão por requisição e fecha ao terminar."""
    with Session(engine) as session:
        yield session