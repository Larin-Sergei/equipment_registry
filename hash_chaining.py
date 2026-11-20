from equipment import Equipment


class HashTableChaining:
    def __init__(self, size=11):
        if size <= 0:
            raise ValueError("Размер таблицы должен быть положительным")

        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0
        self.collisions = 0

    def hash_function(self, key):
        return key % self.size

    def insert(self, equipment: Equipment):
        index = self.hash_function(equipment.id)
        chain = self.table[index]

        for item in chain:
            if item.id == equipment.id:
                print(f"Оборудование с ID {equipment.id} уже существует!")
                return False

        if chain:
            self.collisions += 1

        chain.append(equipment)
        self.count += 1

        print(f"Оборудование с ID {equipment.id} добавлено.")
        return True

    def search(self, equipment_id):
        index = self.hash_function(equipment_id)

        for item in self.table[index]:
            if item.id == equipment_id:
                return item

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
        index = self.hash_function(equipment_id)
        chain = self.table[index]

        for i, item in enumerate(chain):
            if item.id == equipment_id:
                chain.pop(i)
                self.count -= 1
                print(f"Оборудование с ID {equipment_id} удалено.")
                return True

        print(f"Оборудование с ID {equipment_id} не найдено.")
        return False

    def display(self):
        print("\n=== ХЕШ-ТАБЛИЦА (МЕТОД ЦЕПОЧЕК) ===")

        for index, chain in enumerate(self.table):
            if chain:
                print(f"[{index}] " + " -> ".join(
                    str(item) for item in chain
                ))
            else:
                print(f"[{index}] Пусто")

        print(f"\nКоличество записей: {self.count}")
        print(f"Количество коллизий при вставке: {self.collisions}")
        print(f"Коэффициент заполнения: {self.count / self.size:.2f}")
