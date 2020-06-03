def result_1(x):
    y = str(x)
    elements = list(y)
    lenght = len(elements)

    if lenght == 2:
        rb = x / 10
        return rb

    elif lenght == 3:
        rb = round(x, -1)
        return rb

    elif lenght == 4:
        rb = round(x, -2)
        return rb

    elif lenght == 5:
        rb = round(x, -3)
        return rb

    elif lenght == 6:
        rb = round(x, -4)
        return rb

    elif lenght == 7:
        rb = round(x, -5)
        return rb

    elif lenght == 8:
        rb = round(x, -6)
        return rb

    elif lenght == 9:
        rb = round(x, -7)
        return rb

    elif lenght == 10:
        rb = round(x, -8)
        return rb

    else:
        print("Incorrect data")


def result_2(x):
    y = str(x)
    elements = list(y)
    lenght = len(elements)

    if lenght == 2:
        ab = "{} x 10^{}".format(x, 1)
        return ab

    elif lenght == 3:
        ab = "{} x 10^{}".format((x / 1e2), 2)
        return ab

    elif lenght == 4:
        ab = "{} x 10^{}".format((x / 1e3), 3)
        return ab

    elif lenght == 5:
        ab = "{} x 10^{}".format((x / 1e4), 4)
        return ab

    elif lenght == 6:
        ab = "{} x 10^{}".format((x / 1e5), 5)
        return ab

    elif lenght == 7:
        ab = "{} x 10^{}".format((x / 1e6), 6)
        return ab

    elif lenght == 8:
        ab = "{} x 10^{}".format((x / 1e7), 7)
        return ab

    elif lenght == 9:
        ab = "{} x 10^{}".format((x / 1e8), 8)
        return ab

    elif lenght == 10:
        ab = "{} x 10^{}".format((x / 1e9), 9)
        return ab

    else:
        print("Incorrect data")
