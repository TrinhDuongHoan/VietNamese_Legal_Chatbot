from src.search import initialize_search_index, lexical_search


def test_lexical_search():
    initialize_search_index([{'question': 'ly hôn', 'content': 'thủ tục ly hôn thuận tình'}])
    results = lexical_search('ly hôn')
    assert len(results) >= 1
