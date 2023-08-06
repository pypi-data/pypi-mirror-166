import os
import sys
import subprocess
from steam_sdk.parsers.ParserYAML import yaml_to_data_class
from steam_sdk.data.DataFiQuS import DataFiQuS
import pip
import subprocess
import sys


class DriverFiQuS:
    """
        Class to drive FiQuS models
    """

    def __init__(self, FiQuS_path='', FiQuS_GetDP_path=''):
        sys.path.insert(0, FiQuS_path)
        from fiqus.MainFiQuS import MainFiQuS as MF
        self.MainFiQuS = MF

    def run_FiQuS(self, input_file_path: str, model_folder: str = 'output', verbose=True):

        self.MainFiQuS(input_file_path=input_file_path, model_folder=model_folder)


