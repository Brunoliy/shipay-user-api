# pylint: disable=R0801,R0902
from __future__ import annotations

from sqlalchemy import Column, Integer, String

from interface_adapters.data.models.base import Model


class ClaimModel(Model):
    """Database representation for table user"""

    claim_id = Column(Integer, primary_key=True, index=True)
    claim_description = Column(String)
    is_active = Column(bool)


