from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CandidateInput(BaseModel):
    skills: list[str]
    evidence: dict[str, list[str]]


class JobInput(BaseModel):
    required_skills: list[str]
    preferred_skills: list[str]


class AnalysisRequest(BaseModel):
    candidate: CandidateInput
    job: JobInput


class SkillComparison(BaseModel):
    matching_skills: list[str]
    missing_skills: list[str]


class EvidenceClassification(BaseModel):
    skills_with_evidence: list[str]
    skills_without_evidence: list[str]


class Uncertainty(BaseModel):
    type: Literal["missing_evidence"]
    skill: str


class AnalysisResponse(BaseModel):
    required: SkillComparison
    preferred: SkillComparison
    required_match_percentage: int | None
    evidence: EvidenceClassification
    uncertainties: list[Uncertainty]


class JobCreate(BaseModel):
    title: str
    company: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)


class JobSkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    skill_type: Literal["required", "preferred"]


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: str
    skills: list[JobSkillResponse]


class RequirementDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    category: Literal[
        "technical_skill",
        "experience",
        "education",
        "language",
        "certification",
        "soft_skill",
        "domain_knowledge",
        "eligibility",
        "other",
    ]
    importance: Literal["required", "preferred", "unspecified"]
    details: str | None = None
    source_evidence: str


class JobDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    company: str | None = None
    locations: list[str] = Field(default_factory=list)
    work_mode: Literal["remote", "hybrid", "on_site", "unspecified"] = "unspecified"
    work_mode_details: str | None = None
    employment_type: Literal[
        "full_time",
        "part_time",
        "contract",
        "temporary",
        "internship",
        "unspecified",
    ] = "unspecified"
    seniority: Literal[
        "intern",
        "junior",
        "mid",
        "senior",
        "lead",
        "staff",
        "principal",
        "manager",
        "unspecified",
    ] = "unspecified"
    seniority_details: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    salary_period: Literal["hour", "month", "year", "unspecified"] | None = None
    salary_details: str | None = None
    company_description: str | None = None
    role_summary: str | None = None
    responsibilities: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    requirements: list[RequirementDraft] = Field(default_factory=list)
    benefits: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
