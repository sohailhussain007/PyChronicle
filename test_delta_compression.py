from delta_compression import calculate_delta


def test_new_variable():
    previous_state = {}

    current_state = {
        "x": "10"
    }

    result = calculate_delta(previous_state, current_state)

    assert result == {
        "x": "10"
    }


def test_changed_variable():
    previous_state = {
        "x": "10"
    }

    current_state = {
        "x": "20"
    }

    result = calculate_delta(previous_state, current_state)

    assert result == {
        "x": "20"
    }


def test_unchanged_variable():
    previous_state = {
        "x": "10"
    }

    current_state = {
        "x": "10"
    }

    result = calculate_delta(previous_state, current_state)

    assert result == {}


def test_multiple_variables():
    previous_state = {
        "x": "10",
        "y": "20"
    }

    current_state = {
        "x": "10",
        "y": "30",
        "z": "40"
    }

    result = calculate_delta(previous_state, current_state)

    assert result == {
        "y": "30",
        "z": "40"
    }