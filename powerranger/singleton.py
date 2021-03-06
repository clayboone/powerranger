from typing import Dict, Type, Callable


class SingletonMeta(type):
    """A metaclass for singletons.

    See:
    https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances: Dict[Type, Callable] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]
