"""
Store Model

This module defines the Store data model.
"""

from dataclasses import dataclass


@dataclass
class Store:
    """Store data model"""

    store_id: str
    name: str
    address: str
    city: str
    state: str
    zip_code: str
