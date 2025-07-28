from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Esquemas para Votantes
class VoterCreate(BaseModel):
    """Esquema para crear un nuevo votante"""
    name: str
    email: EmailStr

class VoterResponse(BaseModel):
    """Esquema de respuesta para votantes"""
    id: int = Field(..., description="ID único del votante")
    name: str = Field(..., description="Nombre completo del votante")
    email: EmailStr = Field(..., description="Correo electrónico del votante")
    has_voted: bool = Field(..., description="Indica si el votante ya ha votado")

    class Config:
        from_attributes = True

# Esquemas para Candidatos
class CandidateCreate(BaseModel):
    """Esquema para crear un nuevo candidato"""
    name: str
    party: Optional[str] = None

class CandidateResponse(BaseModel):
    """Esquema de respuesta para candidatos"""
    id: int = Field(..., description="ID único del candidato")
    name: str = Field(..., description="Nombre completo del candidato")
    party: Optional[str] = Field(None, description="Partido político del candidato")
    votes: int = Field(..., description="Número de votos recibidos")

    class Config:
        from_attributes = True

# Esquemas para Votos
class VoteCreate(BaseModel):
    """Esquema para emitir un nuevo voto"""
    voter_id: int = Field(..., description="ID del votante")
    candidate_id: int = Field(..., description="ID del candidato seleccionado")

class VoteResponse(BaseModel):
    """Esquema de respuesta para votos"""
    id: int = Field(..., description="ID único del voto")
    voter_id: int = Field(..., description="ID del votante")
    candidate_id: int = Field(..., description="ID del candidato")

    class Config:
        from_attributes = True

# Esquemas para Estadísticas
class CandidateStats(BaseModel):
    """Estadísticas por candidato"""
    candidate_name: str = Field(..., description="Nombre del candidato")
    total_votes: int = Field(..., description="Total de votos recibidos")
    percentage: float = Field(..., description="Porcentaje de votos obtenidos")

class VotingStats(BaseModel):
    """Estadísticas generales de la votación"""
    candidates_stats: list[CandidateStats]
    total_voters_who_voted: int = Field(..., description="Número de votantes que han votado")

# Esquemas de respuesta HTTP
class HTTPError(BaseModel):
    """Esquema para errores HTTP"""
    detail: str = Field(..., description="Descripción del error")

class SuccessMessage(BaseModel):
    """Esquema para mensajes de éxito"""
    message: str = Field(..., description="Mensaje de éxito")
    data: Optional[dict] = Field(None, description="Datos adicionales opcionales")