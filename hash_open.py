from equipment import Equipment


class HashTableOpen:
    DELETED = object()

    def __init__(self, size=11):
        if size <= 0:
            raise ValueError("Размер таблицы должен быть положительным")

        self.size = size
        self.table = [None] * size
        self.count = 0
        self.collisions = 0

    def hash_function(self, key):
        return key % self.size

    def insert(self, equipment: Equipment):
        start_index = self.hash_function(equipment.id)
        first_deleted = None
        collisions = 0

        for i in range(self.size):
            index = (start_index + i) % self.size
            current = self.table[index]

            if current is None:
                target = (
                    first_deleted
                    if first_deleted is not None
                    else index
                )

                self.table[target] = equipment
                self.count += 1
                self.collisions += collisions

                print(
                    f"Оборудование с ID {equipment.id} "
                    f"добавлено в ячейку {target}."
                )
                return True

            if current is self.DELETED:
                if first_deleted is None:
                    first_deleted = index
                continue

            if current.id == equipment.id:
                print(
                    f"Оборудование с ID {equipment.id} "
                    "уже существует!"
                )
                return False

            collisions += 1

        if first_deleted is not None:
            self.table[first_deleted] = equipment
            self.count += 1
            self.collisions += collisions

            print(
                f"Оборудование с ID {equipment.id} "
                f"добавлено в ячейку {first_deleted}."
            )
            return True

        print("Ошибка: хеш-таблица полностью заполнена!")
        return False

    def search(self, equipment_id):
        start_index = self.hash_function(equipment_id)

        for i in range(self.size):
            index = (start_index + i) % self.size
            current = self.table[index]

            if current is None:
                return None

            if current is self.DELETED:
                continue

            if current.id == equipment_id:
                return current

        return None

    def update(self, equipment_id, name=None, room=None, status=None):
        equipment = self.search(equipment_id)

        if equipment is None:
            print(f"Оборудование с ID {equipment_id} не найдено.")
            return False

        if name is not None:
            equipment.name = name

        if room is not None:
            equipment.room = room

        if status is not None:
            equipment.status = status

        print(f"Оборудование с ID {equipment_id} обновлено.")
        return True

    def delete(self, equipment_id):
        start_index = self.hash_function(equipment_id)

        for i in range(self.size):
            index = (start_index + i) % self.size
            current = self.table[index]

            if current is None:
                break

            if current is self.DELETED:
                continue

            if current.id == equipment_id:
                self.table[index] = self.DELETED
                self.count -= 1

                print(
                    f"Оборудование с ID {equipment_id} "
                    "удалено."
                )
                return True

        print(f"Оборудование с ID {equipment_id} не найдено.")
        return False

    def display(self):
        print("\n=== ХЕШ-ТАБЛИЦА (ОТКРЫТАЯ АДРЕСАЦИЯ) ===")

        for index, item in enumerate(self.table):
            if item is None:
                print(f"[{index}] Пусто")
            elif item is self.DELETED:
                print(f"[{index}] Удалено")
            else:
                print(f"[{index}] {item}")

        print(f"\nКоличество записей: {self.count}")
        print(f"Количество коллизий при вставке: {self.collisions}")
        print(
            f"Коэффициент заполнения: "
            f"{self.count / self.size:.2f}"
        )
