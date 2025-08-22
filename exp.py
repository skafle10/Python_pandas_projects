


def checkig(cons, **var):

    if "name" and "country" in var:
        print(f"The shirt no. is: {cons}, name is {var["name"]} and the county is: {var["country"]} ")

checkig(10,name = "Messi", country = "Argentina" )

