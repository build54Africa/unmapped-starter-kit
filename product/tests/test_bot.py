import bot


def test_replies_with_matching_rows():
    reply = bot.answer("nairobi")
    assert "name: Example Clinic F" in reply and "name: Example Clinic G" in reply


def test_suggests_another_word_when_nothing_matches():
    assert bot.answer("zzzz").startswith("Nothing matched")


def test_shows_a_few_results_and_says_how_many_more():
    reply = bot.answer("example")
    assert reply.count("name: ") == bot.MAX_RESULTS
    assert reply.endswith("9 more matched. Add a word to narrow it down.")


def test_replies_never_exceed_telegrams_limit(monkeypatch):
    import pandas as pd

    wide = pd.DataFrame([{f"field{i}": "word " * 300 for i in range(20)} for _ in range(5)])
    monkeypatch.setattr(bot, "TABLE", wide)
    reply = bot.answer("word")
    assert len(reply) <= bot.TELEGRAM_LIMIT
    assert reply.endswith("2 more matched. Add a word to narrow it down.")
