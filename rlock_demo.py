import threading


class SharedGraph:
    def __init__(self):
        self._lock = threading.RLock()
        self._graph = {}

    def add_edge(self, source, target):
        with self._lock:
            self._graph.setdefault(source, []).append(target)

    def reachable(self, current, target, visited=None):
        # 整次递归遍历期间，图不能被其他线程修改
        with self._lock:
            if visited is None:
                visited = set()

            if current == target:
                return True

            if current in visited:
                return False

            visited.add(current)

            for neighbor in self._graph.get(current, []):
                # 真实递归：同一线程再次进入 reachable()
                if self.reachable(neighbor, target, visited):
                    return True

            return False


graph = SharedGraph()

graph.add_edge("A", "B")
graph.add_edge("B", "C")
graph.add_edge("C", "D")

print(graph.reachable("A", "D"))  # True