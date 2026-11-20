"""
FastAPI Routes for AZ-900 Quiz Simulator and Error Log.
"""

from fastapi import APIRouter
from app.models.schemas import QuizSubmissionRequest, QuizSubmissionResponse
from app.services.quiz_service import quiz_service

router = APIRouter(prefix="/api/quiz", tags=["AZ-900 Quiz & Error Log"])

@router.get("/questions")
def get_exam_questions():
    questions = quiz_service.get_all_questions()
    # Mask answer index from public question fetch
    sanitized = []
    for q in questions:
        sanitized.append({
            "id": q.id,
            "domain": q.domain,
            "domain_weight": q.domain_weight,
            "subtopic": q.subtopic,
            "question": q.question,
            "options": q.options
        })
    return {"total": len(sanitized), "questions": sanitized}

@router.post("/submit", response_model=QuizSubmissionResponse)
def submit_exam(submission: QuizSubmissionRequest):
    return quiz_service.submit_quiz(submission)

@router.get("/error-log")
def get_curated_error_log():
    return {
        "candidate": "Dev Sehgal",
        "uid": "24BAI70484",
        "official_score": 971,
        "max_score": 1000,
        "error_log_entries": quiz_service.get_error_log()
    }

@router.get("/report-summary")
def get_internship_report_summary():
    return {
        "candidate": "Dev Sehgal",
        "uid": "24BAI70484",
        "degree": "Bachelor of Engineering in Computer Science and Engineering (Artificial Intelligence & Machine Learning)",
        "institution": "Chandigarh University, Gharuan",
        "internship_title": "Cloud Fundamentals with Microsoft Azure: A Hands-On Study of Cloud Concepts, Azure Architecture and Governance (AZ-900)",
        "dates": "01/06/2026 - 30/06/2026",
        "exam_date": "28 October 2026",
        "exam_result": {
            "score": 971,
            "passing_score": 700,
            "domain_scores": {
                "Describe cloud concepts": "95%",
                "Describe Azure architecture and services": "100%",
                "Describe Azure management and governance": "96%"
            }
        },
        "curriculum_weeks": [
            {"week": 1, "title": "Describe cloud concepts", "dates": "01/06/2026 - 05/06/2026"},
            {"week": 2, "title": "Azure architecture – core services", "dates": "08/06/2026 - 12/06/2026"},
            {"week": 3, "title": "Storage, migration, identity and security", "dates": "15/06/2026 - 19/06/2026"},
            {"week": 4, "title": "Management and governance", "dates": "22/06/2026 - 26/06/2026"},
            {"week": 5, "title": "Revision and consolidation", "dates": "29/06/2026 - 30/06/2026"}
        ]
    }
