import math

def quadratic_equation(a, b, c):
    delta = b*b - 4*a*c
    if delta < 0:
        return "No solution!"
    x_1 = (-b + math.sqrt(delta)) / 2 / a
    x_2 = (-b - math.sqrt(delta)) / 2 / a
    return x_1, x_2

def Euclide_distance(x_0, y_0, x_1, y_1):
    return math.sqrt((x_0 - x_1)**2 + (y_0 - y_1)**2)

def defineLine(x_0, y_0, x_1, y_1):
    a = (y_0-y_1)/(x_0-x_1)
    b = y_0 - a*x_0
    return a, b

def line_circle_equation(a, b, m, n, r):
    A = 1 + a**2
    B = 2*(a*b - a*n - m)
    C = m**2 + (b-n)**2 - r**2
    return quadratic_equation(A, B, C)

def find_near_point(target_x, target_y, beacon_x, beacon_y, beacon_r):
    a, b = defineLine(target_x, target_y, beacon_x, beacon_y)
    x_1, x_2 = line_circle_equation(a, b, beacon_x, beacon_y, beacon_r)
    y_1 = a*x_1 + b
    y_2 = a*x_2 + b
    distance_1 = Euclide_distance(target_x, target_y, x_1, y_1)
    distance_2 = Euclide_distance(target_x, target_y, x_2, y_2)
    if distance_1 < distance_2:
        return x_1, y_1
    return x_2, y_2

def find_intersection_two_lines(a_1, b_1, a_2, b_2):
    x = (b_2-b_1)/(a_1-a_2)
    y = a_1*x + b_1
    return x, y

def find_radical_axis(x_0, y_0, r_0, x_1, y_1, r_1):
    a = (x_0 - x_1)/(y_1 - y_0)
    b = (x_0**2 + y_0**2 + r_1**2 - x_1**2 -y_1**2 - r_0**2)/2/(y_0 - y_1)
    return a, b
