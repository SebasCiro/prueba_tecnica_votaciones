from sqlalchemy.orm import Session
from models import Voter, Candidate, Vote
from schemas import VoterCreate, CandidateCreate, VoteCreate, CandidateStats
from typing import List, Optional

# CRUD para Votantes
def create_voter(db: Session, voter: VoterCreate) -> Voter:
    """Crear un nuevo votante"""
    db_voter = Voter(name=voter.name, email=voter.email)
    db.add(db_voter)
    db.commit()
    db.refresh(db_voter)
    return db_voter

def get_voter(db: Session, voter_id: int) -> Optional[Voter]:
    """Obtener un votante por ID"""
    return db.query(Voter).filter(Voter.id == voter_id).first()

def get_voter_by_email(db: Session, email: str) -> Optional[Voter]:
    """Obtener un votante por email"""
    return db.query(Voter).filter(Voter.email == email).first()

def get_voters(db: Session, skip: int = 0, limit: int = 100) -> List[Voter]:
    """Obtener lista de votantes"""
    return db.query(Voter).offset(skip).limit(limit).all()

def delete_voter(db: Session, voter_id: int) -> bool:
    """Eliminar un votante"""
    db_voter = db.query(Voter).filter(Voter.id == voter_id).first()
    if db_voter:
        db.delete(db_voter)
        db.commit()
        return True
    return False

def update_voter_has_voted(db: Session, voter_id: int, has_voted: bool = True) -> Optional[Voter]:
    """Actualizar el estado de votación del votante"""
    db_voter = db.query(Voter).filter(Voter.id == voter_id).first()
    if db_voter:
        db_voter.has_voted = has_voted
        db.commit()
        db.refresh(db_voter)
        return db_voter
    return None

# CRUD para Candidatos
def create_candidate(db: Session, candidate: CandidateCreate) -> Candidate:
    """Crear un nuevo candidato"""
    db_candidate = Candidate(name=candidate.name, party=candidate.party)
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def get_candidate(db: Session, candidate_id: int) -> Optional[Candidate]:
    """Obtener un candidato por ID"""
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()

def get_candidates(db: Session, skip: int = 0, limit: int = 100) -> List[Candidate]:
    """Obtener lista de candidatos"""
    return db.query(Candidate).offset(skip).limit(limit).all()

def delete_candidate(db: Session, candidate_id: int) -> bool:
    """Eliminar un candidato"""
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if db_candidate:
        db.delete(db_candidate)
        db.commit()
        return True
    return False

def increment_candidate_votes(db: Session, candidate_id: int) -> Optional[Candidate]:
    """Incrementar el contador de votos de un candidato"""
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if db_candidate:
        db_candidate.votes += 1
        db.commit()
        db.refresh(db_candidate)
        return db_candidate
    return None

# CRUD para Votos
def create_vote(db: Session, vote: VoteCreate) -> Vote:
    """Crear un nuevo voto"""
    db_vote = Vote(voter_id=vote.voter_id, candidate_id=vote.candidate_id)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote

def get_votes(db: Session, skip: int = 0, limit: int = 100) -> List[Vote]:
    """Obtener lista de votos"""
    return db.query(Vote).offset(skip).limit(limit).all()

def get_vote_by_voter(db: Session, voter_id: int) -> Optional[Vote]:
    """Obtener el voto de un votante específico"""
    return db.query(Vote).filter(Vote.voter_id == voter_id).first()

# Funciones de Estadísticas
def get_total_votes(db: Session) -> int:
    """Obtener el total de votos emitidos"""
    return db.query(Vote).count()

def get_voters_who_voted(db: Session) -> int:
    """Obtener el número de votantes que ya han votado"""
    return db.query(Voter).filter(Voter.has_voted == True).count()

def get_candidates_with_vote_stats(db: Session) -> List[CandidateStats]:
    """Obtener estadísticas detalladas de votos por candidato"""

    # Obtener el total de votos emitidos
    total_votes = get_total_votes(db)

    # Obtener todos los candidatos
    candidates = db.query(Candidate).all()

    candidate_stats = []

    for candidate in candidates:
        # Contar votos para este candidato específico
        vote_count = db.query(Vote).filter(Vote.candidate_id == candidate.id).count()

        # Calcular porcentaje
        if total_votes > 0:
            percentage = (vote_count / total_votes) * 100
        else:
            percentage = 0

        # Crear estadística para este candidato
        candidate_stats.append(CandidateStats(
            candidate_name=candidate.name,
            total_votes=vote_count,
            percentage=round(percentage, 2)
        ))
    return candidate_stats