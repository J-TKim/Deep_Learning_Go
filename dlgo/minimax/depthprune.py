import random

from dlgo.agent.base import Agent
from dlgo.scoring import GameResult


__all__ = [
    'AlphaBetaAgent',
]

MAX_SCORE = 999999
MIN_SCORE = -999999


def reverse_game_result(game_result):
    if game_result == GameResult.loss:
        return game_result.win
    if game_result == GameResult.win:
        return game_result.loss
    return GameResult.draw


def best_result(game_state, max_depth, eval_fn):
    if game_state.is_over(): # 경기가 끝났을 때 승자 확인
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE
    
    if max_depth == 0: # 최대 탐색 깊이까지 도달했을 때 복기
        return eval_fn(game_state)
    
    best_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves(): # 모든 가능한 수를 반복
        next_state = game_state.apply_move(candidate_move) # 만약 이 수를 둔다면 판세가 어떻게 될지 계산
        opponent_best_result = best_result( # 이 위치에서 상대가 낼 수 있는 최상의 결과 탐색
            next_state, max_depth - 1, eval_fn)
        our_result = -1 * opponent_best_result
        if our_result > best_so_far: # 최선의 결과보다 낫다면 best_so_far에 저장
            best_so_far = our_result
    
    return best_so_far


class DepthPruendAgent(Agent):
    def __init__(self, max_depth, eval_fn):
        Agent.__init__(self)
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    def select_move(self, game_state):
        best_moves = []
        best_score = None
        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            opponent_best_result = best_result(next_state, self.max_depth, self.eval_fn)
            our_best_outcome = -1 * opponent_best_result
            if (not best_moves) or our_best_outcome > best_score:
                best_moves = [possible_move]
                best_score = our_best_outcome
            elif our_best_outcome == best_score:
                best_moves.append(possible_move)
        return random.choice(best_moves)
