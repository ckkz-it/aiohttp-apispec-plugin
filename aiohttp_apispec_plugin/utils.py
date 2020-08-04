def issubclass_safe(cls, other) -> bool:
    try:
        return issubclass(cls, other)
    except TypeError:
        return False
