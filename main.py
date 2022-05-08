from Func import *


def main():

    P = [Point(-5.0, 1), Point(-2, 2.1), Point(-7, 4), Point(-10, 2.1)]
    Q = [Point(16, 3), Point(23, 4), Point(22, 6), Point(16, 7), Point(10, 6), Point(11, 4)]

    # задаем направление и скорость точкам
    speed = 0.5
    for point in P:
      point.set_direction([Vector(speed * 1, 0), speed])
    for point in Q:
      point.set_direction([Vector(speed * -1, 0), speed])

    main_task(P, Q)


main()