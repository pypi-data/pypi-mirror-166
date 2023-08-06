from datetime import datetime
from typing import List

from pydantic import BaseModel


class BaseAnalyzerResult(BaseModel):
    """
    Base class for analyzer results.
    """
    observer: str
    malicious: bool = False


class WebRiskAnalyzerResult(BaseAnalyzerResult):
    """
    WebRisk analyzer result.
    """
    threat_list: List[str]


class UserReportAnalyzerResult(BaseAnalyzerResult):
    """
    WebRisk analyzer result.
    """
    is_user_reported: bool = True


class BaseResult(BaseModel):
    """
    Base class for all analyzers results.
    """
    url: str
    web_risk: WebRiskAnalyzerResult
    user_report: UserReportAnalyzerResult
    last_refresh: datetime = datetime.now()
    malicious: bool = False
    reasons: List[str] = []
