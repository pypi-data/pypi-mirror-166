import re
from typing import List
from dataclasses import dataclass
import logging
from .model.models import ThreeCommasDict

logger = logging.getLogger(__name__)


@dataclass
class BaseOrderToSmallErrorElement:
    amount: float = None
    pair: str = None


def cast_bool(func):
    def wrapped(*args, **kwargs):
        return bool(func(*args, **kwargs))
    return wrapped


class ThreeCommasApiError(ThreeCommasDict):
    BO_TO_SMALL_ERROR_PATTERN = re.compile(r"Base order size is too small\. Min: ([0-9.]*),? ?([\w_]+)?", re.IGNORECASE)
    NO_MARKET_PAIR_ERROR_PATTERN = re.compile(r"No market data for this pair: ([^\']*)\'", re.IGNORECASE)
    EXTRACT_PY3CW_MESSAGE_PATTERN = re.compile(r"Other error occurred: record_invalid Invalid parameters (\{.*\})\.", re.IGNORECASE)
    BOT_WAS_DELETED_ERROR_PATTERN = re.compile(r"Other error occurred: Not found None None", re.IGNORECASE)
    BOT_DID_NOT_EXISTED_OR_BELONGS_TO_OTHER_ACCOUNT_ERROR_PATTERN = re.compile(r"Other error occurred: not_found Not Found None", re.IGNORECASE)
    API_KEY_NOT_ENOUGH_PERMISSION_PATTERN = re.compile(r"access_denied Api key doesn't have enough permissions", re.IGNORECASE)
    API_KEY_INVALID_OR_EXPIRED_PATTERN = re.compile(r'api_key_invalid_or_expired Unauthorized. Invalid or expired api key', re.IGNORECASE)
    API_KEY_NOT_AUTHORIZED_FOR_THIS_ACTION_PATTERN = re.compile(r'key not authorized for this action', re.IGNORECASE)
    ACCOUNT_ALREADY_CONNECTED_PATTERN = re.compile(r'This account is already connected!', re.IGNORECASE)
    ACCOUNT_NOT_DELETABLE_PATTERN = re.compile(r"account_not_deletable Can't remove account.", re.IGNORECASE)

    @cast_bool
    def is_account_not_deletable_error(self) -> bool:
        if self.get_status_code() and self.get_status_code() != 422:
            return False
        return self._has_error_message() and self.ACCOUNT_NOT_DELETABLE_PATTERN.findall(self.get_msg())

    @cast_bool
    def is_account_already_connected_error(self) -> bool:
        return self._has_error_message() and self.ACCOUNT_ALREADY_CONNECTED_PATTERN.findall(self.get_msg())

    @cast_bool
    def is_api_key_not_authorized_for_this_action_error(self) -> bool:
        return self._has_error_message() and self.API_KEY_NOT_AUTHORIZED_FOR_THIS_ACTION_PATTERN.findall(self.get_msg())

    @cast_bool
    def is_api_key_has_no_permission_error(self) -> bool:
        return self._has_error_message() and self.API_KEY_NOT_ENOUGH_PERMISSION_PATTERN.findall(self.get_msg())

    @cast_bool
    def is_api_key_invalid_or_expired(self) -> bool:
        return self._has_error_message() and self.API_KEY_INVALID_OR_EXPIRED_PATTERN.findall(self.get_msg())

    @cast_bool
    def is_base_order_to_small_error(self) -> bool:
        return self._has_error_message() and self.BO_TO_SMALL_ERROR_PATTERN.findall(self.get_msg())

    @cast_bool
    def is_not_found_error(self) -> bool:
        return self._has_error_message() and 'not_found' in self.get_msg() or 'Not found' in self.get_msg()

    @cast_bool
    def is_no_market_pair_error(self) -> List[str]:
        return self._has_error_message() and self.NO_MARKET_PAIR_ERROR_PATTERN.findall(self.get_msg())

    def get_no_market_pair_error(self) -> List[str]:
        if self._has_error_message():
            pairs_to_remove = ThreeCommasApiError.NO_MARKET_PAIR_ERROR_PATTERN.findall(self.get_msg())
            if pairs_to_remove:
                return pairs_to_remove
        return list()

    def get_base_order_to_small_error(self) -> List[BaseOrderToSmallErrorElement]:
        ret = list()
        if self._has_error_message():
            try:
                match = ThreeCommasApiError.EXTRACT_PY3CW_MESSAGE_PATTERN.findall(self.get_msg())
                if match:
                    error_parsed = eval(match[0])
                else:
                    return list()
            except:
                return list()
            if error_parsed.get('base_order_volume'):
                for sub_message in error_parsed.get('base_order_volume'):
                    bo_min_match = ThreeCommasApiError.BO_TO_SMALL_ERROR_PATTERN.findall(sub_message)
                    if bo_min_match:
                        amount = float(bo_min_match[0][0])
                        pair = bo_min_match[0][1] or None
                        ret.append(BaseOrderToSmallErrorElement(amount=amount, pair=pair))
        return ret

    @cast_bool
    def _has_error_message(self) -> bool:
        return bool(self and self.get_msg())

    def get_msg(self) -> str:
        return self.get('msg')

    def get_status_code(self) -> int:
        return self.get('status_code', None)


class ThreeCommasException(RuntimeError):
    pass
