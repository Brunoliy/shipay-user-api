# pylint: disable=R0801,R0902
from __future__ import annotations

from sqlalchemy import Column, Integer

from interface_adapters.data.models.base import Model


class ClaimModel(Model):
    """Database representation for table user"""

    user_id = Column(Integer, Foreing_key="users.user_id")
    claim_id = Column(Integer, Foreing_key="claims.claim_id")


