# pylint: disable=R0801,R0902
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserClaim(Base):
    """Database representation for table user_claims"""

    __tablename__ = "user_claims"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), primary_key=True)

    # user and claim relationship
    user = relationship("User", back_populates="user_claims")
    claim = relationship("Claim", back_populates="user_claims")


class Claim(Base):
    """Database representation for table claims"""

    __tablename__ = "claims"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    active = Column(Integer, default=True)

    # user_claims relationship
    user_claims = relationship("UserClaim", back_populates="claim")


class Role(Base):
    """Database representation for table roles"""

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)

    # users relationship
    users = relationship("User", back_populates="role")


class User(Base):
    """Database representation for table users"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # roles relationship
    role = relationship("Role", back_populates="users")

    # user_claims relationship
    user_claims = relationship("UserClaim", back_populates="user")
