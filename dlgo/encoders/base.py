import importlib

__all__ = [
    'Encoder',
    'get_encoder_by_name',
]


class Encoder:
    def name(self): # 모델이 사용하는 변환기 이름을 로깅하거나 저장할 수 있게 한다
        raise NotImplementedError()

    def encode(self, game_state): # 바둑판을 숫자 데이터로 바꾼다
        raise NotImplementedError()

    def encode_point(self, point): # 바둑판의 점을 정수형 인덱스로 바꾼다
        raise NotImplementedError()

    def decode_point_index(self, index):  # 정수형 인덱스를 바둑판의 점으로 바꾼다
        raise NotImplementedError()

    def num_points(self): # 바둑판에 있는 점의 개수는 너비 x 높이
        raise NotImplementedError()

    def shape(self): # 변환된 바둑판 구조의 모양
        raise NotImplementedError()


def get_encoder_by_name(name, board_size): # 변환기 인스턴스에 이름 부여 가능
    if isinstance(board_size, int):
        board_size = (board_size, board_size) # board_size 가 한자리 정수인 경우 정사각형 바둑판을 만든다
    module = importlib.import_module('dlgo.encoders.' + name)
    constructor = getattr(module, 'create')
    return constructor(board_size)
