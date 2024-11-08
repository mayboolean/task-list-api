from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] 

    # book object to dict representation
    def obj_to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = True if self.completed_at is not None else False

        return task_as_dict
    
    @classmethod
    # create instance from request body
    def obj_from_dict(cls, task_data):
        
        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at", None)
        )

        return new_task