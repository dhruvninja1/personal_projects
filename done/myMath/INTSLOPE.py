a, b = map(float, input("Enter coefficient and constant: ").split())

def findXint(coeff, constant):
    if coeff == 0:
        if constant == 0:
            return 0  
        else:
            return "inf"  # Return "inf" as a string
    else:
        try:
            xint = -constant / coeff
            return xint
        except ZeroDivisionError:
            return "inf"

def findYint(constant):
    return constant

def findSlope(x, y):
    if x == 0:
        if y == 0: 
            return 0.0 
        else:
            return "inf"  # Return "inf" as a string
    else:
        try:
            slope = -y / x
            return slope
        except ZeroDivisionError: #Catch a zero division error
            return "inf"

xint = findXint(a, b)
yint = findYint(b)
slope = findSlope(xint, yint)

xint_str = str(xint) #Convert to string
yint_str = str(yint)
slope_str = str(slope)

print("X intercept is " + xint_str) #Concatenate strings
print("Y intercept is " + yint_str)

if xint == "inf" or slope == "inf":  # Check for "inf" string first
    print("Slope is Undefined")
elif xint == 0 and yint == 0:
    print("Slope is 0")
elif type(slope) == float and abs(slope) > 1e10:  # Check for VERY large float
    print("Slope is Undefined")
else:
    print("Slope is " + slope_str) #Concatenate strings