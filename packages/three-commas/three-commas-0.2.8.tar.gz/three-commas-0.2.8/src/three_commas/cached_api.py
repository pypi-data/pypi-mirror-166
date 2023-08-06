from . import api
from . import site
from cachetools import cached, TTLCache
from .model import *
from typing import List


@cached(cache=TTLCache(maxsize=1024, ttl=60))
def get_deals(*args, **kwargs) -> List[DealEntity]:
    return api.get_deals(*args, **kwargs)


@cached(cache=TTLCache(maxsize=1024, ttl=60))
def get_all_deals(*args, **kwargs) -> List[DealEntity]:
    return api.get_all_deals(*args, **kwargs)


@cached(cache=TTLCache(maxsize=1024, ttl=60*3))
def get_market_pairs(*args, **kwargs) -> List[str]:
    return api.get_market_pairs(*args, **kwargs)


@cached(cache=TTLCache(maxsize=1024, ttl=60*3))
def get_account(*args, **kwargs) -> AccountEntity:
    return api.get_account(*args, **kwargs)


@cached(cache=TTLCache(maxsize=1024, ttl=60*15))
def get_url_secret(bot_id: int) -> str:
    bot_model: Bot = api.get_bot(bot_id=bot_id)
    return bot_model.get_url_secret()


@cached(cache=TTLCache(maxsize=1024, ttl=60*60*24))
def get_bot_account_id(bot_id: int) -> int:
    bot_model: BotEntity = api.get_bot(bot_id=bot_id)
    return bot_model.get_account_id()


@cached(cache=TTLCache(maxsize=1024, ttl=60*3))
def get_bot_profit_line_chart_data(*args, **kwargs):
    return site.get_bot_profit_line_chart_data(*args, **kwargs)


@cached(cache=TTLCache(maxsize=1024, ttl=60))
def get_pie_chart_data(*args, **kwargs) -> List[dict]:
    return api.get_pie_chart_data(*args, **kwargs)
