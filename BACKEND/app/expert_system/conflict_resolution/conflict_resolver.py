class ConflictResolver:
    def __init__(self, conflict_groups):
       
        self.conflict_groups = conflict_groups

    def resolve(self):
        
        resolved_rules = []

        for conclusion, rules in self.conflict_groups.items():
            if not rules:
                continue
            
           
            best_rule = max(
                rules, 
                key=lambda r: (r.get("confidence", 0.0), r.get("priority", 0))
            )
            resolved_rules.append(best_rule)

        return resolved_rules
