import math
import heapq

adj = [(0,1),(0,-1),(1,-1),(1,0),(-1,1),(-1,0)]

def dfs(g,player_id,size):
    visited = set()
    p = {}
    for u in g:
        if player_id == 1 and u[1] != 0:
            continue
        if player_id == 2 and u[0] != 0:
            continue
        if u not in visited:
            p[(u[0],u[1])] = None
            if dfs_visit(g,u,visited,p,size,player_id):
                return True
    return False

def dfs_visit(g,u,visited,p,size,player_id):
    visited.add((u))
    for dir in adj:
        v = (u[0]+dir[0],u[1]+dir[1])
        if v not in g:
            continue
        if player_id == 1 and v[1] == size - 1:
            p[v] = u
            return True
        if player_id == 2 and v[0] == size - 1:
            p[v] = u
            return True
        if v not in visited:
            p[v] = u
            if dfs_visit(g,v,visited,p,size,player_id):
                return True
    return False

def dijsktra(board, player_id, size):
    edges = {}
    for r in range(size):
        for c in range(size):
            edges[(r,c)] = []
            for dir in adj:
                v = (r+dir[0],c+dir[1])
                if v[0] < 0 or v[0] >= size:
                    continue
                if v[1] < 0 or v[1] >= size:
                    continue
                edges[(r,c)].append(v)
    #Ghost node
    if player_id == 1:
        for i in range(size):
            edges[(size-1,i)].append((-1,-1))
    else:
        for i in range(size):
            edges[(i,size-1)].append((-1,-1))
    edges[(-1,-1)] = []

    dis = {(r, c): math.inf for r in range(size) for c in range(size)}
    dis[(-1,-1)] = math.inf

    heap = []

    if player_id == 1:
        for i in range(size):
            if board[0][i] == 1:
                dis[(0,i)] = 0
            if board[0][i] == 0:
                dis[(0,i)] = 1
    else:
        for i in range(size):
            if board[i][0] == player_id:
                dis[(i,0)] = 0
            if board[i][0] == 0:
                dis[(i,0)] = 1

    for u in dis:
        heapq.heappush(heap,(dis[u], u))
    while heap:
        u = heapq.heappop(heap)
        if u[0] > dis[u[1]]:
            continue
        for v in edges[u[1]]:
            if board[v[0]][v[1]] == player_id:
                cost = 0
            if board[v[0]][v[1]] == 0:
                cost = 1
            else:
                continue
            actual_dist = dis[u[1]] + cost 
            if actual_dist < dis[v]:
                dis[v] = actual_dist
                heapq.heappush(heap,(dis[v] , v))
    return dis[(-1,-1)] - 1

def count_bridges(board, player_id):
    size = len(board)
    count = 0 
    for i in range(size):
        for j in range(size):
            if board[i][j] != 0:
                continue
            for mov in adj:
                next = (i+mov[0],j+mov[1])
                if next[0] < 0 or next[0] >= size:
                    continue
                if next[1] < 0 or next[1] >= size:
                    continue
                if board[next[0]][next[1]] == player_id:
                    count += 1
                    break
    return count


                


