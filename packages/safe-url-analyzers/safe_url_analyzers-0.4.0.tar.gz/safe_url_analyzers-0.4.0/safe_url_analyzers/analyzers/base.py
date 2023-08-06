from abc import ABCMeta
import os
from dataclasses import dataclass, asdict


class BaseAnalyzer(metaclass=ABCMeta):
    def __init__(self, *, api_key: str = None, credentials: str = None):
        self.api_key = api_key
        if not os.path.exists(credentials):
            raise FileNotFoundError(f"Credentials file not found: {credentials}")
        self.credentials = credentials


@dataclass
class BaseAnalyzerResult:
    """
    Base class for all analyzer results.
    """
    observer: str
    malicious: bool = False

    def serialize(self) -> dict:
        return asdict(self)
