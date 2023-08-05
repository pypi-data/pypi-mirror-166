class EmptyDataFrameException(Exception):
    """
    An error defined when a DataFrame is empty and should have something
    for the process to work fine.

    Args:
        Exception (Exception): The same set of arguments you would pass
        to any normal exception in python.
    """
    def __init__(self, message: str = 'The DataFrame has no data.'):
        super().__init__(message)