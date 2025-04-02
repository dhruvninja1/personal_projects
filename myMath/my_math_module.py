import math



def is_whole(input):
    input_string = str(input)
    if "." in input_string:
        return False
    else:
        return True



def prime_factorize(input, p=False):
    list_of_p_factors = []
    total = input
    for x in range(2, input-1):
        while total % x == 0:
            if total != 1:
                list_of_p_factors.append(x)
                total = total/x
    if p:
        for x in range(0, len(list_of_p_factors)):
            print(list_of_p_factors[x], end=" ")
    return list_of_p_factors

def simplify_root(input):
    list = prime_factorize(input)
    doubles_list = list
    print(list)
    singles_list = []
    done = False
    while not done:
        for x in range(0, len(doubles_list), 2):
            if doubles_list[x] == doubles_list[x+1]:
                if x == len(doubles_list) - 2:
                    done = True
                continue

            else:
                singles_list.append(doubles_list[x])
                doubles_list.pop(x)
                singles_list.append(doubles_list[x])
                doubles_list.pop(x)
                break
    print(doubles_list)

simplify_root(120)




def abs(input):
    if input < 0:
        return input*-1
    elif input >= 0:
        return input
    



def factorial(input):
    total = 1
    for x in range(1, input+1):
        total *= x
    return total

def my_exponent(input, exponent):
    total = 1
    for x in range(0, exponent):
        total *= input
    return total

