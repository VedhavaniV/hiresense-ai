from __future__ import annotations

import re
from dataclasses import dataclass

from app.semantic_similarity import semantic_similarity_score
from app.skill_taxonomy import SKILL_TAXONOMY, all_skills


@dataclass(frozen=True)
class MatchReport:
    score: int
    skill_score: int
    semantic_score: int
    scoring_method: str
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skills: list[str]
    job_skills: list[str]
    roadmap: list[str]


def normalize_text(text: str) -> str:
    lowered = text.lower()
    return re.sub(r"\s+", " ", lowered).strip()


def extract_skills(text: str) -> list[str]:
    normalized = normalize_text(text)
    found = []

    for skill in all_skills():
        pattern = rf"(?<![a-z0-9+#]){re.escape(skill)}(?![a-z0-9+#])"
        if re.search(pattern, normalized):
            found.append(skill)

    return found


def build_learning_roadmap(missing_skills: list[str]) -> list[str]:
    if not missing_skills:
        return ["Strengthen project storytelling, metrics, deployment notes, and interview explanations."]

    roadmap = []
    for category, skills in SKILL_TAXONOMY.items():
        category_missing = [skill for skill in missing_skills if skill in skills]
        if category_missing:
            label = category.replace("_", " ").title()
            roadmap.append(f"{label}: practice {', '.join(category_missing[:4])}.")

    return roadmap


def analyze_match(resume_text: str, job_description: str) -> MatchReport:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)
    semantic_score = semantic_similarity_score(resume_text, job_description)

    if not job_skills:
        return MatchReport(
            score=semantic_score,
            skill_score=0,
            semantic_score=semantic_score,
            scoring_method="semantic_only_no_known_job_skills",
            matched_skills=[],
            missing_skills=[],
            resume_skills=resume_skills,
            job_skills=[],
            roadmap=["Add a detailed job description with required tools, responsibilities, and qualifications."],
        )

    matched = sorted(set(resume_skills).intersection(job_skills))
    missing = sorted(set(job_skills).difference(resume_skills))
    skill_score = round((len(matched) / len(set(job_skills))) * 100)
    overall_score = round((skill_score * 0.7) + (semantic_score * 0.3))

    return MatchReport(
        score=overall_score,
        skill_score=skill_score,
        semantic_score=semantic_score,
        scoring_method="hybrid_skill_overlap_70_semantic_30",
        matched_skills=matched,
        missing_skills=missing,
        resume_skills=resume_skills,
        job_skills=job_skills,
        roadmap=build_learning_roadmap(missing),
    )
