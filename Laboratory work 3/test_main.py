import unittest


from main import (
    gen_bin_tree,
    to_dict,
    Node,
)


class TestGenBinTree(unittest.TestCase):

    def depth_dict(self, tree) -> int:
        """Глубина дерева-словаря; пустой/None -> 0."""
        if not tree:
            return 0
        if isinstance(tree, dict):
            return 1 + max(self.depth_dict(tree.get("left")), self.depth_dict(tree.get("right")))
        return self.depth_dict(to_dict(tree))

    def assert_rule_variant4(self, value: int, left_val: int, right_val: int):
        """Проверка правила порождения детей: left=value*4, right=value+1."""
        self.assertEqual(left_val, value * 4)
        self.assertEqual(right_val, value + 1)

    # тесты

    def test_default_dict_tree_basic(self):
        """По умолчанию: container='dict', root=4, height=4 — структура и глубина корректны."""
        t = gen_bin_tree()  # dict
        self.assertIsInstance(t, dict)
        self.assertEqual(t["value"], 4)
        self.assertEqual(self.depth_dict(t), 4)

        # проверим два уровня правил для нескольких узлов
        l1 = t["left"]; r1 = t["right"]
        self.assert_rule_variant4(4, l1["value"], r1["value"])

        l2l = l1["left"]; l2r = l1["right"]
        r2l = r1["left"]; r2r = r1["right"]
        self.assert_rule_variant4(l1["value"], l2l["value"], l2r["value"])
        self.assert_rule_variant4(r1["value"], r2l["value"], r2r["value"])

    def test_dataclass_tree_basic(self):
        """container='dataclass': тип Node и корректные значения на первых уровнях."""
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

        # глубина через to_dict
        self.assertEqual(self.depth_dict(to_dict(t)), 4)

    def test_height_one_leaf(self):
        """height=1 -> лист (дети None) для обоих контейнеров."""
        t_dict = gen_bin_tree(height=1, root=10, container="dict")
        self.assertEqual(t_dict, {"value": 10, "left": None, "right": None})

        t_dc = gen_bin_tree(height=1, root=10, container="dataclass")
        self.assertIsInstance(t_dc, Node)
        self.assertEqual(t_dc.value, 10)
        self.assertIsNone(t_dc.left)
        self.assertIsNone(t_dc.right)

    def test_height_less_than_one(self):
        """height<1: dict -> одиночный узел-словарь; dataclass -> None."""
        t_dict = gen_bin_tree(height=0, root=99, container="dict")
        self.assertEqual(t_dict, {"value": 99, "left": None, "right": None})

        t_dc = gen_bin_tree(height=0, root=99, container="dataclass")
        self.assertIsNone(t_dc)

    def test_invalid_container_returns_none(self):
        """Неизвестный контейнер -> None."""
        t = gen_bin_tree(container="unknown")
        self.assertIsNone(t)

    def test_to_dict_equivalence(self):
        """to_dict(dataclass) совпадает со структурой dict-дерева при тех же параметрах."""
        t_dict = gen_bin_tree(height=4, root=4, container="dict")
        t_dc = gen_bin_tree(height=4, root=4, container="dataclass")
        self.assertEqual(to_dict(t_dc), to_dict(t_dict))  # to_dict нормализует оба

    def test_values_on_known_path(self):
        """Проверим конкретные значения по известному пути."""
        # для корня 4:

        t = gen_bin_tree(height=3, root=4, container="dict")
        self.assertEqual(t["left"]["value"], 16)
        self.assertEqual(t["right"]["value"], 5)
        self.assertEqual(t["left"]["left"]["value"], 64)
        self.assertEqual(t["left"]["right"]["value"], 17)
        self.assertEqual(t["right"]["left"]["value"], 20)
        self.assertEqual(t["right"]["right"]["value"], 6)

    def test_large_height_depth_only(self):
        """На больших высотах проверяем хотя бы глубину (без полного обхода)."""
        t = gen_bin_tree(height=6, root=2, container="dict")
        self.assertEqual(self.depth_dict(t), 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
