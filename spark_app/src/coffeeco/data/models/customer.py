"""
Customer Model

This module defines the Customer data model and related structures.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Preferences:
    """Customer preferences"""

    customer_id: str
    preferences_id: str


@dataclass
class Membership:
    """Customer membership information"""

    customer_id: str
    membership_id: str
    since: datetime
    points: int  # customers collect points for purchases (rewards, etc)


@dataclass
class Customer:
    """Customer data model"""

    active: bool
    created: datetime
    customer_id: str
    first_name: str
    last_name: str
    email: str
    nickname: str
    membership: Optional[Membership] = None
    preferences: Optional[Preferences] = None
