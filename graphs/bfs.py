from collections import deque

glob_graph = {
    'A': ['M', 'P'],
    'M': ['A', 'N'],
    'N': ['M', 'B'],
    'P': ['A', 'B'],
    'B': ['P', 'N']
}


def bfs(start, goal, graph: dict):
    """breadth first search algorithm"""
    var_queue = deque([start])
    visited = {start: None}

    while var_queue:
        cur_node = var_queue.popleft()
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                var_queue.append(next_node)
                visited[next_node] = cur_node

    return visited


start = 'A'
goal = 'B'

visited = bfs(start, goal, glob_graph)

cur_node = goal
print(f'\n path from {goal} to {start}: \n {goal} ', end='')
while cur_node != start:
    cur_node = visited[cur_node]
    print(f'----> {cur_node} ', end='')

if __name__ == '__main__':
    pass
