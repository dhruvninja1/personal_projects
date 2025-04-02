import math as m

def main():
    hyp = float(input("Enter hypotenuse. 0 if unknown  "))
    bLeg = float(input("Enter bottom leg. 0 if unknown  "))
    tLeg = float(input("Enter top leg. 0 if unknown  "))
    bAngle = float(input("Enter bottom angle. 0 if unknown  "))
    tAngle = float(input("Enter top angle. 0 if unknown  "))

    round_decimals = 4

    if bLeg and tLeg:
            bAngle = round(m.degrees(m.atan(tLeg/bLeg)), round_decimals)
            tAngle = round(90-bAngle, round_decimals)
            hyp = round(m.sqrt(bLeg**2 + tLeg**2), round_decimals)

    elif hyp and tLeg:
            bLeg = round(m.sqrt(hyp**2 - tLeg**2), round_decimals)
            bAngle = round(m.degrees(m.atan(tLeg/bLeg)), round_decimals)
            tAngle = round(90-bAngle, round_decimals)

    elif hyp and bLeg:
            tLeg = round(m.sqrt(hyp**2 - bLeg**2), round_decimals)
            bAngle = round(m.degrees(m.atan(tLeg/bLeg)), round_decimals)
            tAngle = round(90-bAngle, round_decimals)

    elif hyp and bAngle:
            tAngle = round(90-bAngle, round_decimals)
            bLeg = round(hyp*(m.cos(m.radians(bAngle))))
            tLeg = round(hyp*(m.cos(m.radians(tAngle))))

    elif hyp and tAngle:
            bAngle = round(90-tAngle, round_decimals)
            bLeg = round(hyp*(m.cos(m.radians(bAngle))))
            tLeg = round(hyp*(m.cos(m.radians(tAngle))))

    elif bLeg and bAngle:
            tAngle = round(90-bAngle, round_decimals)
            tLeg = round(bLeg*(m.tan(m.radians(bAngle))), round_decimals)
            hyp = round(m.sqrt(tLeg**2 + bLeg**2), round_decimals)

    elif bLeg and tAngle:
            bAngle = round(90-tAngle, round_decimals)
            tLeg = round(bLeg*(m.tan(m.radians(bAngle))), round_decimals)
            hyp = round(m.sqrt(tLeg**2 + bLeg**2), round_decimals)

    elif tLeg and bAngle:
            tAngle = round(90-bAngle, round_decimals)
            bLeg = round(tLeg*(m.tan(m.radians(tAngle))), round_decimals)
            hyp = round(m.sqrt(tLeg**2 + bLeg**2), round_decimals)

    elif tLeg and tAngle:
            bAngle = round(90-tAngle, round_decimals)
            bLeg = round(tLeg*(m.tan(m.radians(tAngle))), round_decimals)
            hyp = round(m.sqrt(tLeg**2 + bLeg**2), round_decimals)
    else:
            print("nah bro")


    print("Hypotenuse: " + str(hyp))
    print("Bottom leg: " + str(bLeg))
    print("Top leg: " + str(tLeg))
    print("Bottom angle: " + str(bAngle))
    print("Top angle: " + str(tAngle))

main()