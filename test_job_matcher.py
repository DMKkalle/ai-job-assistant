from job_matcher import (
    calculate_match_percentage,
    classify_skills_by_evidence,
    compare_job_requirements,
    compare_skills,
)


def test_matches_skills_case_insensitively():
    candidate = {"skills": ["python", "GIT"]}
    job = {"skills": ["Python", "Git", "Docker"]}

    assert compare_skills(candidate, job) == {
        "matching_skills": ["Python", "Git"],
        "missing_skills": ["Docker"],
    }


def test_calculates_required_match_percentage():
    analysis = {
        "matching_skills": ["Python", "Git"],
        "missing_skills": ["Docker"],
    }

    assert calculate_match_percentage(analysis) == 67


def test_returns_none_when_job_has_no_requirements():
    assert (
        calculate_match_percentage({"matching_skills": [], "missing_skills": []})
        is None
    )


def test_classifies_matching_skills_by_evidence():
    candidate = {
        "evidence": {
            "Python": ["Built a tested Python project"],
            "Git": [],
        }
    }

    assert classify_skills_by_evidence(candidate, ["Python", "Git"]) == {
        "skills_with_evidence": ["Python"],
        "skills_without_evidence": ["Git"],
    }


def test_required_and_preferred_skills_are_separate():
    candidate = {"skills": ["Python", "Git"]}
    job = {
        "required_skills": ["Python", "Docker"],
        "preferred_skills": ["Git", "AWS"],
    }

    assert compare_job_requirements(candidate, job) == {
        "required": {
            "matching_skills": ["Python"],
            "missing_skills": ["Docker"],
        },
        "preferred": {
            "matching_skills": ["Git"],
            "missing_skills": ["AWS"],
        },
    }
