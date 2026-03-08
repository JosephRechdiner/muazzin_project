from app.logger import Logger
from app.analytics_config import AnalyticsConfig
from app.elastic_client import ElasticClient
from app.dangerous_words_extractor import DangerousWordsExtractor
from app.kafka_consumer import KafkaConsumer
from app.text_analyzer import TextAnalyzer


logger = Logger().get_logger()

def main():
    config = AnalyticsConfig(logger=logger)
    config.validate()

    es = ElasticClient(
        elastic_uri=config.elsatic_uri,
        index_name=config.index_name,
        logger=logger
    )

    consumer = KafkaConsumer(
        bootstrap_server=config.bootstrap_servers,
        listen_topic=config.listen_topic,
        group_id=config.group_id,
        logger=logger
    )

    words_extractor = DangerousWordsExtractor(logger=logger)

    less_dangerous_decoded_list = words_extractor.decode_text("/app/keys/less_dangerous.txt")
    very_dangerous_decoded_list = words_extractor.decode_text("/app/keys/very_dangerous.txt")

    analyzer = TextAnalyzer(
        logger=logger,
        less_dangerous_decoded_list=less_dangerous_decoded_list,
        very_dangerous_decoded_list=very_dangerous_decoded_list,
        threshold=5
    )

    consumer.start(
        analyze=analyzer.analyze,
        update_analyzed_info_in_elastic=es.update_analyzed_info
    )

if __name__ == "__main__":
    main()