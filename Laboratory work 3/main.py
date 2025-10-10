from dataclasses import dataclass
from typing import Any, Dict, Optional, Union


# Контейнеры

@dataclass(frozen=True)
class Node:
    """Узел бинарного дерева.

    Attributes:
        value: Значение в узле.
        left: Левый потомок (Node) или None.
        right: Правый потомок (Node) или None.
    """
    value: int
    left: Optional["Node"]
    right: Optional["Node"]


DictTree = Dict[str, Any]
TreeLike = Union[DictTree, Node]


# Правила варианта 4

def _children_variant4(value: int) -> tuple[int, int]:
    """Правило порождения потомков для варианта 4.

    Левый потомок = value * 4
    Правый потомок = value + 1
    """
    return value * 4, value + 1


# Генератор дерева

def gen_bin_tree(
    height: int = 4,
    root: int = 4,
    *,
    container: str = "dict",
) -> Optional[TreeLike]:
    """Рекурсивно сгенерировать бинарное дерево (вариант 4).

    Порождает ровно `height` уровней (корень — уровень 1).
    На уровне `height` создаётся лист с потомками None.

    Args:
        height: Высота дерева (>=1). Если <1 — вернётся пустой словарь для
            container="dict" или None для container="dataclass".
        root: Значение в корне.
        container: "dict" или "dataclass" — тип контейнера узлов.

    Returns:
        Дерево в виде словаря или dataclass `Node`.
        Если контейнер неизвестен или построение невозможно — None.
    """
    if height < 1:
        return {"value": root, "left": None, "right": None} if container == "dict" else None

    if height == 1:
        if container == "dict":
            return {"value": root, "left": None, "right": None}
        if container == "dataclass":
            return Node(root, None, None)
        return None

    left_value, right_value = _children_variant4(root)
    left_sub = gen_bin_tree(height - 1, left_value, container=container)
    right_sub = gen_bin_tree(height - 1, right_value, container=container)

    if left_sub is None or right_sub is None:
        return None

    if container == "dict":
        return {"value": root, "left": left_sub, "right": right_sub}
    if container == "dataclass":
        # если поддеревья пришли словарями — конвертируем их в Node
        lnode = left_sub if isinstance(left_sub, Node) else _dict_to_dataclass(left_sub)
        rnode = right_sub if isinstance(right_sub, Node) else _dict_to_dataclass(right_sub)
        return Node(root, lnode, rnode)
    return None


# Преобразования

def to_dict(tree: Optional[TreeLike]) -> DictTree:
    """Преобразовать дерево любого поддерживаемого контейнера к словарю."""
    if tree is None:
        return {}
    if isinstance(tree, dict):
        return {
            "value": tree.get("value"),
            "left": to_dict(tree.get("left")),
            "right": to_dict(tree.get("right")),
        }
    # dataclass Node
    return {
        "value": tree.value,
        "left": to_dict(tree.left),
        "right": to_dict(tree.right),
    }


def _dict_to_dataclass(tree: DictTree) -> Optional[Node]:
    """Внутренняя утилита: словарь -> Node."""
    if not tree:
        return None
    left = tree.get("left")
    right = tree.get("right")
    return Node(
        value=tree.get("value"),
        left=_dict_to_dataclass(left) if isinstance(left, dict) else left,
        right=_dict_to_dataclass(right) if isinstance(right, dict) else right,
    )




if __name__ == "__main__":
    t_dict = gen_bin_tree()
    t_dc = gen_bin_tree(container="dataclass")

    print("DICT:")
    print(t_dict)

    print("\nDATACLASS:")
    print(to_dict(t_dc))
