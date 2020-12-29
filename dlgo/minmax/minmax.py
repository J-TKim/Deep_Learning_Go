import enum
import random
from dlgo.agent import Agent


class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3


class minimaxAgent(Agent):
    def select_move(self, game_state):
        winning_moves = []
        draw_moves = []
        losing_moves = []
        for possible_move in game_state.legal_moves():  # 가능한 모든 수에 대해 탐색한다
            next_state = game_state.apply_move(
                possible_move)  # 이 수를 골랐을 때 전체 게임이 어떻게 될지 계산한다
            # 상대가 다음 수를 두었을 때 거기서 나올 수 있는 최상의 결과가 무엇인지 구한다
            opponent_best_outcome = best_result(next_state)
            our_best_outcome = reverse_game_result(
                opponent_best_outcome)  # 결과에 따라 수를 분류
            if our_best_outcome == GameResult.win:
                winning_moves.append(possible_move)
            elif our_best_outcome == GameResult.draw:
                draw_moves.append(possible_move)
            else:
                losing_moves.append(possible_move)
        if winning_moves:  # 결과가 가장 좋게되는 수를 택한다
            return random.choice(winning_moves)
        if draw_moves:
            return random.choice(draw_moves)
        return random.choice(losing_moves)


def best_result(game_state):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return GameResult.win
        elif game_state.winner() is None:
            return GameResult.draw
        else:
            return GameResult.loss

    # 상대방의 최선의 수 찾기
    best_result_so_far = GameResult.loss
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(
            candidate_move)  # 만약에 이 수를 두면 판세가 어떻게 될지 찾아보기
        opponent_best_result = best_result(next_state)  # 상대방의 촤선의 수를 찾기
        our_result = reverse_game_result(opponent_best_result)
        if our_result.value > best_result_so_far.value:  # 이 결과가 더 나은지 확인
            best_result_so_far = our_result
    return best_result_so_far
