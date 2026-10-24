# from app.graph.edges import after_critic, fan_out

# OUTLINE = [{"id": "q1", "text": "a"}, {"id": "q2", "text": "b"}]


# def test_first_pass_fans_out_every_question():
#     assert len(fan_out({"outline": OUTLINE, "critique": []})) == 2


# def test_retry_only_weak_questions_with_followup_query():
#     crit = [{"question_id": "q1", "verdict": "supported"}, {"question_id": "q2", "verdict": "weak", "followup_query": "better"}]
#     sends = after_critic({"outline": OUTLINE, "critique": crit, "iteration": 1})
#     assert len(sends) == 1 and sends[0].arg["query"] == "better"


# def test_loop_stops_at_cap():
#     crit = [{"question_id": "q1", "verdict": "weak"}, {"question_id": "q2", "verdict": "supported"}]
#     assert after_critic({"outline": OUTLINE, "critique": crit, "iteration": 3}) == "writer"


# def test_all_supported_goes_to_writer():
#     crit = [{"question_id": "q1", "verdict": "supported"}, {"question_id": "q2", "verdict": "supported"}]
#     assert after_critic({"outline": OUTLINE, "critique": crit, "iteration": 1}) == "writer"


from app.graph.edges import after_critic, fan_out, search_query

OUTLINE = [{"id": "q1", "text": "a", "kind": "factual"}, {"id": "q2", "text": "b", "kind": "evaluative"}]


def test_first_pass_fans_out_every_question():
    assert len(fan_out({"outline": OUTLINE, "critique": []})) == 2


def test_evaluative_questions_get_evidence_terms():
    assert search_query(OUTLINE[0]) == "a"
    assert "systematic review" in search_query(OUTLINE[1])


def test_retry_only_weak_questions_with_followup_query():
    crit = [{"question_id": "q1", "verdict": "supported"}, {"question_id": "q2", "verdict": "weak", "followup_query": "better"}]
    sends = after_critic({"outline": OUTLINE, "critique": crit, "iteration": 1})
    assert len(sends) == 1 and sends[0].arg["query"] == "better"


def test_loop_stops_at_cap():
    crit = [{"question_id": "q1", "verdict": "weak"}, {"question_id": "q2", "verdict": "supported"}]
    assert after_critic({"outline": OUTLINE, "critique": crit, "iteration": 3}) == "writer"


def test_all_supported_goes_to_writer():
    crit = [{"question_id": "q1", "verdict": "supported"}, {"question_id": "q2", "verdict": "supported"}]
    assert after_critic({"outline": OUTLINE, "critique": crit, "iteration": 1}) == "writer"
