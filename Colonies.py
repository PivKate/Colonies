import sqlite3
from Result_ import result_1, result_2

print("Calculation of results obtained with solid media according to ISO 7218")

conn = sqlite3.connect('microbedb.sqlite3')
cur = conn.cursor()
cur.executescript('''
DROP TABLE IF EXISTS Colonies;''')

choice = int(input("One plate per dilution(1) or two plates per dilution(2)?: "))
amount = int(input("Enter the number of samples: "))
if choice == 1:
    cur.executescript('''
        CREATE TABLE Colonies (
            id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            Colonies_first     INTEGER,
            Colonies_second    INTEGER,
            Result             INTEGER,
            Rounding_result    TEXT,
            Final_result       COMPLEX    
        );
        ''')
if choice == 2:
    cur.executescript('''
        CREATE TABLE Colonies (
            id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            Colonies_first1    INTEGER,
            Colonies_first2    INTEGER,
            Colonies_second1   INTEGER,
            Colonies_second2   INTEGER,
            Result             INTEGER,
            Rounding_result    TEXT,
            Final_result       COMPLEX    
        );
        ''')

for i in range(amount):

    # Method of calculation: general case.
    if choice == 1:
        colonies1 = int(input("Number of colonies on a plate of the first dilution: "))
        colonies2 = int(input("Number of colonies on a plate of the second dilution: "))
        d = float(input("First dilution retained for counting e.g. 0.01: "))
        v = float(input("Volume inoculated on each plate [ml]: "))

        # If the plate contains 10-300 colonies.
        # equation: N =sum colonies / V *1,1 *d.
        if 10 <= colonies1 < 300:
            c = colonies1 + colonies2
            m = v * d * 1.1
            N = float(c / m)
            x = round(N)
            print(x)

            # Rounding.
            print(result_1(x))
            d = result_1(x)

            # Result in correct form.
            print(result_2(d))

            # Entering data into the database.
            if i is None or i is not None:
                cur.execute('''
                    INSERT INTO Colonies (
                        Colonies_first,
                        Colonies_second,
                        Result,
                        Rounding_result,
                        Final_result) 
                    VALUES(?,?,?,?,?)''', (colonies1, colonies2, x, result_1(x), result_2(d)))
                conn.commit()

        # If the plate contains less than 10 colonies, but at least 4.
        elif 10 > colonies1 >= 4 and colonies2 == 0:
            m = v * d
            N = float(colonies1 / m)
            x = round(N)
            print(x)

            # Rounding.
            print(result_1(x))
            d = result_1(x)
            print(result_2(d))

            if i is None or i is not None:
                cur.execute('''
                    INSERT INTO Colonies (
                        Colonies_first,
                        Colonies_second,
                        Result,
                        Rounding_result,
                        Final_result) 
                    VALUES(?,?,?,?,?)''', (colonies1, colonies2, x, result_1(x), result_2(d)))
                conn.commit()

        # If the plate contains less than 4.
        elif colonies1 < 4 and colonies1 != 0:
            N = 4 / (v * d)
            x = int(N)
            res = "< {}".format(x)

            cur.execute('''
                INSERT INTO Colonies (
                    Colonies_first,
                    Colonies_second,
                    Result,
                    Rounding_result,
                    Final_result) 
                VALUES(?,?,?,?,?)''', (colonies1, colonies2, x, x, res))
            conn.commit()

        # If the plate contains no colonies.
        elif colonies1 == 0:
            N = 1 / (v * d)
            x = int(N)
            res = "< {}".format(x)

            cur.execute('''
                INSERT INTO Colonies (
                    Colonies_first,
                    Colonies_second,
                    Result,
                    Rounding_result,
                    Final_result) 
                VALUES(?,?,?,?,?)''', (colonies1, colonies2, x, x, res))
            conn.commit()
        else:
            print("Incorrect data")

    # Method of calculation: the case of two dishes.
    if choice == 2:
        colonies1, colonies2 = input(
            "Number of colonies on two plates of the first dilution, separate by a comma: ").split(",")
        colonies3, colonies4 = input(
            "Number of colonies on two plates of the second dilution, separate by a comma: ").split(",")
        d = float(input("First dilution retained for counting e.g.0.01: "))
        v = float(input("Volume inoculated on each plate [ml]: "))
        n1 = int(input("Number of plates counted from the first dilution selected: "))
        n2 = int(input("Number of plates counted from the second dilution selected: "))

        c1, c2, c3, c4 = int(colonies1), int(colonies2), int(colonies3), int(colonies4)

        # If the plate contains 10-300 colonies.
        # Equation: N = sum/v*d*[n1 + (0,1 * n2)].
        if all(10 <= x < 300 for x in [c1, c2]):
            c = c1 + c2 + c3 + c4
            denominator = float(v * d * (n1 + (0.1 * n2)))
            N = float(c / denominator)
            x = round(N)
            print(x)

            # Rounding.
            print(result_1(x))
            d = result_1(x)

            # Result in correct form.
            print(result_2(d))

            # Entering data into the database.
            if i is None or i is not None:
                cur.execute('''
                    INSERT INTO Colonies (
                        Colonies_first1,
                        Colonies_first2,
                        Colonies_second1,
                        Colonies_second2,
                        Result,
                        Rounding_result,
                        Final_result) 
                    VALUES(?,?,?,?,?,?,?)''', (colonies1, colonies2, colonies3, colonies4, x, result_1(x), result_2(d)))
                conn.commit()

        # If the plate contains less than 10 colonies, but at least 4.
        elif all(4 <= x < 10 for x in [c1, c2]) and all(x == 0 for x in [c3, c4]):
            # N=sum colonies/v*d*n.
            c = c1 + c2
            N = float(c / (v * d * n1))
            x = round(N)
            print(x)

            # Rounding.
            print(result_1(x))
            d = result_1(x)
            print(result_2(d))

            if i is None or i is not None:
                cur.execute('''
                    INSERT INTO Colonies (
                        Colonies_first1,
                        Colonies_first2,
                        Colonies_second1,
                        Colonies_second2,
                        Result,
                        Rounding_result,
                        Final_result) 
                    VALUES(?,?,?,?,?,?,?)''', (colonies1, colonies2, colonies3, colonies4, x, result_1(x), result_2(d)))
                conn.commit()

        # If the plate contains less than 4.
        elif all(x < 4 and x != 0 for x in [c1, c2]):
            N = 8 / (v * d * n1)
            x = int(N)
            res = "< {}".format(x)

            cur.execute('''
                INSERT INTO Colonies (
                    Colonies_first1,
                    Colonies_first2,
                    Colonies_second1,
                    Colonies_second2,
                    Result,
                    Rounding_result,
                    Final_result) 
                VALUES(?,?,?,?,?,?,?)''', (colonies1, colonies2, colonies3, colonies4, x, x, res))
            conn.commit()

        # If the plate contains no colonies.
        elif c1 == 0 and c2 == 0:
            N = 1 / (v * d)
            x = int(N)
            res = "< {}".format(x)

            cur.execute('''
                INSERT INTO Colonies (
                    Colonies_first1,
                    Colonies_first2,
                    Colonies_second1,
                    Colonies_second2,
                    Result,
                    Rounding_result,
                    Final_result) 
                    VALUES(?,?,?,?,?,?,?)''', (colonies1, colonies2, colonies3, colonies4, x, x, res))
            conn.commit()
        else:
            print("Incorrect data")
