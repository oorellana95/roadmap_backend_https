"""Project Exception Class"""


class ProjectException(Exception):
    def __init__(self):
        self.code = None
        self.message = None
