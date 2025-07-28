from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import (
    VoterCreate, VoterResponse, CandidateCreate, CandidateResponse,
    VoteCreate, VoteResponse, VotingStats, HTTPError, SuccessMessage
)
import crud

router = APIRouter()

# ENDPOINTS PARA VOTANTES
@router.post(
    "/voters",
    response_model=VoterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo votante",
    description="Registra un nuevo votante en el sistema. El email debe ser único.",
    responses={
        201: {"description": "Votante registrado exitosamente"},
        400: {"model": HTTPError, "description": "Email ya registrado o datos inválidos"}
    },
    tags=["Votantes"]
)
def register_voter(
    voter: VoterCreate,
    db: Session = Depends(get_db)
):
    db_voter = crud.get_voter_by_email(db, email=voter.email)
    if db_voter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    return crud.create_voter(db=db, voter=voter)

@router.get(
    "/voters",
    response_model=List[VoterResponse],
    summary="Obtener la lista de votantes",
    description="Obtiene la lista completa de votantes registrados en el sistema.",
    responses={
        200: {"description": "Lista de votantes obtenida exitosamente"}
    },
    tags=["Votantes"]
)
def get_voters(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    voters = crud.get_voters(db, skip=skip, limit=limit)
    return voters

@router.get(
    "/voters/{voter_id}",
    response_model=VoterResponse,
    summary="Obtener detalles de un votante por ID",
    description="Obtiene los detalles completos de un votante específico usando su ID.",
    responses={
        200: {"description": "Detalles del votante obtenidos exitosamente"},
        404: {"model": HTTPError, "description": "Votante no encontrado"}
    },
    tags=["Votantes"]
)
def get_voter(
    voter_id: int,
    db: Session = Depends(get_db)
):
    db_voter = crud.get_voter(db, voter_id=voter_id)
    if db_voter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Votante no encontrado"
        )
    return db_voter

@router.delete(
    "/voters/{voter_id}",
    response_model=SuccessMessage,
    summary="Eliminar un votante",
    description="Elimina un votante del sistema usando su ID.",
    responses={
        200: {"description": "Votante eliminado exitosamente"},
        404: {"model": HTTPError, "description": "Votante no encontrado"}
    },
    tags=["Votantes"]
)
def delete_voter(
    voter_id: int,
    db: Session = Depends(get_db)
):
    success = crud.delete_voter(db, voter_id=voter_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Votante no encontrado"
        )
    return SuccessMessage(message="Votante eliminado exitosamente")

# ENDPOINTS PARA CANDIDATOS

@router.post(
    "/candidates",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo candidato",
    description="Registra un nuevo candidato en el sistema de votaciones.",
    responses={
        201: {"description": "Candidato registrado exitosamente"},
        400: {"model": HTTPError, "description": "Datos del candidato inválidos"}
    },
    tags=["Candidatos"]
)
def register_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db)
):
    return crud.create_candidate(db=db, candidate=candidate)

@router.get(
    "/candidates",
    response_model=List[CandidateResponse],
    summary="Obtener la lista de candidatos",
    description="Obtiene la lista completa de candidatos registrados en el sistema.",
    responses={
        200: {"description": "Lista de candidatos obtenida exitosamente"}
    },
    tags=["Candidatos"]
)
def get_candidates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    candidates = crud.get_candidates(db, skip=skip, limit=limit)
    return candidates

@router.get(
    "/candidates/{candidate_id}",
    response_model=CandidateResponse,
    summary="Obtener detalles de un candidato por ID",
    description="Obtiene los detalles completos de un candidato específico usando su ID.",
    responses={
        200: {"description": "Detalles del candidato obtenidos exitosamente"},
        404: {"model": HTTPError, "description": "Candidato no encontrado"}
    },
    tags=["Candidatos"]
)
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    db_candidate = crud.get_candidate(db, candidate_id=candidate_id)
    if db_candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidato no encontrado"
        )
    return db_candidate

@router.delete(
    "/candidates/{candidate_id}",
    response_model=SuccessMessage,
    summary="Eliminar un candidato",
    description="Elimina un candidato del sistema usando su ID.",
    responses={
        200: {"description": "Candidato eliminado exitosamente"},
        404: {"model": HTTPError, "description": "Candidato no encontrado"}
    },
    tags=["Candidatos"]
)
def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    success = crud.delete_candidate(db, candidate_id=candidate_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidato no encontrado"
        )
    return SuccessMessage(message="Candidato eliminado exitosamente")

# ENDPOINTS PARA VOTOS

@router.post(
    "/votes",
    response_model=VoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Emitir un voto",
    description="Permite a un votante emitir su voto por un candidato específico. Se debe registrar el voter_id y el candidate_id.",
    responses={
        201: {"description": "Voto emitido exitosamente"},
        400: {"model": HTTPError, "description": "El votante ya ha votado previamente o datos inválidos"},
        404: {"model": HTTPError, "description": "Votante o candidato no encontrado"}
    },
    tags=["Votos"]
)
def register_vote(
    vote: VoteCreate,
    db: Session = Depends(get_db)
):
    db_voter = crud.get_voter(db, voter_id=vote.voter_id)
    if not db_voter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Votante no encontrado"
        )

    if db_voter.has_voted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El votante ya ha emitido su voto"
        )

    db_candidate = crud.get_candidate(db, candidate_id=vote.candidate_id)
    if not db_candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidato no encontrado"
        )

    db_vote = crud.create_vote(db=db, vote=vote)
    crud.update_voter_has_voted(db, voter_id=vote.voter_id, has_voted=True)
    crud.increment_candidate_votes(db, candidate_id=vote.candidate_id)

    return db_vote

@router.get(
    "/votes",
    response_model=List[VoteResponse],
    summary="Obtener todos los votos emitidos",
    description="Obtiene la lista completa de todos los votos emitidos en el sistema.",
    responses={
        200: {"description": "Lista de votos obtenida exitosamente"}
    },
    tags=["Votos"]
)
def get_votes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    votes = crud.get_votes(db, skip=skip, limit=limit)
    return votes

# ENDPOINT PARA ESTADÍSTICAS

@router.get(
    "/votes/statistics",
    response_model=VotingStats,
    summary="Obtener estadísticas de la votación",
    description="Obtiene estadísticas completas de la votación incluyendo total de votos por candidato, porcentajes y total de votantes que han votado.",
    responses={
        200: {"description": "Estadísticas obtenidas exitosamente"}
    },
    tags=["Votos"]
)
def get_voting_statistics(db: Session = Depends(get_db)):
    candidates_stats = crud.get_candidates_with_vote_stats(db)
    voters_who_voted = crud.get_voters_who_voted(db)

    return VotingStats(
        candidates_stats=candidates_stats,
        total_voters_who_voted=voters_who_voted
    )