import os.path
import tarfile
import gzip
import glob
import shutil

import numpy as np
from keras.utils import to_categorical

from dlgo.gosgf.sgf import Sgf_game
from dlgo.goboard_fast import Board, GameState, Move
from dlgo.gotypes import Player, Point
from dlgo.encoders.base import get_encoder_by_name

from dlgo.data.index_processor import KGSIndex
from dlgo.data.sampling import Sampler  # 이를 이용해서 train, valid데이터를 샘플링 한다



class GoDataProcessor:
    def __init__(self, encoder='oneplane', data_directory='data'):
        self.encoder = get_encoder_by_name(encoder, 19)
        self.data_dir = data_directory

    def load_go_data(self, data_type='train', num_samples=1000): # data_type에 train or test 지정 가능
        index = KGSIndex(data_directory=self.data_dir)
        index.download_files() # 데이터가 없으면 다운로드

        sampler = Sampler(data_dir=self.data_dir)
        data = sampler.draw_data(data_type, num_samples)

        zip_names = set()
        indices_by_zip_name = {}
        for filename, index in data:
            zip_names.add(filename) # 데이터의 모든 zip파일 이름을 리스트에 저장
            if filename not in indices_by_zip_name:
                indices_by_zip_name[filename] = []
            indices_by_zip_name[filename].append(index) # zip파일로 인덱싱된 SGF파일을 모은다
        for zip_name in zip_names:
            base_name = zip_name.replace('.tar.gz', '')
            data_file_name = base_name + data_type
            if not os.path.isfile(self.data_dir, + '/' + data_file_name):
                self.process_zip(zip_name, data_file_name,
                                indices_by_zip_name[zip_name]) # zip파일 처리

        features_and_labels = self.consolidate_games(data_type, data) # 특징과 label을 집계한 후 반환
        return features_and_labels