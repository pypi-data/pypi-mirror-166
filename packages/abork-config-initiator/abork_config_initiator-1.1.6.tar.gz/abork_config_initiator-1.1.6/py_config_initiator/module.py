import os.path as p
from typing import List


class ParametersError(Exception):
    pass

class ParameterTypeError(Exception):
    pass

class EmptyConfigsError(Exception):
    pass


class ConfigInitiator:

    def __init__(self, path:str, template: str, filename:str='config.ini'):

        if not isinstance(path, str):
            raise ParameterTypeError('parameter "path" must be a string')

        if not isinstance(template, str):
            raise ParameterTypeError('parameter "template" must be a string')

        if not isinstance(filename, str):
            raise ParameterTypeError('parameter "filename" must be a string')

        self.path = path
        self.template = template
        self.filename = filename

        self.__check()

    @classmethod
    def from_list(cls, path:str, template:List[str], filename:str='config.ini'):

        if not isinstance(template, List):
            raise ParameterTypeError('Parameter list must be a list.')
    
        template_str = ''

        for row in template:
            template_str += row + '\n'

        return cls(path, template_str, filename)

    def __check(self):

        if not self.path or not p.exists(self.path):
            raise ValueError('Supplied path does not exist.')

        fullpath = p.join(self.path, self.filename)

        if not p.exists(fullpath):
            self.__create_file(fullpath)

        self.__check_file(fullpath)

    def __create_file(self, fullpath:str):

        with open(fullpath, mode='w') as file:
            file.write(self.template)

    def __check_file(self, fullpath:str):
        
        with open(fullpath, mode='r') as file:
            lines = file.readlines()
        
        empty_configs = []

        for line in lines:
            if line.find('=') > 0 and line.split('=')[1].isspace():
                empty_configs.append(line.split('=')[0])

        if empty_configs:
            raise EmptyConfigsError('Empty configs: ' + str(empty_configs))