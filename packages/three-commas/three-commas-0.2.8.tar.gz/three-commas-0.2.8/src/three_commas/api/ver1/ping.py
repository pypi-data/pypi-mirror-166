from py3cw.request import Py3CW
from ...model import *
from ...error import ThreeCommasApiError
from typing import Tuple, List
import logging
from ...sys_utils import logged, with_py3cw, Py3cwClosure


logger = logging.getLogger(__name__)
wrapper: Py3cwClosure = None


''' This endpoint was not present in the py3cw module
@logged
@with_py3cw
def get(payload: dict = None):
    """
    GET /ver1/ping
    Test connectivity to the Rest API (Permission: NONE, Security: NONE)

    """
    error, data = wrapper.request(
        entity='<py3cw_entity>',
        action='<py3cw_action>',
        payload=payload,
    )
    return ThreeCommasApiError(error), data
'''


