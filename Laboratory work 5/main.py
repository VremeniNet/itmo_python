from dataclasses import dataclass
from typing import Any, Callable, Deque, Dict, Optional, Union, Tuple
from collections import deque


# Контейнеры узла
@dataclass
class Node:
    """Узел бинарного дерева (изменяемый dataclass).

    Attributes
        value : int
            Значение, хранимое в узле.
        left : Optional[Node]
            Левый потомок или None.
        right : Optional[Node]
            Правый потомок или None.
    """
    value: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


DictTree = Dict[str, Any]
TreeLike = Union[DictTree, Node]


def gen_bin_tree(
    height: int = 4,
    root: int = 4,
    *,
    left_branch: Callable[[int], int] = lambda v: v * 4,   # вариант 4
    right_branch: Callable[[int], int] = lambda v: v + 1,  # вариант 4
    container: str = "dict",  # "dict" | "dataclass"
) -> Optional[TreeLike]:
    """Сгенерировать бинарное дерево без рекурсии
    Args
        height : int, optional
            Высота дерева (>= 1). По умолчанию 4.
            Если значение некорректно — вернёт None.
        root : int, optional
            Значение в корне. По умолчанию 4.
        left_branch : Callable[[int], int], optional
            Функция порождения левого потомка из значения узла.
            По умолчанию для варианта 4 — lambda v: v * 4.
        right_branch : Callable[[int], int], optional
            Функция порождения правого потомка из значения узла.
            По умолчанию для варианта 4 — lambda v: v + 1.
        container : {"dict", "dataclass"}, optional
            Тип результирующего контейнера: словарь или :class: Node.
            По умолчанию "dict". Любое другое значение → None.

    Returns
    -------
    Optional[TreeLike]
        - Если container="dict" — словарь вида
          {"value": int, "left": DictTree|None, "right": DictTree|None}.
        - Если container="dataclass" — экземпляр :class: Node.
        - None, если параметры некорректны.
    """
    # «мягкая» валидация — без raise
    if not isinstance(height, int) or height < 1:
        return None
    if container not in {"dict", "dataclass"}:
        return None

    # Инициализация корня и адаптеров под выбранный контейнер
    if container == "dict":
        tree: TreeLike = {"value": root, "left": None, "right": None}

        def make_node(val: int) -> DictTree:
            return {"value": val, "left": None, "right": None}

        def set_left(n: DictTree, child: DictTree) -> None:
            n["left"] = child

        def set_right(n: DictTree, child: DictTree) -> None:
            n["right"] = child

        def get_val(n: DictTree) -> int:
            return n["value"]
    else:  # dataclass
        tree = Node(root)

        def make_node(val: int) -> Node:
            return Node(val)

        def set_left(n: Node, child: Node) -> None:
            n.left = child

        def set_right(n: Node, child: Node) -> None:
            n.right = child

        def get_val(n: Node) -> int:
            return n.value

    # Очередь узлов, хранящая пару (узел, номер_уровня)
    q: Deque[Tuple[TreeLike, int]] = deque([(tree, 1)])

    # Обход в ширину: строим уровень за уровнем
    while q:
        node, level = q.popleft()
        if level == height:
            continue  # достигли последнего уровня — детей не добавляем

        v = get_val(node)
        lch = make_node(left_branch(v))
        rch = make_node(right_branch(v))

        set_left(node, lch)
        set_right(node, rch)

        q.append((lch, level + 1))
        q.append((rch, level + 1))

    return tree


def to_dict(tree: Optional[TreeLike]) -> DictTree:
    """Преобразовать дерево к словарному представлению.

    Поддерживает оба контейнера (dict и :class: Node) и None.

    Args
        tree : Optional[TreeLike]
            Исходное дерево или None.

    Returns
        DictTree
            Рекурсивный словарь с ключами value, left, right.
            Для отсутствующей ветви возвращается пустой словарь {}.

    Examples
    --------
    >>> to_dict(None)
    {}
    >>> to_dict({"value": 1, "left": None, "right": None})
    {'value': 1, 'left': {}, 'right': {}}
    """
    if tree is None:
        return {}
    if isinstance(tree, dict):
        return {
            "value": tree["value"],
            "left": to_dict(tree["left"]),
            "right": to_dict(tree["right"]),
        }
    return {
        "value": tree.value,
        "left": to_dict(tree.left),
        "right": to_dict(tree.right),
    }


if __name__ == "__main__":
    # Демонстрация: вариант 4 (по умолчанию)
    t_dict = gen_bin_tree()
    print("DICT:", to_dict(t_dict))

    t_dc = gen_bin_tree(container="dataclass")
    print("DATACLASS:", to_dict(t_dc))
