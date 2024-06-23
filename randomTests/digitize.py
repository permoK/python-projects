"""
Convert number to reversed array of digits

Given a random non-negative number, you have to return the digits of this number within an array in reverse order.
Example(Input => Output):

35231 => [1,3,2,5,3]
0 => [0]

"""

def digitize(n):
    p = list(str(n))
    y = []
    length_of_p = len(p)   
    for i in range(0, length_of_p):
        x = (int(p[length_of_p - 1 - i]))
        y.append(x)
    return y

n = 123
print(digitize(n))
