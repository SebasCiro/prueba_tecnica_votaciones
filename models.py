from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Voter(Base):
    __tablename__ = "voters"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    has_voted = Column(Boolean, default=False, nullable=False)
    # Relación con votos
    votes = relationship("Vote", back_populates="voter")

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    party = Column(String(255), nullable=True)
    votes = Column(Integer, default=0, nullable=False)
    # Relación con votos
    received_votes = relationship("Vote", back_populates="candidate")

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    voter_id = Column(Integer, ForeignKey("voters.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    # Relaciones
    voter = relationship("Voter", back_populates="votes")
    candidate = relationship("Candidate", back_populates="received_votes")