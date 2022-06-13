import json
from os import path
try:
    from lib.logger import Logger
    from lib.utils import flatdict
except ImportError:
    print('error while importing logger in configloader')


class Statics: # DO NOT EDIT THIS VALUES
    ENTRY_POINT = 'https://kkutu.co.kr/o/login/'
    GAME_MAIN_ENTRY_POINT = 'https://kkutu.co.kr/o/game?server='
    OUTGAME_USERNAME_CSS_SELECTOR = '#MeBox div.product-body div.my-stat .my-stat-name.ellipse'
    INGAME_USER_CSS_NAME = 'game-user'
    INGAME_USERNAME_CSS_NAME = 'game-user-name'


class Config:
    default_form = {
        'typing': {
            'delay_min': float,
            'delay_max': float,
            'delay_random': bool
        }
    }

    def __init__(self, log: Logger):
        self.log = log
        self.log.info('Loading configs...')

        if path.exists('config.json'):

            self.log.success('Config file found!')
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            self.log.success('Config file loaded.')

            if not self.check_config_format(self.config):
                self.log.warning('Config file format is invalid!')
                self.log.warning('Please check config.json format.')
                self.log.warning('Using default configs.')
                self.config = {}

        if not path.exists('config.json') or not self.config:  # Setting default configurations
            self.config = {  # DO NOT EDIT THIS VALUES
                'typing': {
                    'delay_min': 0.01,
                    'delay_max': 0.1,
                    'delay_random': True
                }
            }

        self.log.success('Configs successfully loaded.')
        for key, value in flatdict(self.config).items():
            self.log.info(f'{key}\t:\t{value}')

    def get(self, dictpath: str = None):
        if not dictpath:
            return self.config
        result_config = self.config
        for key in dictpath.split('.'):
            result_config = result_config[key]
        return result_config

    def set(self, dictpath: str, value: any):
        result_config = self.config
        for key in dictpath.split('.')[:-1]:
            result_config = result_config[key]
        result_config[dictpath.split('.')[-1]] = value

    def check_config_format(self, form, default_form_path:str=None):
        default_form = self.default_form
        if default_form_path:
            for key in default_form_path.split('.'):
                default_form = default_form[key]
        for key, value in form.items():
            if key not in default_form:
                return False
            if isinstance(value, dict):
                if not self.check_config_format(value, f'{default_form_path}.{value}'):
                    return False
            elif not isinstance(value, default_form[key]):
                return False
        return True
