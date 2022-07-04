import functools
import inspect
import warnings

def deprecated(message: str = None):
    """
    Decorator for classes or functions to mark them as deprecated.
    If the decorator is applied without a specific message (`@deprecated()`),
    the default warning is shown when using the function/class. To specify
    a custom message use it like:
        @deprecated('Don't use this function anymore!').

    Parameters
    ----------
    message : str, optional (default: None)
        Custom message to show with the DeprecationWarning.
    """

    def decorator(src):
        default_msg = f"GLDAS python " \
                      f"{'class' if inspect.isclass(src) else 'method'} " \
                      f"'{src.__module__}.{src.__name__}' " \
                      f"is deprecated and will be removed soon."

        @functools.wraps(src)
        def new_func(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)

            warnings.warn(
                default_msg if message is None else message,
                category=DeprecationWarning,
                stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return src(*args, **kwargs)

        return new_func

    return decorator
