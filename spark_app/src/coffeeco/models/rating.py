"""
Rating Model

This module defines the Rating data model.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Rating:
    """Rating data model"""

    created: datetime
    customer_id: str
    score: int
    item: Optional[str] = None
    store: Optional[str] = None
