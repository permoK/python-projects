def rental_car_cost(d):
    initial_cost = (d*40)
    
    if d >= 7:
        cost = initial_cost - 50
        return cost
    elif d >= 3:
        cost = initial_cost - 20
        return cost
    return initial_cost


print(rental_car_cost(5))
