from app.services.openai_service import review_code, generate_mock_comments

def test_mock_comments_generation():
    code_with_eval = "val = eval(input_str)"
    comments = generate_mock_comments(code_with_eval)
    assert len(comments) > 0
    assert any(c["severity"] == "critical" for c in comments)

def test_mock_comments_print():
    code_with_print = "print('Hello world')"
    comments = generate_mock_comments(code_with_print)
    assert len(comments) > 0
    assert any(c["severity"] == "info" for c in comments)

def test_review_code_fallback():
    # Calling review_code without an API key triggers fallback mock review
    response = review_code("print('test')")
    assert len(response.comments) > 0
    assert response.comments[0].severity == "info"
