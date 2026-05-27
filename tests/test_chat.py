from src.brain import detect_user_intent


def test_detect_intent():
    assert detect_user_intent('Thủ tục ly hôn là gì?') == 'legal_rag'
