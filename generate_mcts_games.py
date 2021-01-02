import argparse
import numpy as np

from dlgo.encoders.base import get_encoder_by_name
from dlgo import goboard_fast as goboard
from dlgo.mcts import mcts
from dlgo.utils import print_board, print_move


def generate_game(board_size, rounds, max_moves, temperature):
    boards, moves = [], [] # boards에는 바둑판의 상태, moves에는 수의 값을 변환해서 기록

    encoder = get_encoder_by_name('oneplane', board_size) # OnePlaneEncoder에 이름과 바둑판 크기를 지정해서 초기화

    game = goboard.GameState.new_game(board_size) # board_size 크기의 새 경기가 초기화

    bot = mcts.MCTSAgent(rounds, temperature) # 횟수와 온도가 정해진 몬테카를로 트리 탐색 에이전트를 봇으로 설정

    num_moves = 0
    while not game.is_over():
        print_board(game.board)
        move = bot.select_move(game) # 다음 수는 봇이 선택
        if move.is_play:
            boards.append(encoder.encode(game)) # 바둑 현왕을 변환한 내용을 boards에 추가

            move_one_hot = np.zeros(encoder.num_points())
            move_one_hot[encoder.encode_point(move.point)] = 1
            moves.append(move_one_hot) # 원 핫 인코딩 된 다음 수를 moves에 추가

        print_move(game.next_player, move)
        game = game.apply_move(move) # 봇의 다음 수가 바둑판에 추가
        num_moves += 1
        if num_moves > max_moves: # 정해진 최대 수에 도달할 때 까지 다음 수를 진행한다
            break

    return np.array(boards), np.array(moves)


def main():
    # ex) python generate_mcts_games.py -n 20 --board-out features.npy --move-out labels.npy
    parser = argparse.ArgumentParser()
    parser.add_argument('--board_size', '-b', type=int, default=9)
    parser.add_argument('--rounds', '-r', type=int, default=1000)
    parser.add_argument('--temperature', '-t', type=float, default=0.8)
    parser.add_argument('--max-moves', '-m', type=int, default=60, help='Max moves per game.')
    parser.add_argument('--num-games', '-n', type=int, default=10)
    parser.add_argument('--board-out')
    parser.add_argument('--move-out')

    args = parser.parse_args()
    xs = []
    ys = []

    for i in range(args.num_games): # 정해진 게임 수 만큼 대국 데이터를 생성한다
        print('Generating game %d/%d...' % (i + 1, args.num_games))
        x, y = generate_game(args.board_size, args.rounds,
                             args.max_moves, args.temperature)
        xs.append(x)
        ys.append(y)

    x = np.concatenate(xs) # 모든 대국 데이터를 생성한 후 특징과 라벨을 합친다
    y = np.concatenate(ys)

    np.save(args.board_out, x) # 명령줄에 입력된 파일명에 따라 각 파일에 특징과 라벨을 저장
    np.save(args.move_out, y)


if __name__ == '__main__':
    main()
