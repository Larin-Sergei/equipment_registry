from dataclasses import dataclass


@dataclass
class Equipment:
    id: int
    name: str
    room: str
    status: str

    def __str__(self):
        return (
            f"ID: {self.id} | "
            f"Название: {self.name} | "
            f"Аудитория: {self.room} | "
            f"Состояние: {self.status}"
        )
