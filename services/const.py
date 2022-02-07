import sys


class _const:
    """
    This class is a utility class that is used to manage constants. It
    enables us to define constants once so that they cannot be reset, something
    that is supported by python since it has no concept of constants.
    Inspiration for this class came from:

    http://code.activestate.com/recipes/65207-constants-in-python/?in=user-97991
    """

    class ConstError(TypeError):
        """
        Represents a problem within the constants class.

        Instances of this exception are raised when an attempt is made to
        change the value of an existing constant.
        """

        pass

    def __setattr__(self, name, value):
        """
        Sets the value of a constant.

        :param name: The name of the constant to be set.
        :param value: The value of the constant.
        :return: The value of the constant.
        :raises ConstError: If an attempt is made to change the value of an
        existing constant.
        :raise ConstError: If an attempt is made to change the value of an
        existing constant.
        """
        if name in self.__dict__:
            raise _const.ConstError(f"Can't rebind const({name})")
        self.__dict__[name] = value


sys.modules[__name__] = _const()
