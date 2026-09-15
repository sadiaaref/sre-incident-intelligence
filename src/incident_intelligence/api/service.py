from ..engine.analyzer import IncidentAnalyzer
from ..domain.models import Incident

class IncidentIntelligenceService:
    def __init__(self, analyzer=None):
        self.analyzer = analyzer or IncidentAnalyzer()
    def analyze(self, incident: Incident):
        return self.analyzer.analyze(incident)
