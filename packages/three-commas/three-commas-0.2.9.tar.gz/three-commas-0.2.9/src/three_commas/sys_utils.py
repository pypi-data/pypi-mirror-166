import sys
import inspect
import logging
import functools
from py3cw.request import Py3CW
from typing import Callable, Union, Tuple
import os
import hmac
import hashlib
from .model.generated_enums import Mode
from . import configuration
from .error import ThreeCommasApiError

logger = logging.getLogger(__name__)


def get_parent_function_name() -> str:
    """
    :return: The name of the function one level up the call stack where this function was called
    """
    try:
        return sys._getframe(2).f_code.co_name
    except ValueError as e:
        logger.exception('Error occurred while fetching the name of the parent')


def get_parent_module_name() -> str:
    """
    :return: The name of the module one level up the call stack
    """
    stack_frame = inspect.currentframe()
    while stack_frame:
        if stack_frame.f_code.co_name == '<module>':
            return stack_frame.f_globals['__name__']
        stack_frame = stack_frame.f_back


def blur_api_keys(initial_dict: dict):
    result = dict(initial_dict)
    if 'api_key' in result:
        result['api_key'] = f'{result.get("api_key")[:5]}...'
    if 'api_secret' in result:
        result['api_secret'] = f'{result.get("api_secret")[:5]}...'
    return result


def reduced_arg(arg):
    arg = str(arg)
    return arg if len(arg) < configuration.REDUCED_LOGGING_LIMIT else arg[:configuration.REDUCED_LOGGING_LIMIT] + '...'


def transform_args_kwargs_for_logging(args: tuple, kwargs: dict, reduce_long_arguments: bool):
    if reduce_long_arguments:
        logging_args = ', '.join([reduced_arg(a) for a in args])
        logging_kwargs = {k: reduced_arg(v) for k, v in kwargs}
    else:
        logging_args = args
        logging_kwargs = kwargs
    logging_kwargs = blur_api_keys(logging_kwargs)
    return logging_args, logging_kwargs


def logged(*logged_args,
           with_logger: logging.Logger = None,
           log_return: bool = False,
           reduce_long_arguments: bool = False):
    """
    :param logged_args:
    :param with_logger: Uses the passed logger to log.
    By default it will use the logger of the module where the annotation was called
    :param log_return: If True, will log the return after the execution of the function
    :param reduce_long_arguments: If True and the wrapping function is called with long arguments, the the log will be trimmed
    :return:
    """

    if with_logger is None:
        parent_module_name = get_parent_module_name()
        if parent_module_name is None:
            with_logger = logger
        else:
            with_logger = logging.getLogger(parent_module_name)

    def inner(function_to_wrap):
        @functools.wraps(function_to_wrap)
        def wrapper(*wrapper_args, **wrapper_kwargs):
            if not configuration.THREE_COMMAS_LOG_API:
                return function_to_wrap(*wrapper_args, **wrapper_kwargs)

            logging_args, logging_kwargs = transform_args_kwargs_for_logging(wrapper_args,
                                                                             wrapper_kwargs,
                                                                             reduce_long_arguments)
            with_logger.debug(f"Called '{function_to_wrap.__name__}' with args={logging_args}, kwargs={logging_kwargs}")

            try:
                ret = function_to_wrap(*wrapper_args, **wrapper_kwargs)
            except Exception as e:
                with_logger.debug(f"Function '{function_to_wrap.__name__}' raised an exception {repr(e)}")
                raise e

            if log_return:
                with_logger.debug(f"Function '{function_to_wrap.__name__}' was executed and returned: {ret}")
            else:
                with_logger.debug(f"Function '{function_to_wrap.__name__}' was executed")
            return ret
        return wrapper

    if len(logged_args) == 1 and callable(logged_args[0]):
        return inner(function_to_wrap=logged_args[0])
    return inner


class Py3cwClosure:
    def __init__(self,
                 py3cw: Py3CW,
                 additional_headers: dict = None):
        self.py3cw = py3cw
        self.additional_headers = additional_headers

    def request(self, *args, **kwargs) -> Tuple[dict, Union[dict, list]]:
        return self.py3cw.request(*args, **kwargs, additional_headers=self.additional_headers)


def with_py3cw(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args,
                forced_mode: Union[str, Mode] = None,
                additional_headers: dict = None,
                api_key: str = None,
                api_secret: str = None,
                request_options: dict = None,
                **kwargs):

        # request options
        request_options = request_options or dict()
        if request_options:
            logger.debug(f"Setting {request_options=}")

        # forced mode
        additional_headers = additional_headers or dict()
        additional_headers.update(get_forced_mode_headers(req_forced_mode=forced_mode))

        # py3cw
        py3cw = get_py3cw(req_api_key=api_key, req_api_secret=api_secret, request_options=request_options)

        # create buffer
        py3cw_closure = Py3cwClosure(additional_headers=additional_headers, py3cw=py3cw)

        inject_py3cw_into_function(func=func, wrapper=py3cw_closure)

        return func(*args, **kwargs)
    return wrapper


def inject_py3cw_into_function(func: Callable, wrapper: Union[Py3CW, Py3cwClosure]):
    func.__globals__['wrapper'] = wrapper


def get_forced_mode_headers(req_forced_mode: Union[str, Mode] = None) -> dict:
    # request forced mode has precedence over global forced mode
    forced_mode = req_forced_mode or os.getenv('THREE_COMMAS_FORCED_MODE')
    if forced_mode is None:
        return dict()

    if str(forced_mode).lower() == 'real':
        logger.debug(f"Forced mode is set to 'real'")
        return get_real_headers()
    elif str(forced_mode).lower() == 'paper':
        logger.debug(f"Forced mode is set to 'paper'")
        return get_paper_headers()
    else:
        logger.warning(f'{forced_mode=} is not known. Will not set.')
        return dict()


def get_py3cw(req_api_key: str = None, req_api_secret: str = None, request_options: dict = None) -> Py3CW:
    # request api keys has precedence over global api keys
    api_key = req_api_key or os.getenv("THREE_COMMAS_API_KEY")
    api_secret = req_api_secret or os.getenv("THREE_COMMAS_API_SECRET")
    if api_key is None or api_secret is None:
        raise RuntimeError("Please configure 'THREE_COMMAS_API_KEY' and 'THREE_COMMAS_API_SECRET'")
    return Py3CW(key=api_key, secret=api_secret, request_options=request_options)


def verify_no_error(error, data):
    calling_function_name = get_parent_function_name()
    if error:
        error['function_name'] = calling_function_name
        logger.error(error)
        raise ThreeCommasApiError(error=error)
    if data is None:
        logger.warning(f'No data was received for function {calling_function_name}')
        raise ThreeCommasApiError(error={'msg': 'Data is None', 'function_name': calling_function_name})


def create_signature(payload, api_secret):
    signature = hmac.new(bytes(api_secret, 'latin-1'),
                         msg=bytes(payload, 'latin-1'),
                         digestmod=hashlib.sha256).hexdigest()
    return signature


def get_paper_headers():
    return {'Forced-Mode': 'paper'}


def get_real_headers():
    return {'Forced-Mode': 'real'}
