from datetime import datetime, UTC
from sqlalchemy import Column, Integer, DateTime
from app.core.database import Base

class BaseModel(Base):
    """
    Classe base para todos os modelos.
    Inclui campos comuns como id, criado_em e atualizado_em.
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    criado_em = Column(DateTime, default=datetime.now(UTC))
    atualizado_em = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC)) 