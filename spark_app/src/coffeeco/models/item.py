"""
Item Model

This module defines the Item data model.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    """Item data model"""

    item_id: str
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
