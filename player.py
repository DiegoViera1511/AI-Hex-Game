from hex_board import HexBoard
import math
import random
import heapq
import time

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")
    
adj = [(0,1),(0,-1),(1,-1),(1,0),(-1,1),(-1,0)]
    
def dijsktra(board, player_id, size):
    edges = {}
    dis = {}
    heap = []
    for r in range(size):
        for c in range(size):
            edges[(r,c)] = []
            dis[(r,c)] = math.inf
            for dir in adj:
                v = (r+dir[0],c+dir[1])
                if v[0] < 0 or v[0] >= size:
                    continue
                if v[1] < 0 or v[1] >= size:
                    continue
                edges[(r,c)].append(v)
            if player_id == 2:
                if r == size - 1:
                    edges[(r,c)].append((-1,-1))
                elif r == 0:
                    if board[r][c] == 1:
                        dis[(r,c)] = 0
                    elif board[r][c] == 0:
                        dis[(r,c)] = 1
            elif player_id == 1: 
                if c == size - 1:
                    edges[(r,c)].append((-1,-1))
                elif c == 0:
                    if board[r][c] == player_id:
                        dis[(r,c)] = 0
                    elif board[r][c] == 0:
                        dis[(r,c)] = 1
            heapq.heappush(heap,(dis[(r,c)], (r,c)))
            
    #Ghost node
    edges[(-1,-1)] = []
    dis[(-1,-1)] = math.inf
    result = [100,100]

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
                if v == (-1,-1):
                    temp = result[0]
                    result[0] = actual_dist
                    result[1] = temp
            if v == (-1,-1) and actual_dist == dis[v]:
                result[1] = actual_dist
    return dis[(-1,-1)] - 1

def count_bridges(board, player_id):
    size = len(board)
    count = 0 
    for i in range(size):
        for j in range(size):
            if board[i][j] != player_id:
                continue
            for mov in adj:
                next = (i+mov[0],j+mov[1])
                if next[0] < 0 or next[0] >= size:
                    continue
                if next[1] < 0 or next[1] >= size:
                    continue
                bouns = 0 
                if player_id == 1 and next[0] == 0 or next[0] == size-1:
                    bouns = 5
                if player_id == 2 and next[1] == 0 or next[1] == size-1:
                    bouns = 5
                if board[next[0]][next[1]] == player_id:
                    count += 1
                
    return count

def count_blocks(board,player_id):
    size = len(board)
    count = 0 
    for i in range(size):
        for j in range(size):
            if player_id == 1 and board[i][j] == 1 and i == 0 or i == size-1:
                count+=1
            if player_id == 2 and board[i][j] == 2 and j == 0 or j == size-1:
                count+=1   
    return count
   

def evaluate(current_id,board: HexBoard):
    h1 =  4 * (dijsktra(board.board, 3-current_id, board.size) - dijsktra(board.board, current_id, board.size))
    h2 =  (count_bridges(board.board, current_id) - count_bridges(board.board, 3-current_id))
    h3 =  (count_blocks(board.board,current_id))
    return h1 + h2 + h3

class VieraPlayer (Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)

    def minimax(self, depth:int, board: HexBoard, alpha:int, beta:int, current_id:int):
        if board.check_connection(self.player_id):
            return 10000
        if board.check_connection(3 - self.player_id):
            return - 10000
        if depth == 0 :
            return evaluate(current_id,board)
        if len(board.get_possible_moves()) == 0:
            return 0
            
        possible_moves = board.get_possible_moves()

        if current_id == self.player_id:
            max_score = - math.inf
            for move in possible_moves:
                copy_board = board.clone()
                copy_board.place_piece( move[0], move[1], current_id )
                score = self.minimax(depth - 1,copy_board, alpha, beta, 3 - current_id)
                max_score = max(max_score , score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score
        
        if current_id == 3 - self.player_id:
            min_score = math.inf
            for move in possible_moves:
                copy_board = board.clone()
                copy_board.place_piece( move[0], move[1], current_id )
                score = self.minimax(depth - 1, copy_board, alpha, beta, 3 - current_id)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score
        
    def play(self, board: HexBoard) -> tuple:
        best_move = None
        best_score = - math.inf
        alpha = - math.inf
        beta = math.inf
        depth = 1
        possible_moves = board.get_possible_moves()
        random.shuffle(possible_moves)
        if len(possible_moves) <= 36:
            depth = 3
        init_time = time.time()  
        limit_time = 8    
        for move in possible_moves:
            copy_board = board.clone()
            copy_board.place_piece( move[0], move[1], self.player_id )
            if copy_board.check_connection(self.player_id):
                best_move = move
                break
            copy_board.board[move[0]][move[1]] = 3-self.player_id
            if copy_board.check_connection(3-self.player_id):
                best_move = move
                break
            copy_board.board[move[0]][move[1]] = self.player_id
            current_time = time.time()
            boniato_time = current_time - init_time
            if boniato_time >= limit_time:
                break
            score = self.minimax(depth,copy_board, alpha, beta, 3 - self.player_id )
            board.board[move[0]][move[1]] = 0
            if score > best_score:
                best_score = score
                best_move = move
                alpha = max(alpha,score)
        if best_move is None:
            best_move = random.choice(possible_moves)        
        return best_move