def add(a, b):
    result = a + b
    return result


total = 0

for i in range(3):
    total = add(total, i)

print("Final Result:", total)