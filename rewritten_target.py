x = 10
capture_state('x', x)
y = 20
capture_state('y', y)
z = x + y
capture_state('z', z)
x = 30
capture_state('x', x)
result = x + y
capture_state('result', result)