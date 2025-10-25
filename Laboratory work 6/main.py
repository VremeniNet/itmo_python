from dataclasses import dataclass
from typing import Any, Callable, Deque, Dict, Optional, Tuple, Union, Iterable, List
from collections import deque
import timeit
import statistics as stats
import matplotlib.pyplot as plt


# Контейнеры

@dataclass
class Node:
    """Узел бинарного дерева.

    Attributes:
        value: Значение в узле.
        left: Левый потомок или None.
        right: Правый потомок или None.
    """
    value: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


DictTree = Dict[str, Any]
TreeLike = Union[DictTree, Node]


# ариант 4 (по умолчанию)

def rule_left(v: int) -> int:
    """Левый потомок: left(v) = v * 4 (вариант 4)."""
    return v * 4


def rule_right(v: int) -> int:
    """Правый потомок: right(v) = v + 1 (вариант 4)."""
    return v + 1


# Утилиты контейнеров

def make_node_dict(val: int) -> DictTree:
    """Создать узел-словарь."""
    return {"value": val, "left": None, "right": None}


def to_dict(tree: Optional[TreeLike]) -> DictTree:
    """Преобразовать дерево к словарному представлению.

    Работает и для dict, и для dataclass Node, и для None (возвращает пустой словарь).
    """
    if tree is None:
        return {}
    if isinstance(tree, dict):
        return {
            "value": tree.get("value"),
            "left": to_dict(tree.get("left")),
            "right": to_dict(tree.get("right")),
        }
    return {
        "value": tree.value,
        "left": to_dict(tree.left),
        "right": to_dict(tree.right),
    }


# Рекурсивная генерация

def build_tree_recursive(
    *,
    height: int = 4,
    root: int = 4,
    left_branch: Callable[[int], int] = rule_left,
    right_branch: Callable[[int], int] = rule_right,
    container: str = "dict",  # "dict" | "dataclass"
) -> Optional[TreeLike]:
    """Построить бинарное дерево рекурсивно (вариант 4 по умолчанию).

    Порождает ровно `height` уровней (корень — уровень 1). На последнем уровне
    создаются листья с None-потомками.

    Args:
        height: Высота дерева (>= 1). Иначе — None.
        root: Значение в корне.
        left_branch: Формула левого потомка.
        right_branch: Формула правого потомка.
        container: Тип результирующего контейнера: "dict" или "dataclass".

    Returns:
        Дерево (dict или Node) или None при некорректных параметрах.
    """
    if not isinstance(height, int) or height < 1:
        return None
    if container not in {"dict", "dataclass"}:
        return None

    if height == 1:
        if container == "dict":
            return make_node_dict(root)
        return Node(root)

    left_val = left_branch(root)
    right_val = right_branch(root)

    left_sub = build_tree_recursive(
        height=height - 1,
        root=left_val,
        left_branch=left_branch,
        right_branch=right_branch,
        container=container,
    )
    right_sub = build_tree_recursive(
        height=height - 1,
        root=right_val,
        left_branch=left_branch,
        right_branch=right_branch,
        container=container,
    )
    if left_sub is None or right_sub is None:
        return None

    if container == "dict":
        node = make_node_dict(root)
        node["left"] = left_sub
        node["right"] = right_sub
        return node
    # dataclass
    return Node(root, left_sub if isinstance(left_sub, Node) else _dict_to_node(left_sub),
                right_sub if isinstance(right_sub, Node) else _dict_to_node(right_sub))


def _dict_to_node(tree: DictTree) -> Optional[Node]:
    """Внутренняя утилита: словарь -> Node (рекурсивно)."""
    if not tree:
        return None
    return Node(
        value=tree.get("value"),
        left=_dict_to_node(tree.get("left")) if isinstance(tree.get("left"), dict) else tree.get("left"),
        right=_dict_to_node(tree.get("right")) if isinstance(tree.get("right"), dict) else tree.get("right"),
    )


# Нерекурсивная генерация

def build_tree_iterative(
    *,
    height: int = 4,
    root: int = 4,
    left_branch: Callable[[int], int] = rule_left,
    right_branch: Callable[[int], int] = rule_right,
    container: str = "dict",  # "dict" | "dataclass"
) -> Optional[TreeLike]:
    """Построить бинарное дерево без рекурсии.

    Алгоритм создаёт дерево по уровням до `height`. Корень — уровень 1.

    Args:
        height: Высота дерева (>= 1). Иначе — None.
        root: Значение в корне.
        left_branch: Формула левого потомка.
        right_branch: Формула правого потомка.
        container: Тип результирующего контейнера: "dict" или "dataclass".

    Returns:
        Дерево (dict или Node) или None при некорректных параметрах.
    """
    if not isinstance(height, int) or height < 1:
        return None
    if container not in {"dict", "dataclass"}:
        return None

    if container == "dict":
        tree: TreeLike = make_node_dict(root)
        def make_node(v: int) -> DictTree: return make_node_dict(v)
        def set_left(n: DictTree, ch: DictTree) -> None: n["left"] = ch
        def set_right(n: DictTree, ch: DictTree) -> None: n["right"] = ch
        def get_val(n: DictTree) -> int: return n["value"]
    else:
        tree = Node(root)
        def make_node(v: int) -> Node: return Node(v)
        def set_left(n: Node, ch: Node) -> None: n.left = ch
        def set_right(n: Node, ch: Node) -> None: n.right = ch
        def get_val(n: Node) -> int: return n.value

    q: Deque[Tuple[TreeLike, int]] = deque([(tree, 1)])
    while q:
        node, level = q.popleft()
        if level == height:
            continue
        v = get_val(node)
        lch = make_node(left_branch(v))
        rch = make_node(right_branch(v))
        set_left(node, lch)
        set_right(node, rch)
        q.append((lch, level + 1))
        q.append((rch, level + 1))
    return tree


# Бенчмарк и график

def benchmark_series(
    heights: Iterable[int],
    repeats: int = 7,
    *,
    root: int = 4,
    container: str = "dict",
    left_branch: Callable[[int], int] = rule_left,
    right_branch: Callable[[int], int] = rule_right,
) -> Dict[str, List[float]]:
    """Измерить время построения рекурсивной и нерекурсивной реализаций.

    Для каждой высоты из `heights` запускает обе функции с одинаковыми параметрами
    и берёт медиану времени по `repeats` повторов (по одному построению на повтор).

    Args:
        heights: Набор высот для тестирования.
        repeats: Сколько раз повторять измерение для каждой точки.
        root: Значение в корне (одинаково для обеих реализаций).
        container: Тип контейнера ("dict" | "dataclass").
        left_branch, right_branch: Формулы порождения потомков.

    Returns:
        Словарь со списками одинаковой длины:
        {
          "height": [...],
          "iter_ms": [...],
          "rec_ms":  [...],
        }
    """
    hts = list(heights)
    iter_ms: List[float] = []
    rec_ms: List[float] = []

    for h in hts:
        # iterative
        t_iter = timeit.repeat(
            lambda: build_tree_iterative(
                height=h, root=root, left_branch=left_branch,
                right_branch=right_branch, container=container
            ),
            repeat=repeats, number=1
        )
        iter_ms.append(1000.0 * stats.median(t_iter))

        # recursive
        t_rec = timeit.repeat(
            lambda: build_tree_recursive(
                height=h, root=root, left_branch=left_branch,
                right_branch=right_branch, container=container
            ),
            repeat=repeats, number=1
        )
        rec_ms.append(1000.0 * stats.median(t_rec))

    return {"height": hts, "iter_ms": iter_ms, "rec_ms": rec_ms}


def plot_results(series: Dict[str, List[float]], out_path: str = "btree_benchmark.png") -> str:
    """Построить график: высота vs время (мс)."""
    plt.figure()
    plt.plot(series["height"], series["iter_ms"], marker="o", label="Нерекурсивная (BFS)")
    plt.plot(series["height"], series["rec_ms"], marker="o", label="Рекурсивная")
    plt.xlabel("Высота дерева (h)")
    plt.ylabel("Время построения, мс (медиана)")
    plt.title("Бинарное дерево: рекурсивная vs нерекурсивная генерация (вариант 4)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.savefig(out_path, dpi=160, bbox_inches="tight")
    return out_path


# Демонстрация

def main() -> None:
    """Пример запуска бенчмарка и вывода результатов."""
    heights = [1, 2, 3, 4, 5, 6, 7]
    series = benchmark_series(heights, repeats=9, root=4, container="dict")

    # Таблица
    print("Время построения (медиана, мс):")
    print(f"{'h':>3} | {'нерекурсивная':>14} | {'рекурсивная':>11}")
    print("-" * 36)
    for h, ti, tr in zip(series["height"], series["iter_ms"], series["rec_ms"]):
        print(f"{h:3d} | {ti:14.3f} | {tr:11.3f}")

    # Чистый бенчмарк одного построения на выбранной высоте
    h0 = 5 if 5 in series["height"] else series["height"][len(series["height"]) // 2]
    iter_one = 1000.0 * stats.median(
        timeit.repeat(lambda: build_tree_iterative(height=h0), repeat=15, number=1)
    )
    rec_one = 1000.0 * stats.median(
        timeit.repeat(lambda: build_tree_recursive(height=h0), repeat=15, number=1)
    )
    ratio = rec_one / iter_one if iter_one > 0 else float("inf")
    print("\nЧистый бенчмарк (один вызов, мс; медиана из 15 повторов):")
    print(f"h = {h0}: нерекурсивная = {iter_one:.3f} мс, рекурсивная = {rec_one:.3f} мс")
    print(f"Отношение (рекурсивная / нерекурсивная) = {ratio:.2f}×")

    # График
    out = plot_results(series)
    print(f"\nГрафик сохранён: {out}")


if __name__ == "__main__":
    main()
