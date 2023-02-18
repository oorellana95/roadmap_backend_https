class File(object):
    def __init__(self, path: str, method: str):
        self.file_obj = open(path, method)

    def __enter__(self):
        return self.file_obj

    def __exit__(self, type, value, traceback):
        self.file_obj.close()
        return True

