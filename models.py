from dataclasses import dataclass
from typing import List

@dataclass
class Threat:
    id: str
    title: str
    category: str
    description: str
    mitigations: List[str]
    cvss_rating: float
    severity: str
