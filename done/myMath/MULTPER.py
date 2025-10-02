def main():
    try:
        a, b, c = map(float, input("Enter 3 values: Base amount, percent, percent. No symbol: ").split())
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return

    b = b / 100
    c = c / 100

    v1 = a + (a * b)
    v2 = v1 + (v1 * c)

    v1_str = str(v1)  # Convert to string before printing
    v2_str = str(v2)  # Convert to string before printing


    print("Value 1 is " + v1_str) #Concatenate strings
    print("Value 2 is " + v2_str) #Concatenate strings

main()