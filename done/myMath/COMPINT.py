import math

def main():
    try:
        total, principal, rate, time = map(float, input("Enter total, principal, rate, time. No symbol. Enter 0 for the one you need to find: ").split())
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return

    rate = rate / 100  

    if total == 0:
        x = principal * (1 + rate)**time
    elif principal == 0:
        try:
            x = total / ((1 + rate)**time)
        except ZeroDivisionError:
            print("Cannot divide by zero.")
            return
    elif rate == 0:
        try:
            x = (total / principal)**(1 / time) - 1
        except ZeroDivisionError:
            print("Cannot calculate rate when time is 0.")
            return
        except ValueError:
            print("Cannot calculate rate when total/principal is a negative number.")
            return
    elif time == 0:
        try:
            x = math.log(total / principal) / math.log(1 + rate)
        except ZeroDivisionError:
            print("Cannot calculate time when rate is -1.")
            return
        except ValueError:
            print("Cannot calculate time when rate is -1 or total/principal is a negative number.")
            return
    else:
        print("You entered something incorrectly.")
        return

    if rate == 0:
        x_str = str(x * 100) + "%"
        print("Answer is " + x_str)
    elif time == 0:
        time_in_months = x * 12

main()