from equipment import Equipment
from hash_chaining import HashTableChaining
from hash_open import HashTableOpen


DEMO_EQUIPMENT = [
    (101, "Проектор Epson", "305", "Исправен"),
    (112, "Ноутбук Lenovo", "210", "Исправен"),
    (123, "Принтер HP", "305", "На ремонте"),
    (105, "Монитор Samsung", "210", "Исправен"),
    (134, "Интерактивная доска", "401", "Исправен"),
]


def read_id():
    """Ввод корректного инвентарного номера."""
    while True:
        value = input("Введите инвентарный номер: ").strip()

        try:
            equipment_id = int(value)

            if equipment_id < 0:
                print("ID не может быть отрицательным.")
                continue

            return equipment_id

        except ValueError:
            print("Ошибка: ID должен быть целым числом.")


def read_required(prompt):
    """Ввод непустой строки."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Поле не может быть пустым.")


def add_equipment(registry):
    print("\n=== ДОБАВЛЕНИЕ ОБОРУДОВАНИЯ ===")

    equipment_id = read_id()

    if registry.search(equipment_id) is not None:
        print(f"Оборудование с ID {equipment_id} уже существует!")
        return

    name = read_required("Наименование: ")
    room = read_required("Аудитория: ")
    status = read_required("Состояние: ")

    equipment = Equipment(
        id=equipment_id,
        name=name,
        room=room,
        status=status
    )

    registry.insert(equipment)


def find_equipment(registry):
    print("\n=== ПОИСК ОБОРУДОВАНИЯ ===")

    equipment_id = read_id()
    equipment = registry.search(equipment_id)

    if equipment is not None:
        print("\nОборудование найдено:")
        print(equipment)
    else:
        print("Оборудование не найдено.")


def edit_equipment(registry):
    print("\n=== ИЗМЕНЕНИЕ ОБОРУДОВАНИЯ ===")

    equipment_id = read_id()
    equipment = registry.search(equipment_id)

    if equipment is None:
        print("Оборудование не найдено.")
        return

    print("\nТекущие данные:")
    print(equipment)

    print("\nВведите новые значения.")
    print("Оставьте поле пустым, чтобы сохранить старое значение.")

    name = input("Новое наименование: ").strip()
    room = input("Новая аудитория: ").strip()
    status = input("Новое состояние: ").strip()

    if not any([name, room, status]):
        print("Изменения не внесены.")
        return

    registry.update(
        equipment_id,
        name=name if name else None,
        room=room if room else None,
        status=status if status else None
    )


def remove_equipment(registry):
    print("\n=== УДАЛЕНИЕ ОБОРУДОВАНИЯ ===")

    equipment_id = read_id()
    equipment = registry.search(equipment_id)

    if equipment is None:
        print("Оборудование не найдено.")
        return

    print("\nНайденная запись:")
    print(equipment)

    confirmation = input(
        "\nПодтвердить удаление? (да/нет): "
    ).strip().lower()

    if confirmation in ("да", "д", "yes", "y"):
        registry.delete(equipment_id)
    else:
        print("Удаление отменено.")


def show_statistics(registry):
    print("\n=== СТАТИСТИКА ХЕШ-ТАБЛИЦЫ ===")

    print(f"Размер таблицы: {registry.size}")
    print(f"Количество записей: {registry.count}")
    print(f"Коллизии при вставке: {registry.collisions}")

    load_factor = registry.count / registry.size

    print(f"Коэффициент заполнения: {load_factor:.2f}")

    if isinstance(registry, HashTableChaining):
        print("Алгоритм: метод цепочек")

        lengths = [len(chain) for chain in registry.table]

        print(f"Количество непустых бакетов: {sum(x > 0 for x in lengths)}")
        print(f"Максимальная длина цепочки: {max(lengths)}")

    elif isinstance(registry, HashTableOpen):
        print("Алгоритм: линейное пробирование")

        empty = sum(item is None for item in registry.table)
        deleted = sum(
            item is registry.DELETED for item in registry.table
        )

        print(f"Свободных ячеек: {empty}")
        print(f"Удалённых ячеек: {deleted}")


def load_demo_data(registry):
    print("\n=== ЗАГРУЗКА ДЕМОНСТРАЦИОННЫХ ДАННЫХ ===")

    added = 0

    for equipment_id, name, room, status in DEMO_EQUIPMENT:
        if registry.search(equipment_id) is not None:
            print(f"ID {equipment_id} пропущен: уже существует.")
            continue

        equipment = Equipment(
            id=equipment_id,
            name=name,
            room=room,
            status=status
        )

        if registry.insert(equipment):
            added += 1

    print(f"\nУспешно добавлено записей: {added}")


def registry_menu(registry, method_name):
    while True:
        print("\n" + "=" * 45)
        print("          УПРАВЛЕНИЕ РЕЕСТРОМ")
        print("=" * 45)
        print(f"Текущий метод: {method_name}")

        print("\n1. Добавить оборудование")
        print("2. Найти оборудование")
        print("3. Изменить оборудование")
        print("4. Удалить оборудование")
        print("5. Показать хеш-таблицу")
        print("6. Показать статистику")
        print("7. Загрузить демонстрационные данные")
        print("0. Вернуться к выбору алгоритма")

        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            add_equipment(registry)

        elif choice == "2":
            find_equipment(registry)

        elif choice == "3":
            edit_equipment(registry)

        elif choice == "4":
            remove_equipment(registry)

        elif choice == "5":
            registry.display()

        elif choice == "6":
            show_statistics(registry)

        elif choice == "7":
            load_demo_data(registry)

        elif choice == "0":
            print("Возврат к выбору алгоритма.")
            break

        else:
            print("Неверный пункт меню. Повторите ввод.")


def main():
    chaining_registry = HashTableChaining(size=11)
    open_registry = HashTableOpen(size=11)

    while True:
        print("\n" + "=" * 45)
        print("       РЕЕСТР УЧЕБНОГО ОБОРУДОВАНИЯ")
        print("=" * 45)

        print("\nВыберите способ хранения:")
        print("1. Закрытая адресация (метод цепочек)")
        print("2. Открытая адресация (линейное пробирование)")
        print("0. Выход")

        choice = input("\nВаш выбор: ").strip()

        if choice == "1":
            registry_menu(
                chaining_registry,
                "Закрытая адресация (метод цепочек)"
            )

        elif choice == "2":
            registry_menu(
                open_registry,
                "Открытая адресация (линейное пробирование)"
            )

        elif choice == "0":
            print("\nРабота программы завершена.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
