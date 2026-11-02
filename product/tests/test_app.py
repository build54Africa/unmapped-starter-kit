from streamlit.testing.v1 import AppTest


def run_app():
    app = AppTest.from_file("../app.py", default_timeout=60)
    return app.run()


def test_the_app_shows_every_row_a_map_and_a_comparison():
    app = run_app()
    assert not app.exception
    assert app.title[0].value == "Clinic Finder"
    assert app.subheader[0].value == "12 of 12 rows"
    assert app.subheader[1].value == "Compare"
    assert [box.label for box in app.selectbox] == ["Number", "Grouped by"]


def test_search_and_filters_narrow_the_rows():
    app = run_app()
    app.text_input[0].input("kigali").run()
    assert app.subheader[0].value == "2 of 12 rows"
    app.text_input[0].input("").run()
    country = next(box for box in app.multiselect if box.label == "country")
    country.select("Nigeria").run()
    assert app.subheader[0].value == "5 of 12 rows"
