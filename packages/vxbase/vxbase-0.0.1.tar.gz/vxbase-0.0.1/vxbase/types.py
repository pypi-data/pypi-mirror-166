from six import string_types, binary_type


def is_iterable(obj):
    """ Method that verifies if an object is iterable and not a string, example:

        >>>types.is_iterable(1)
        False
        >>> types.is_iterable([1, 2, 3])
        True

    :param obj: Any object that will be tested if is iterable
    :return: True or False if the object can be iterated
    """
    return hasattr(obj, '__iter__') and not isinstance(obj, string_types + (binary_type,))
