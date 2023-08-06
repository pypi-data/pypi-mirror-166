from google.cloud.webrisk_v1 import WebRiskServiceAsyncClient, SearchUrisRequest
from google.cloud.webrisk_v1.types import ThreatType

from safe_url_analyzers.analyzers.base import BaseAnalyzer
from safe_url_analyzers.models.analyzers.base import WebRiskAnalyzerResult


class WebRiskAnalyzer(BaseAnalyzer):
    """Check if a given URL is malicious using Web Risk API."""

    async def run(self, uri, threat_types=None):
        """
        :param uri: The URI to check.
        :param threat_types: A list of threat types to check.
        :return: A WebRiskAnalyzerResult object.
        """
        client = WebRiskServiceAsyncClient.from_service_account_json(self.credentials)
        if threat_types is None:
            threat_types = [ThreatType.MALWARE, ThreatType.SOCIAL_ENGINEERING, ThreatType.UNWANTED_SOFTWARE]
        request = SearchUrisRequest(uri=uri, threat_types=threat_types)
        resp = await client.search_uris(request)
        found_threats = resp.threat.threat_types

        threat_list = []
        if malicious := True if found_threats else False:
            threat_list = [f"webrisk.{threat.name}" for threat in found_threats]
        return WebRiskAnalyzerResult(observer="webrisk", malicious=malicious, threat_list=threat_list)
