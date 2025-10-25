import unittest

from main import (
    gen_bin_tree,
    to_dict,
    Node,
)


class TestGenBinTreeVariant4(unittest.TestCase):
    # Вспомогательные методы

    def depth_dict(self, tree) -> int:
        """Глубина дерева-словаря; пустой/None -> 0."""
        if not tree:
            return 0
        if isinstance(tree, dict):
            return 1 + max(self.depth_dict(tree.get("left")), self.depth_dict(tree.get("right")))
        # если пришёл dataclass — нормализуем
        return self.depth_dict(to_dict(tree))

    def collect_levels(self, tree_dict: dict) -> list[list[int]]:
        """Собрать уровни значений (BFS) из словарного представления."""
        if not tree_dict:
            return []
        levels = []
        q = [tree_dict]
        while q:
            nxt, vals = [], []
            for node in q:
                vals.append(node["value"])
                if node.get("left"):
                    nxt.append(node["left"])
                if node.get("right"):
                    nxt.append(node["right"])
            levels.append(vals)
            q = nxt
        return levels

    def assert_rule_variant4(self, value: int, left_val: int, right_val: int):
        """Проверка правила варианта 4: left = v*4, right = v+1."""
        self.assertEqual(left_val, value * 4)
        self.assertEqual(right_val, value + 1)

    # Тесты

    def test_default_dict_tree_basic(self):
        """По умолчанию: container='dict', root=4, height=4 — структура и глубина корректны."""
        t = gen_bin_tree()  # dict
        self.assertIsInstance(t, dict)
        self.assertEqual(t["value"], 4)
        self.assertEqual(self.depth_dict(t), 4)

        # проверим правила на двух первых уровнях
        l1 = t["left"]; r1 = t["right"]
        self.assert_rule_variant4(4, l1["value"], r1["value"])

        l2l = l1["left"]; l2r = l1["right"]
        r2l = r1["left"]; r2r = r1["right"]
        self.assert_rule_variant4(l1["value"], l2l["value"], l2r["value"])
        self.assert_rule_variant4(r1["value"], r2l["value"], r2r["value"])

    def test_dataclass_tree_basic(self):
        """container='dataclass': тип Node, корректные дети и глубина."""
        t = gen_bin_tree(container="dataclass")
        self.assertIsInstance(t, Node)
        self.assertEqual(t.value, 4)

        # уровень 2
        self.assertIsInstance(t.left, Node)
        self.assertIsInstance(t.right, Node)
        self.assert_rule_variant4(4, t.left.value, t.right.value)

        # уровень 3
        self.assertIsInstance(t.left.left, Node)
        self.assertIsInstance(t.left.right, Node)
        self.assert_rule_variant4(t.left.value, t.left.left.value, t.left.right.value)

        # глубина через нормализацию
        self.assertEqual(self.depth_dict(to_dict(t)), 4)

    def test_height_one_leaf(self):
        """height=1 -> лист (детей нет) для обоих контейнеров."""
        t_dict = gen_bin_tree(height=1, root=10, container="dict")
        self.assertEqual(t_dict, {"value": 10, "left": None, "right": None})

        t_dc = gen_bin_tree(height=1, root=10, container="dataclass")
        self.assertIsInstance(t_dc, Node)
        self.assertEqual(t_dc.value, 10)
        self.assertIsNone(t_dc.left)
        self.assertIsNone(t_dc.right)

    def test_height_less_than_one_returns_none(self):
        """height<1: функция возвращает None."""
        self.assertIsNone(gen_bin_tree(height=0, root=99, container="dict"))
        self.assertIsNone(gen_bin_tree(height=0, root=99, container="dataclass"))

    def test_invalid_container_returns_none(self):
        """Неизвестный контейнер -> None."""
        self.assertIsNone(gen_bin_tree(container="unknown"))

    def test_to_dict_normalizes_both_containers(self):
        """to_dict(dataclass) совпадает по структуре с dict-деревом при тех же параметрах."""
        t_dict = gen_bin_tree(height=4, root=4, container="dict")
        t_dc = gen_bin_tree(height=4, root=4, container="dataclass")
        self.assertEqual(to_dict(t_dc), to_dict(t_dict))

    def test_values_on_known_path(self):
        """Проверим конкретные значения на известных путях для высоты 3."""
        t = gen_bin_tree(height=3, root=4, container="dict")
        self.assertEqual(t["left"]["value"], 16)   # 4*4
        self.assertEqual(t["right"]["value"], 5)   # 4+1
        self.assertEqual(t["left"]["left"]["value"], 64)   # 16*4
        self.assertEqual(t["left"]["right"]["value"], 17)  # 16+1
        self.assertEqual(t["right"]["left"]["value"], 20)  # 5*4
        self.assertEqual(t["right"]["right"]["value"], 6)  # 5+1

    def test_expected_levels_variant4(self):
        """Полная проверка уровней для высоты 4 (вариант 4)."""
        expected = [
            [4],
            [16, 5],
            [64, 17, 20, 6],
            [256, 65, 68, 18, 80, 21, 24, 7],
        ]
        as_levels = self.collect_levels(to_dict(gen_bin_tree()))
        self.assertEqual(as_levels, expected)

    def test_override_formulas(self):
        """Переопределение правил порождения работает (пример: left=v+1, right=v-1)."""
        t = gen_bin_tree(
            height=3,
            root=10,
            left_branch=lambda v: v + 1,
            right_branch=lambda v: v - 1,
            container="dict",
        )
        levels = self.collect_levels(to_dict(t))
        self.assertEqual(levels, [[10], [11, 9], [12, 10, 10, 8]])

    def test_large_height_depth_only(self):
        """На больших высотах проверяем хотя бы глубину (без полного сравнения значений)."""
        t = gen_bin_tree(height=6, root=2, container="dict")
        self.assertEqual(self.depth_dict(t), 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
