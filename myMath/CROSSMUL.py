def main():
    try:
        a, b, c, d = map(float, input("Enter 4 values. Format: a/b = c/d. Enter 0 for the number you need to find. If doing percent of change, formula is P/100 = is/of: ").split())
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return

    if a == 0:
        try:
            a = (b * c) / d
            print(str(a))  # Convert to string before printing
        except ZeroDivisionError:
            print("Cannot divide by zero (d).")
            return
    elif b == 0:
        try:
            b = (a * d) / c
            print(str(b)) #Convert to string before printing
        except ZeroDivisionError:
            print("Cannot divide by zero (c).")
            return
    elif c == 0:
        try:
            c = (a * d) / b
            print(str(c)) #Convert to string before printing
        except ZeroDivisionError:
            print("Cannot divide by zero (b).")
            return
    elif d == 0:
        try:
            d = (b * c) / a
            print(str(d)) #Convert to string before printing
        except ZeroDivisionError:
            print("Cannot divide by zero (a).")
            return
    else:
        print("You entered something incorrectly.")
        return

main()