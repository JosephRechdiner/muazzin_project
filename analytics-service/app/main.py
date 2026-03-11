from shared.logger.logger import Logger
from app.analytics_config import AnalyticsConfig
from shared.elastic.elastic_client import ElasticManager
from app.dangerous_words_extractor import DangerousWordsExtractor
from shared.kafka.kafka_consumer import KafkaConsumer
from app.text_analyzer import TextAnalyzer
from app.analytics_handler import analyticsHandler


logger = Logger().get_logger(name="analytics-service")

def main():
    config = AnalyticsConfig(logger=logger)
    config.validate()

    es = ElasticManager(
        elastic_uri=config.elsatic_uri,
        index_name=config.index_name,
        logger=logger
    )

    consumer = KafkaConsumer(
        bootstrap_servers=config.bootstrap_servers,
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

    handler = analyticsHandler(
        analyze=analyzer.analyze,
        update_analyzed_info_in_elastic=es.update_analyzed_info,
        logger=logger
        )

    consumer.start(
        handler.handle_event
    )


if __name__ == "__main__":
    main()