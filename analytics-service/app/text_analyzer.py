from app.logger import Logger

class TextAnalyzer:
    def __init__(
            self,
            logger: Logger,
            less_dangerous_decoded_list: list[str],
            very_dangerous_decoded_list: list[str],
            threshold: int,
            ):
        self.less_dangerous_decoded_list = less_dangerous_decoded_list
        self.very_dangerous_decoded_list = very_dangerous_decoded_list
        self.logger = logger
        self.threshold = threshold

    def get_text_stats(self, text: str):
        stats = {}
        total_less_dangerous_words = 0
        total_very_dangerous_words = 0
        total_text_words = len(text.split(" "))
        rate = total_text_words
        for word in self.less_dangerous_decoded_list:
            if word in text:
                total_less_dangerous_words += 1
                rate -= total_text_words / 200
        for word in self.very_dangerous_decoded_list:
            if word in text:
                total_very_dangerous_words += 1
                rate -= total_text_words / 100

        stats["total_words"] = total_text_words
        stats["total_less_dangerous_words"] = total_less_dangerous_words
        stats["total_very_dangerous_words"] = total_very_dangerous_words
        stats["dangerous_rate"] = round((1 - rate / total_text_words) * 100, 2)
        return stats

    def bds_percent(self, stats: dict):
        return stats["dangerous_rate"]

    def is_bds(self, stats: dict):
        return True if stats["dangerous_rate"] > self.threshold else False

    def bds_threat_level(self, stats: dict):
        if stats["total_less_dangerous_words"] + stats["total_very_dangerous_words"] == 0:
            return "None"
        if 0 < stats["total_less_dangerous_words"] + stats["total_very_dangerous_words"] <= self.threshold:
            return "Meduim"
        else:
            return "High"
        
    def analyze(self, text):
        text_stats = self.get_text_stats(text)
        analyzed_info = {}
        analyzed_info["is_bds"] = self.is_bds(text_stats)
        analyzed_info["bds_threat_level"] = self.bds_threat_level(text_stats)
        analyzed_info["bds_percent"] = self.bds_percent(text_stats)
        return analyzed_info