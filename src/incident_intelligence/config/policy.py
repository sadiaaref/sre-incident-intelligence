from dataclasses import dataclass

@dataclass(frozen=True)
class ScoringPolicy:
    critical_threshold: float = 80.0
    high_threshold: float = 60.0
    medium_threshold: float = 35.0
    change_window_minutes: int = 120
    known_pattern_threshold: float = 65.0
    max_history_matches: int = 5

    def priority(self, score: float) -> str:
        if score >= self.critical_threshold:
            return "CRITICAL"
        if score >= self.high_threshold:
            return "HIGH"
        if score >= self.medium_threshold:
            return "MEDIUM"
        return "LOW"
