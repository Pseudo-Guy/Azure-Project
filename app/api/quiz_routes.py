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
        "candidate": "Arighna Sadhu",
        "uid": "24BAI70500",
        "official_score": 942,
        "max_score": 1000,
        "error_log_entries": quiz_service.get_error_log()
    }

@router.get("/report-summary")
def get_internship_report_summary():
    return {
        "candidate": "Arighna Sadhu",
        "uid": "24BAI70500",
        "degree": "Bachelor of Engineering in Computer Science and Engineering (Artificial Intelligence and Machine Learning)",
        "institution": "Chandigarh University, Gharuan",
        "internship_title": "Cloud Fundamentals on Microsoft Azure: Industrial Internship Training and AZ-900 Certification",
        "dates": "01/06/2026 - 26/06/2026",
        "exam_date": "28 October 2026",
        "exam_result": {
            "registration_id": "ITS-51811871",
            "exam_reference": "53209596",
            "score": 942,
            "passing_score": 700,
            "domain_scores": {
                "Describe cloud concepts": "90%",
                "Describe Azure architecture and services": "96%",
                "Describe Azure management and governance": "96%"
            }
        },
        "curriculum_weeks": [
            {"week": 1, "title": "Cloud concepts and Azure global infrastructure", "dates": "01/06/2026 - 05/06/2026"},
            {"week": 2, "title": "Resource organisation, compute and networking", "dates": "08/06/2026 - 12/06/2026"},
            {"week": 3, "title": "Storage, databases, identity and security", "dates": "15/06/2026 - 19/06/2026"},
            {"week": 4, "title": "Cost management, governance, management tools and monitoring", "dates": "22/06/2026 - 26/06/2026"}
        ]
    }
