from src.three_commas.model.generated_models import BotEntity
import json


def test_bot_events_are_parsed():
    filepath = 'test/sample_data/bots/btc/bot_show_with_events_btc.json'
    # filepath = './sample_data/bots/btc/bot_show_with_events_btc.json'
    with open(filepath, 'r+') as f:
        j: dict = json.loads(f.read())
        bot: BotEntity = BotEntity(j)
        # TODO
