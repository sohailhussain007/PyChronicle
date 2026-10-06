from ast_rewriter import analyze_code,rewrite_source
def test_new_assignment():
    code = "x = 10"
    result = analyze_code(code)
    assert result == [
        {
            "variable_name": "x",
            "line_number": 1,
            "assignment_type": "new assignment"
        }
    ]
def test_variable_update():
    code = """x = 10
x = 20"""
    result = analyze_code(code)
    assert result == [
        {
            "variable_name": "x",
            "line_number": 1,
            "assignment_type": "new assignment"
        },
        {
            "variable_name": "x",
            "line_number": 2,
            "assignment_type": "update"
        }
    ]
def test_multiple_variables():
    code = """x = 10
y = 20
z = x + y"""
    result = analyze_code(code)
    assert len(result) == 3
    assert result[0]["variable_name"] == "x"
    assert result[1]["variable_name"] == "y"
    assert result[2]["variable_name"] == "z"
def test_assignment_line_numbers():
    code = """a = 5
b = 10
a = 15"""
    result = analyze_code(code)
    assert result[0]["line_number"] == 1
    assert result[1]["line_number"] == 2
    assert result[2]["line_number"] == 3
def test_tuple_assignment():
        code = "x, y = 10, 20"

        result = analyze_code(code)

        assert result == [
            {
                "variable_name": "x",
                "line_number": 1,
                "assignment_type": "new assignment"
            },
            {
                "variable_name": "y",
                "line_number": 1,
                "assignment_type": "new assignment"
            }
        ]
def test_list_assignment():
    code = "a, b, c = [1, 2, 3]"

    result = analyze_code(code)

    assert result == [
        {
            "variable_name": "a",
            "line_number": 1,
            "assignment_type": "new assignment"
        },
        {
            "variable_name": "b",
            "line_number": 1,
            "assignment_type": "new assignment"
        },
        {
            "variable_name": "c",
            "line_number": 1,
            "assignment_type": "new assignment"
        }
    ]
def test_assignment_inside_loop():
    code = """total = 0
for i in range(3):
    total = total + i"""
    result = analyze_code(code)
    assert result == [
        {
            "variable_name": "total",
            "line_number": 1,
            "assignment_type": "new assignment"
        },
        {
            "variable_name": "total",
            "line_number": 3,
            "assignment_type": "update"
        }
    ]
def test_assignment_inside_function():
    code = """def calculate():
    x = 10
    y = 20
    return x + y"""

    result = analyze_code(code)

    assert result == [
        {
            "variable_name": "x",
            "line_number": 2,
            "assignment_type": "new assignment"
        },
        {
            "variable_name": "y",
            "line_number": 3,
            "assignment_type": "new assignment"
        }
    ]
def test_rewrite_tuple_assignment():
    code = "x, y = 10, 20"
    result = rewrite_source(code)
    assert "capture_state('x', x)" in result
    assert "capture_state('y', y)" in result
def test_rewrite_assignment_inside_loop():
    code = """total = 0
for i in range(3):
    total = total + i"""
    result = rewrite_source(code)
    assert "capture_state('total', total)" in result
def test_rewrite_assignment_inside_function():
    code = """def calculate():
    x = 10
    y = 20
    return x + y"""
    result = rewrite_source(code)
    assert "capture_state('x', x)" in result
    assert "capture_state('y', y)" in result
def test_augmented_assignment():
    code = """x = 10
x += 5"""
    result = rewrite_source(code)
    assert "capture_state('x', x)" in result
def test_chained_assignment():
    code = "a = b = 10"
    result = rewrite_source(code)
    assert "capture_state('a', a)" in result
    assert "capture_state('b', b)" in result
