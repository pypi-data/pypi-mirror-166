from classification_model.preprocessing.data_manager import get_title


def test_get_title_with_array(get_titles):
    titles = [get_title(title) for title in get_titles]
    assert titles == ["Mrs", "Mr", "Miss", "Other", "Master"]
