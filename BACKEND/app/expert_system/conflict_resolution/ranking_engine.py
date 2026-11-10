class RankingEngine:
    def __init__(self, resolved_rules):
        self.resolved_rules = resolved_rules

    def rank_careers(self):
        sorted_results = sorted(
            self.resolved_rules,
            key=lambda x: (x.get("confidence", 0.0), x.get("priority", 0)),
            reverse=True
        )

        ranked_list = []
        for index, item in enumerate(sorted_results, start=1):
            ranked_list.append({
                "rank": index,
                "career": item.get("conclusion"),
                "confidence": item.get("confidence", 0.0),
                "priority": item.get("priority", 0),
                "reason": item.get("description", "Đề xuất phù hợp dựa trên năng lực, sở thích và định hướng của học sinh THPT.")
            })

        return ranked_list
