def bfs(queue, path, start_box, target_box):
    if len(queue) > 0:
        current_box = queue.pop(0)
        current_box.visited = True
        if current_box == target_box:
            while current_box.father != start_box and current_box.father is not None:
                path.append(current_box.father)
                current_box = current_box.father
            return True
        else:
            for neighbour in current_box.neighbours:
                if not neighbour.queued and not neighbour.wall:
                    neighbour.queued = True
                    neighbour.father = current_box
                    queue.append(neighbour)

    return False


def dfs(queue, path, start_box, target_box):
    if len(queue) > 0:
        current_box = queue.pop()
        current_box.visited = True
        if current_box == target_box:
            while current_box.father != start_box and current_box.father is not None:
                path.append(current_box.father)
                current_box = current_box.father
            return True
        else:
            for neighbour in current_box.neighbours:
                if not neighbour.queued and not neighbour.wall:
                    neighbour.queued = True
                    neighbour.father = current_box
                    queue.append(neighbour)

    return False