def Singleton(
    class_
) -> object:
    """
    A decorator used to define a singleton class.
    """
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance