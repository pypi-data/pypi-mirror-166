import inspect
import sys


def verify_isinstance(argument, types, optional=False):
    """
    Verifies that the argument is an instance of the type(s).
    """
    if optional and argument is None:
        return

    if not isinstance(argument, types):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find("(") + 1:-1].split(",")
        argument_name = args[0]
        raise TypeError(f"Argument {argument_name!r} must be an instance of {types}, not {type(argument)}.")


def verify_issubclass(argument, types, optional=False):
    """
    Verifies that the argument is a subclass of the type(s).
    """
    if optional and argument is None:
        return

    if not issubclass(argument, types):
        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        args = string[string.find("(") + 1:-1].split(",")
        argument_name = args[0]
        raise TypeError(f"Argument {argument_name!r} must be a subclass of {types}, not {type(type(argument))}.")


def export(obj):
    """
    Marks an object for exporting into the public API.

    This decorator appends the object's name to the private module's __all__ list. The private module should
    then be imported in galois/__init__.py using from ._private_module import *. It also modifies the object's
    __module__ to "galois".
    """
    # Determine the private module that defined the object
    module = sys.modules[obj.__module__]

    # Set the object's module to the package name. This way the REPL will display the object
    # as galois.obj and not galois._private_module.obj
    obj.__module__ = "galois"

    # Append this object to the private module's "all" list
    public_members = getattr(module, "__all__", [])
    public_members.append(obj.__name__)
    setattr(module, "__all__", public_members)

    return obj


def extend_docstring(method, replace={}, docstring=""):  # pylint: disable=dangerous-default-value
    """
    A decorator to append the docstring of a `method` with the docstring the the decorated method.
    """
    def decorator(obj):
        parent_docstring = getattr(method, "__doc__", "")
        for from_str, to_str in replace.items():
            parent_docstring = parent_docstring.replace(from_str, to_str)
        obj.__doc__ = parent_docstring + "\n" + docstring

        return obj

    return decorator
