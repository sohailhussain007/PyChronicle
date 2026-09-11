from ast_rewriter import analyze_code
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