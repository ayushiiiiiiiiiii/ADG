from abc import ABC, abstractmethod
from app.features.feature_schema import ExtractedFeatures

class BaseAnalyzer(ABC):
    """
    Abstract base class for all language-specific code analyzers.
    """
    
    @abstractmethod
    def analyze(self, code: str) -> ExtractedFeatures:
        """
        Parses the code, builds the AST, extracts features, 
        and returns an ExtractedFeatures object.
        """
        pass
