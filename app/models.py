from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from enum import Enum as PyEnum

from .database import Base

class BiasEnum(PyEnum):
    LEFT = "LEFT"
    LEAN_LEFT = "LEAN_LEFT"
    CENTER = "CENTER"
    LEAN_RIGHT = "LEAN_RIGHT"
    RIGHT = "RIGHT"
    UNKNOWN = "UNKNOWN"  # Optional fallback for models that return uncertain predictions

class NewsSource(Base):
    __tablename__ = "sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    url = Column(String)
    bias_label = Column(Enum(BiasEnum), nullable=False)

class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    summary = Column(Text)
    source_id = Column(UUID(as_uuid=True), ForeignKey('sources.id'))
    url = Column(String, unique=True)  # Still keep this unique if possible
    published_at = Column(DateTime, default=datetime.utcnow)

    unique_hash = Column(String, unique=True)  # ✅ Prevents duplication
    bias_label = Column(Enum(BiasEnum), default=BiasEnum.UNKNOWN)  # ✅ Article-specific bias

    cluster_id = Column(UUID(as_uuid=True), ForeignKey('clusters.id'), nullable=True)

    source = relationship("NewsSource")

    __table_args__ = (
        UniqueConstraint('unique_hash', name='uq_article_hash'),
    )

class Cluster(Base):
    __tablename__ = "clusters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_key = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
