from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Uma tarefa. table=True faz o SQLModel criar a tabela 'task' no banco."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    done: bool = False
    created_at: datetime = Field(default_factory=datetime.now)