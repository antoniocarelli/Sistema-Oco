from app.core.database import Base, engine
from app.models.user import User

def init_db():
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_db() 