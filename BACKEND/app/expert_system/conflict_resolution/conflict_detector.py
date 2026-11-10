class ConflictDetector:
    def __init__(self, activated_rules):
       
        self.activated_rules = activated_rules

    def detect_conflicts(self):
      
        conflict_groups = {}
        
        for rule in self.activated_rules:
            conclusion = rule.get("conclusion")
            if not conclusion:
                continue
                
            if conclusion not in conflict_groups:
                conflict_groups[conclusion] = []
            conflict_groups[conclusion].append(rule)
            
        return conflict_groups
