class EmptyDataFrameException(Exception):
    def __init__(self, message: str = 'The DataFrame has no data.'):
        super().__init__(message)