import unittest

from equipment import Equipment
from hash_chaining import HashTableChaining
from hash_open import HashTableOpen


class HashTableTestsMixin:
    """
    Общие тесты для обоих алгоритмов хеширования.
    """

    TABLE_CLASS = None

    def setUp(self):
        self.registry = self.TABLE_CLASS(size=11)

        self.equipment1 = Equipment(
            101, "Проектор Epson", "305", "Исправен"
        )
        self.equipment2 = Equipment(
            112, "Ноутбук Lenovo", "210", "Исправен"
        )
        self.equipment3 = Equipment(
            123, "Принтер HP", "305", "На ремонте"
        )

    def test_insert(self):
        """Проверка добавления оборудования."""
        result = self.registry.insert(self.equipment1)

        self.assertTrue(result)
        self.assertEqual(self.registry.count, 1)
        self.assertEqual(
            self.registry.search(101),
            self.equipment1
        )

    def test_search_existing(self):
        """Поиск существующего оборудования."""
        self.registry.insert(self.equipment1)

        result = self.registry.search(101)

        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Проектор Epson")

    def test_search_missing(self):
        """Поиск несуществующего оборудования."""
        result = self.registry.search(999)

        self.assertIsNone(result)

    def test_duplicate(self):
        """Запрет повторного добавления одного ID."""
        self.registry.insert(self.equipment1)

        duplicate = Equipment(
            101, "Другой проектор", "100", "Неисправен"
        )

        result = self.registry.insert(duplicate)

        self.assertFalse(result)
        self.assertEqual(self.registry.count, 1)
        self.assertEqual(
            self.registry.search(101).name,
            "Проектор Epson"
        )

    def test_update(self):
        """Изменение данных оборудования."""
        self.registry.insert(self.equipment1)

        result = self.registry.update(
            101,
            room="310",
            status="На ремонте"
        )

        self.assertTrue(result)

        updated = self.registry.search(101)

        self.assertEqual(updated.room, "310")
        self.assertEqual(updated.status, "На ремонте")
        self.assertEqual(updated.name, "Проектор Epson")

    def test_update_missing(self):
        """Попытка изменения отсутствующей записи."""
        result = self.registry.update(
            999,
            status="Исправен"
        )

        self.assertFalse(result)

    def test_delete(self):
        """Удаление существующего оборудования."""
        self.registry.insert(self.equipment1)

        result = self.registry.delete(101)

        self.assertTrue(result)
        self.assertEqual(self.registry.count, 0)
        self.assertIsNone(self.registry.search(101))

    def test_delete_missing(self):
        """Удаление несуществующего оборудования."""
        result = self.registry.delete(999)

        self.assertFalse(result)
        self.assertEqual(self.registry.count, 0)

    def test_collisions(self):
        """Проверка нескольких ключей с одним хешем."""
        self.registry.insert(self.equipment1)
        self.registry.insert(self.equipment2)
        self.registry.insert(self.equipment3)

        self.assertEqual(self.registry.count, 3)

        for equipment_id in (101, 112, 123):
            self.assertIsNotNone(
                self.registry.search(equipment_id)
            )

        self.assertGreater(self.registry.collisions, 0)

    def test_delete_from_collision_group(self):
        """Поиск других ключей после удаления."""
        self.registry.insert(self.equipment1)
        self.registry.insert(self.equipment2)
        self.registry.insert(self.equipment3)

        self.registry.delete(112)

        self.assertIsNone(self.registry.search(112))
        self.assertIsNotNone(self.registry.search(101))
        self.assertIsNotNone(self.registry.search(123))
        self.assertEqual(self.registry.count, 2)

    def test_insert_after_delete(self):
        """Повторная вставка после удаления."""
        self.registry.insert(self.equipment1)
        self.registry.insert(self.equipment2)

        self.registry.delete(112)

        new_equipment = Equipment(
            134, "Интерактивная доска", "401", "Исправен"
        )

        result = self.registry.insert(new_equipment)

        self.assertTrue(result)
        self.assertIsNotNone(self.registry.search(134))
        self.assertEqual(self.registry.count, 2)

    def test_zero_id(self):
        """Проверка инвентарного номера 0."""
        equipment = Equipment(
            0, "Тестовое устройство", "100", "Исправен"
        )

        self.assertTrue(self.registry.insert(equipment))
        self.assertIsNotNone(self.registry.search(0))

    def test_invalid_size(self):
        """Размер таблицы должен быть положительным."""
        with self.assertRaises(ValueError):
            self.TABLE_CLASS(size=0)


class TestHashTableChaining(
    HashTableTestsMixin,
    unittest.TestCase
):
    """Тесты закрытой адресации."""

    TABLE_CLASS = HashTableChaining

    def test_chain_structure(self):
        """Коллизии должны формировать одну цепочку."""
        self.registry.insert(self.equipment1)
        self.registry.insert(self.equipment2)
        self.registry.insert(self.equipment3)

        index = self.registry.hash_function(101)

        self.assertEqual(index, 2)
        self.assertEqual(len(self.registry.table[index]), 3)
        self.assertEqual(self.registry.collisions, 2)

    def test_many_items(self):
        """Метод цепочек допускает больше записей, чем бакетов."""
        registry = HashTableChaining(size=3)

        for i in range(10):
            result = registry.insert(
                Equipment(i, f"Устройство {i}", "101", "Исправен")
            )
            self.assertTrue(result)

        self.assertEqual(registry.count, 10)

        for i in range(10):
            self.assertIsNotNone(registry.search(i))


class TestHashTableOpen(
    HashTableTestsMixin,
    unittest.TestCase
):
    """Тесты открытой адресации."""

    TABLE_CLASS = HashTableOpen

    def test_linear_probing_positions(self):
        """Проверка размещения при линейном пробировании."""
        self.registry.insert(self.equipment1)
        self.registry.insert(self.equipment2)
        self.registry.insert(self.equipment3)

        self.assertEqual(self.registry.table[2].id, 101)
        self.assertEqual(self.registry.table[3].id, 112)
        self.assertEqual(self.registry.table[4].id, 123)
        self.assertEqual(self.registry.collisions, 3)

    def test_deleted_marker(self):
        """После удаления должна оставаться метка DELETED."""
        self.registry.insert(self.equipment1)
        self.registry.insert(self.equipment2)

        self.registry.delete(112)

        self.assertIs(
            self.registry.table[3],
            self.registry.DELETED
        )

    def test_reuse_deleted_slot(self):
        """Проверка повторного использования удалённой ячейки."""
        self.registry.insert(self.equipment1)
        self.registry.insert(self.equipment2)
        self.registry.insert(self.equipment3)

        self.registry.delete(112)

        new_equipment = Equipment(
            134, "Интерактивная доска", "401", "Исправен"
        )

        self.registry.insert(new_equipment)

        self.assertEqual(self.registry.table[3].id, 134)
        self.assertIsNotNone(self.registry.search(123))

    def test_full_table(self):
        """Проверка переполнения хеш-таблицы."""
        registry = HashTableOpen(size=2)

        self.assertTrue(
            registry.insert(Equipment(1, "Ноутбук", "101", "Исправен"))
        )

        self.assertTrue(
            registry.insert(Equipment(2, "Принтер", "102", "Исправен"))
        )

        result = registry.insert(
            Equipment(3, "Монитор", "103", "Исправен")
        )

        self.assertFalse(result)
        self.assertEqual(registry.count, 2)

    def test_duplicate_after_deleted_slot(self):
        """Дубликат нельзя добавить за удалённой ячейкой."""
        self.registry.insert(self.equipment1)
        self.registry.insert(self.equipment2)
        self.registry.insert(self.equipment3)

        self.registry.delete(112)

        duplicate = Equipment(
            123, "Другой принтер", "999", "Неисправен"
        )

        result = self.registry.insert(duplicate)

        self.assertFalse(result)
        self.assertEqual(self.registry.count, 2)
        self.assertEqual(self.registry.search(123).name, "Принтер HP")

    def test_wrap_around(self):
        """Пробирование должно переходить к началу массива."""
        registry = HashTableOpen(size=5)

        registry.insert(Equipment(4, "A", "101", "Исправен"))
        registry.insert(Equipment(9, "B", "102", "Исправен"))
        registry.insert(Equipment(14, "C", "103", "Исправен"))

        self.assertEqual(registry.table[4].id, 4)
        self.assertEqual(registry.table[0].id, 9)
        self.assertEqual(registry.table[1].id, 14)


if __name__ == "__main__":
    unittest.main(verbosity=2)
