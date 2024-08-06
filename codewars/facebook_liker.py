def likes(names):

    lenlist = len(names)

    others = lenlist - 2

    if others >= 2:
        return(f"{names[0]}, {names[1]} and {others} others like this")
    elif others == 1:
        return (f"{names[0]}, {names[1]} and {names[2]} like this")
    elif others == 0:
        return (f"{names[0]} and {names[1]} like this")
    elif others == -1:
        return (f"{names[0]} likes this")
    else:
        return f"no one likes this"

names = [] 

print(likes(names))
