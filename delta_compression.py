def calculate_delta(previous_state, current_state):
    """
    Return only variables whose values changed.
    """

    delta = {}

    for name, value in current_state.items():

        if name not in previous_state:
            delta[name] = value

        elif previous_state[name] != value:
            delta[name] = value

    return delta