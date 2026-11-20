"""
Unit tests for AZ-900 Exam Simulator and Error Log.
"""

from app.models.schemas import QuizSubmissionRequest
from app.services.quiz_service import quiz_service

def test_question_bank_loaded():
    questions = quiz_service.get_all_questions()
    assert len(questions) >= 20
    # Ensure all 3 domains are represented
    domains = {q.domain for q in questions}
    assert "Describe cloud concepts" in domains
    assert "Describe Azure architecture and services" in domains
    assert "Describe Azure management and governance" in domains

def test_quiz_scoring_and_passing():
    questions = quiz_service.get_all_questions()
    # Perfect score submission
    perfect_answers = {q.id: q.answer_index for q in questions}
    res = quiz_service.submit_quiz(QuizSubmissionRequest(answers=perfect_answers))
    assert res.candidate_score == 1000
    assert res.passed is True
    assert res.correct_count == len(questions)
    assert len(res.incorrect_questions) == 0

def test_error_log_entries():
    error_log = quiz_service.get_error_log()
    assert len(error_log) >= 5
    topics = [item["topic"] for item in error_log]
    assert any("Governance" in t for t in topics)
    assert any("Networking" in t for t in topics)
