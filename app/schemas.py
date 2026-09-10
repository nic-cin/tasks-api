from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TaskCreate(SQLModel):
    """Dados que o cliente envia para criar uma tarefa."""
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)


class TaskUpdate(SQLModel):
    """Dados para atualizar; tudo opcional, só muda o que for enviado."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    done: Optional[bool] = None


class TaskRead(SQLModel):
    """Formato de resposta da API."""
    id: int
    title: str
    description: Optional[str]
    done: bool
    created_at: datetime