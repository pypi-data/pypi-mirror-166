from generic_crawler.core import GenericCrawler, ActionReader
from generic_crawler.config import Config

from dotenv import load_dotenv
load_dotenv()


config = Config(token="access_token_from_dotenv_file", endpoint_url="endpoint_url_from_dotenv_file")

crawler = GenericCrawler(config=config)
reader = ActionReader(path_to_yaml="tests/actions/test_ismail_feedbacks.yml")


#reader.action["steps"][0]["duration"] = 20

data, _ = crawler.retrieve(reader.action)

print("ok")
