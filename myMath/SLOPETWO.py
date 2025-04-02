def main():
    try:
        x1, y1, x2, y2 = map(float, input("Enter x1, y1, x2, y2: ").split())
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return

    if x1 - x2 == 0:
        slope = "Undefined"
    elif y1 - y2 == 0:
        slope = 0.0  # Make sure it's a float
    else:
        try:
            slope = (y1 - y2) / (x1 - x2)
        except ZeroDivisionError:  # Handle potential division by zero
            slope = "Undefined"

    slope_str = str(slope)  # Convert to string *before* printing
    print("Slope is " + slope_str)


main()