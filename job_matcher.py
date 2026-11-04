def compare_skills(candidate, job):
    matching_skills = []
    missing_skills = []
    candidate_skills_lower = [skill.strip().lower() for skill in candidate["skills"]]

    for required_skill in job["skills"]:
        if required_skill.strip().lower() in candidate_skills_lower:
            matching_skills.append(required_skill)
        else:
            missing_skills.append(required_skill)

    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
    }


def calculate_match_percentage(analysis):
    matching_count = len(analysis["matching_skills"])
    missing_count = len(analysis["missing_skills"])
    total_count = matching_count + missing_count

    if total_count == 0:
        return None

    return round(matching_count / total_count * 100)


def get_skill_evidence(candidate, skill):
    normalized_skill = skill.strip().lower()

    for evidence_skill, evidence_list in candidate["evidence"].items():
        if evidence_skill.strip().lower() == normalized_skill:
            return evidence_list

    return []


def classify_skills_by_evidence(candidate, skills):
    skills_with_evidence = []
    skills_without_evidence = []

    for skill in skills:
        if get_skill_evidence(candidate, skill):
            skills_with_evidence.append(skill)
        else:
            skills_without_evidence.append(skill)

    return {
        "skills_with_evidence": skills_with_evidence,
        "skills_without_evidence": skills_without_evidence,
    }


def find_uncertainties(evidence_classification):
    return [
        {"type": "missing_evidence", "skill": skill}
        for skill in evidence_classification["skills_without_evidence"]
    ]


def compare_job_requirements(candidate, job):
    required = compare_skills(candidate, {"skills": job["required_skills"]})
    preferred = compare_skills(candidate, {"skills": job["preferred_skills"]})
    return {"required": required, "preferred": preferred}
