import numpy as np

from dlgo.encoders.base import Encoder
from dlgo.goboard import Point


class OnePlaneEncoder(Encoder):
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 1
    
    def name(self): # oneplane라는 이름으로 이 변환기를 참조할 수 있다
        return 'oneplane'

    def encode(self, game_state):
        board_matrix = np.zeros(self.shape()) # 기본값 : 0
        next_player = game_state.next_player # 다음 차례 = 이번에 둘 기사
        for r in range(self.board_height):
            for c in range(self.board_width):
                p = Point(row=r + 1, col=c + 1)
                go_string = game_state.board.get_go_string(p)
                if go_string is None:
                    continue
                if go_string.color == next_player: # 현재 플레이어의 돌이라면 1
                    board_matrix[0, r, c] = 1
                else: # 상대 기사의 돌이라면 -1
                    board_matrix[0, r, c] = -1
            return board_matrix
        
    def encode_point(self, point): # 바둑판의 위치를 정수형 인덱스로 변환
        return self.board_width * (point.row - 1) + (point.col - 1)
    
    def decode_point_index(self, index): # 정수형 인덱스를 바둑판의 점 위치로 변환
        row = index // self.board_width
        col = index % self.board_width
        return Point(row=row + 1, col=col + 1)

    def num_points(self):
        return self.board_width * self.board_height
    
    def shape(self):
        return self.num_planes, self.board_height, self.board_width


def create(board_size):
    return OnePlaneEncoder(board_size)
