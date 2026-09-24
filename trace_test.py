def calculate_total():
    total = 0

    for i in range(1, 4):
        total = total + i

    return total


result = calculate_total()

print("Result:", result)