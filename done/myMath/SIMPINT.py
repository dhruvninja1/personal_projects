def main():
    try:
        total, principal, rate, time = map(float, input("Enter total, principal, rate, time. No symbol. Enter 0 for the one you need to find: ").split())
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return

    rate = rate / 100  # Divide the rate by 100

    if total == 0:
        x = principal * (1 + rate * time)
    elif principal == 0:
        try:
            x = total / (1 + rate * time)
        except ZeroDivisionError:
            print("Cannot divide by zero (1 + rate * time).")
            return
    elif rate == 0:
        try:
            x = (total - principal) / (principal * time)
        except ZeroDivisionError:
            print("Cannot divide by zero (principal * time).")
            return
    elif time == 0:
        try:
            x = (total - principal) / (principal * rate)
        except ZeroDivisionError:
            print("Cannot divide by zero (principal * rate).")
            return
    else:
        print("You entered something incorrectly.")
        return

    if rate == 0:
        x_str = str(x * 100) + "%"
        print("Answer is " + x_str)
    elif time == 0:
        time_in_months = x * 12
        x_years_str = str(x) + " years"
        time_in_months_str = str(time_in_months) + " months"
        print("Answer is " + x_years_str + " or " + time_in_months_str)
    else:
        x_str = str(x)
        print("Answer is " + x_str)

main()