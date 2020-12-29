def find_winning_move(game_state, next_player): # 바로 이기는 수를 찾는 함수
    for candidate_move in game_state.legal_moves(next_player): # 모든 가능한 수에 대해 반복한다.
        next_state = game_state.legal_moves(next_player)  # 이 수를 선택한 경우 어떤 일이 일어날지 계산한다.
        if next_state.is_over() and next_state.winner == next_player:
            return candidate_move # 이 수를 두면 이기므로 더 이상 탐색할 필요가 없다
    return None # 이 차례에서는 이길 수 없다
        

def eliminate_losing_moves(game_state, next_player):
    opponent = next_player.other()
    possible_moves = [] # 고려 대상인 모든 수가 들어갈 리스트
    for candidate_move in game_state.legal_moves(next_player): # 모든 가능한 수에 대해 반복
        next_state = game_state.apply_move(candidate_move) # 이 수를 둘 경우 어떤 일이 일어날지 계산
        opponent_winning_move = find_winning_move(next_state, opponent) # 이를 두면 상대가 필승점에 두게될지 계산
        if opponent_winning_move is None:
            possible_moves.append(candidate_move)
    return possible_moves

def find_two_step_win(game_state, next_player):  # 22를 만드는 수를 찾는 함수
    opponent = next_player.other()
    for candidate_move in game_state.legal_moves(next_player): # 모든 가능한 수에 대해 반복
        next_state = game_state.apply_move(candidate_move) # 이 수를 두었을 때 전체 게임이 어떻게 될지 계산한다
        good_responses = eliminate_losing_moves(next_state, opponent)
        if not good_responses:
            return candidate_move
    return None # 22가 없으면 None