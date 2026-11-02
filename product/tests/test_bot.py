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
