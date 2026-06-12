from __future__ import annotations

import re
from dataclasses import dataclass

from app.skill_taxonomy import SKILL_TAXONOMY, all_skills


@dataclass(frozen=True)
class MatchReport:
    score: int
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

    if not job_skills:
        return MatchReport(
            score=0,
            matched_skills=[],
            missing_skills=[],
            resume_skills=resume_skills,
            job_skills=[],
            roadmap=["Add a detailed job description with required tools, responsibilities, and qualifications."],
        )

    matched = sorted(set(resume_skills).intersection(job_skills))
    missing = sorted(set(job_skills).difference(resume_skills))
    score = round((len(matched) / len(set(job_skills))) * 100)

    return MatchReport(
        score=score,
        matched_skills=matched,
        missing_skills=missing,
        resume_skills=resume_skills,
        job_skills=job_skills,
        roadmap=build_learning_roadmap(missing),
    )

