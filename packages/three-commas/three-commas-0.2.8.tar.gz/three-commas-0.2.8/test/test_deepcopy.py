from src.three_commas.model import SmartTradeV2Entity


smart_trade_dict = {
    "id": 321435,
    "version": 2,
    "account": {
        "id": 12341235,
        "type": "paper_trading",
        "name": "Paper Account 112383",
        "market": "Paper trading account",
        "link": "/accounts/12345"
    },
    "pair": "BTC_ETH",
    "instant": False,
    "status": {
        "type": "waiting_targets",
        "basic_type": "waiting_targets",
        "title": "Waiting Targets"
    },
    "leverage": {
        "enabled": False
    },
    "position": {
        "type": "buy",
        "editable": False,
        "units": {
            "value": "0.9981",
            "editable": False
        },
        "price": {
            "value": "0.054366",
            "value_without_commission": "0.054312",
            "editable": False
        },
        "total": {
            "value": "0.05426302"
        },
        "order_type": "market",
        "status": {
            "type": "finished",
            "basic_type": "finished",
            "title": "Finished"
        }
    },
    "take_profit": {
        "enabled": False,
        "steps": []
    },
    "stop_loss": {
        "enabled": False
    },
    "reduce_funds": {
        "steps": []
    },
    "market_close": {},
    "note": "",
    "note_raw": None,
    "skip_enter_step": False,
    "data": {
        "editable": True,
        "current_price": {
            "day_change_percent": "0.356",
            "bid": "0.054624",
            "ask": "0.054625",
            "last": "0.054624",
            "quote_volume": "17066.13745793"
        },
        "target_price_type": "price",
        "base_order_finished": True,
        "missing_funds_to_close": 0,
        "liquidation_price": None,
        "average_enter_price": "0.054366",
        "average_close_price": None,
        "average_enter_price_without_commission": "0.054312",
        "average_close_price_without_commission": None,
        "panic_sell_available": True,
        "add_funds_available": True,
        "reduce_funds_available": True,
        "force_start_available": False,
        "force_process_available": True,
        "cancel_available": True,
        "finished": False,
        "base_position_step_finished": True,
        "entered_amount": "0.9981",
        "entered_total": "0.0542630160072",
        "closed_amount": "0.0",
        "closed_total": "0.0",
        "created_at": "2022-07-01T06:39:41.952Z",
        "updated_at": "2022-07-01T06:39:41.952Z",
        "type": "smart_trade"
    },
    "profit": {
        "volume": "0.0002026781784",
        "usd": "3.9697561412316",
        "percent": "0.37",
        "roe": None
    },
    "margin": {
        "amount": None,
        "total": None
    },
    "is_position_not_filled": False
}


def test_deepcopy():
    st_1 = SmartTradeV2Entity(smart_trade_dict)
    st_2 = SmartTradeV2Entity.deepcopy(st_1)
    assert st_1.account == st_2.account
    assert st_1.account is not st_2.account
