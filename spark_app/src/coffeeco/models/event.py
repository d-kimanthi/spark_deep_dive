"""
Event Models

This module defines the Event data models and their hierarchy.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Base Event Classes


class Event:
    """Base event class"""

    pass


@dataclass
class BasicEvent(Event):
    """Basic event with timestamp, type, and label"""

    created: datetime
    event_type: str
    label: str


@dataclass
class CustomerEvent(BasicEvent):
    """Event associated with a customer"""

    customer_id: str


@dataclass
class RatingEvent(BasicEvent):
    """Event containing rating information"""

    rating: int
    rating_type: str
    store_id: Optional[str] = None
    item_id: Optional[str] = None


# Concrete Event Types


@dataclass
class BasicEventType(BasicEvent):
    """Basic event implementation"""

    def __init__(self, created: datetime, label: str, event_type: str = "BasicEvent"):
        self.created = created
        self.event_type = event_type
        self.label = label


@dataclass
class CustomerEventType(CustomerEvent):
    """Customer event implementation"""

    def __init__(
        self,
        created: datetime,
        customer_id: str,
        label: str,
        event_type: str = "CustomerEvent",
    ):
        self.created = created
        self.event_type = event_type
        self.label = label
        self.customer_id = customer_id


@dataclass
class RatingEventType(RatingEvent):
    """Rating event implementation"""

    def __init__(
        self,
        created: datetime,
        label: str,
        rating: int,
        rating_type: str,
        event_type: str = "RatingEvent",
        store_id: Optional[str] = None,
        item_id: Optional[str] = None,
    ):
        self.created = created
        self.event_type = event_type
        self.label = label
        self.rating = rating
        self.rating_type = rating_type
        self.store_id = store_id
        self.item_id = item_id


@dataclass
class CustomerRatingEventType:
    """Customer rating event - combines customer and rating information"""

    created: datetime
    event_type: str
    label: str
    customer_id: str
    rating: int
    rating_type: str
    store_id: Optional[str] = None
    item_id: Optional[str] = None

    def __init__(
        self,
        created: datetime,
        customer_id: str,
        label: str,
        rating: int,
        rating_type: str,
        event_type: str = "CustomerRatingEventType",
        store_id: Optional[str] = None,
        item_id: Optional[str] = None,
    ):
        self.created = created
        self.event_type = event_type
        self.label = label
        self.customer_id = customer_id
        self.rating = rating
        self.rating_type = rating_type
        self.store_id = store_id
        self.item_id = item_id
