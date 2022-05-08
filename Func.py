from Vector import Vector
from Point import Point
from time import sleep
import matplotlib.pyplot as plt
from celluloid import Camera


def get_intersection_point(p1, p2, p3, p4):
    # p = p3 + t*(p4 - p3)
    n = Vector(-(p2.y - p1.y), p2.x - p1.x)
    t = (Vector.scalar_product(n, Vector(p3, p1))) / (Vector.scalar_product(n, Vector(p3, p4)))
    p = Vector(p3, p4)
    return Point(p3.x + t * p.x, p3.y + t * p.y)


def is_intersect(p1, p2, p3, p4):
    d1 = determinant(p3, p4, p3, p1)
    d2 = determinant(p3, p4, p3, p2)
    d3 = determinant(p1, p2, p1, p3)
    d4 = determinant(p1, p2, p1, p4)
    if d1 == d2 == d3 == d4 == 0:
        c1 = Vector.scalar_product(Vector(p1, p3), Vector(p1, p4))
        c2 = Vector.scalar_product(Vector(p2, p3), Vector(p2, p4))
        c3 = Vector.scalar_product(Vector(p3, p1), Vector(p3, p2))
        c4 = Vector.scalar_product(Vector(p4, p1), Vector(p4, p2))
        if c1 < 0 or c2 < 0 or c3 < 0 or c4 < 0:
            return True
        else:
            return False
    elif d1 * d2 <= 0 and d3 * d4 <= 0:
        return True
    else:
        return False


def next(i, n):
    return (i + 1) % n


def determinant(p1, p2, p3, p4):
    a = p2.x - p1.x
    b = p2.y - p1.y
    c = p4.x - p3.x
    d = p4.y - p3.y
    return a * d - b * c


def det(p, p1, p2):  # p относительно p1p2
    return (p2.x - p1.x) * (p.y - p1.y) - (p.x - p1.x) * (p2.y - p1.y)


def check_point_position(p1, p2, p0):
    det = determinant(p1, p2, p1, p0)
    if det > 0:  # left
        return 1
    elif det < 0:
        return -1  # right
    else:
        return 0  # on


def is_aimed(a1, a2, b1, b2):
    are_collinear = check_point_position(b1, b2, a1) == 0 and check_point_position(b1, b2, a2) == 0

    if are_collinear:
        # если a1a2 и b1b2 не пересекаются и a2, b1 по одну сторону от a1 - нацелен
        if (not is_intersect(a1, a2, b1, b2)) and ((a2.x - a1.x) * (b1.x - a1.x) + (a2.y - a1.y) * (b1.y - a1.y) > 0):
            return True
    else:
        if determinant(b1, b2, a1, a2) < 0 and determinant(b1, b2, b1, a2) > 0:
            return True
        elif determinant(b1, b2, a1, a2) > 0 and determinant(b1, b2, b1, a2) < 0:
            return True
    return False


def is_external(a1, a2, b1, b2):
    if check_point_position(b1, b2, a2) < 0:  # справа
        return True
    return False


def polygon_intersection(P, Q):
    n = len(P)
    m = len(Q)
    Res = []  # массив точек пересечения

    p = 0  # "окно" для движения по первому многоугольнику
    q = 0  # "окно" для движения по второму многоугольнику

    # фиксируем окно q из второго многоугольника и для него подбираем окно p из первого многоугольника
    for i in range(0, n):
        # справа
        if check_point_position(P[i], P[next(i, n)], Q[0]) < 0 or check_point_position(Q[0], Q[1], P[next(i, n)]) < 0:
            p = i
            break

    # следующие точки
    p_next = next(p, n)
    q_next = next(q, m)

    # цикл по точкам многоугольника
    for i in range(0, 2 * (n + m)):

        # 1. если окна нацелены друг на друга
        if is_aimed(P[p], P[p_next], Q[q], Q[q_next]) and is_aimed(Q[q], Q[q_next], P[p], P[p_next]):
            # двигаем внешнее окно
            if is_external(P[p], P[p_next], Q[q], Q[q_next]):
                p = p_next
                p_next = next(p, n)
            else:
                q = q_next
                q_next = next(q, m)

        # 2. если p нацелен на q, а q на p не нацелен
        elif is_aimed(P[p], P[p_next], Q[q], Q[q_next]) and not is_aimed(Q[q], Q[q_next], P[p], P[p_next]):
            # если p - внешнее окно, то добавляем конечную вершину в ответ
            if not is_external(P[p], P[p_next], Q[q], Q[q_next]):
                Res.append(P[p_next])
            # двигаем окно p
            p = p_next
            p_next = next(p, n)

        # 3. если q нацелен на p, а p на q не нацелен
        elif not is_aimed(P[p], P[p_next], Q[q], Q[q_next]) and is_aimed(Q[q], Q[q_next], P[p], P[p_next]):
            # если q - внешнее окно, то добавляем конечную вершину в ответ
            if not is_external(Q[q], Q[q_next], P[p], P[p_next]):
                Res.append(Q[q_next])
            # двигаем окно q
            q = q_next
            q_next = next(q, m)

        # 4. если окна не нацелены друг на друга
        elif not is_aimed(P[p], P[p_next], Q[q], Q[q_next]) and not is_aimed(Q[q], Q[q_next], P[p], P[p_next]):
            # если окна пересекаются, то добавляем точку пересечения в ответ
            if is_intersect(P[p], P[p_next], Q[q], Q[q_next]):
                Res.append(get_intersection_point(P[p], P[p_next], Q[q], Q[q_next]))
            # двигаем внешнее окно
            if is_external(P[p], P[p_next], Q[q], Q[q_next]):
                p = p_next
                p_next = next(p, n)
            else:
                q = q_next
                q_next = next(q, m)

        # если первая добавленная точка совпала с последней - выход
        if len(Res) > 1 and Res[0] == Res[-1]:
            del Res[-1]
            break

    return Res


def get_intersection_parameter(segment, p1, p2):
    n = Vector(-(p2.y - p1.y), p2.x - p1.x)
    return Vector.scalar_product(n, Vector(segment[0], p1)) / Vector.scalar_product(n, Vector(segment[0], segment[1]))


def get_intersection_type(p1, p2, segment):
    normal_vector = Vector(p2.y - p1.y, -(p2.x - p1.x))
    segment_vector = Vector(segment[1].x - segment[0].x, segment[1].y - segment[0].y)

    if Vector.scalar_product(segment_vector, normal_vector) > 0:
        return 1  # п покид
    elif Vector.scalar_product(segment_vector, normal_vector) < 0:
        return -1  # п вход
    else:
        return 0


def cyrus_beck(segment, polygon_points):
    t0_values = [0]
    t1_values = [1]
    n = len(polygon_points)

    for i in range(n):
        intersection_type = get_intersection_type(polygon_points[i], polygon_points[next(i, n)], segment)
        t = get_intersection_parameter(segment, polygon_points[i],
                                       polygon_points[next(i, n)])  # параметр точки пересечения
        if intersection_type == -1:
            t0_values.append(t)
        elif intersection_type == 1:
            t1_values.append(t)
        else:
            continue

    t0 = max(t0_values)
    t1 = min(t1_values)

    if t0 <= t1:
        x1 = segment[0].x + (segment[1].x - segment[0].x) * t0  # xA + (xB-xA)*t0
        x2 = segment[0].x + (segment[1].x - segment[0].x) * t1
        y1 = segment[0].y + (segment[1].y - segment[0].y) * t0
        y2 = segment[0].y + (segment[1].y - segment[0].y) * t1
        return Point(x1, y1), Point(x2, y2)
    else:
        return segment[0], segment[0]  # если пустое множество, то возвращаем две совпадающие точки


def main_task(P, Q):
    fig, ax = plt.subplots()
    camera = Camera(fig)
    plt.ion()

    count = 50
    for k in range(0, count):
        # рисуем многоугольники
        draw_polygon(P)
        draw_polygon(Q)
        ax.fill(list(map(lambda p: p.x, P)), list(map(lambda p: p.y, P)), "yellow")
        ax.fill(list(map(lambda p: p.x, Q)), list(map(lambda p: p.y, Q)), "orange")

        res = polygon_intersection(P, Q)  # массив точек пересечения многоугольников
        ax.fill(list(map(lambda p: p.x, res)), list(map(lambda p: p.y, res)), "red")

        p0_new, p2_new = cyrus_beck([P[0], P[2]], Q)  # концевые точки отсечения отрезка Р0Р2
        draw_line([p0_new, p2_new], "black")

        # делаем шаг анимации
        camera.snap()
        # двигаем многоугольники
        for p1 in P:
            p1.move()
        for p2 in Q:
            p2.move()

        plt.draw()
        plt.gcf().canvas.flush_events()
        sleep(0.00001)

    # сохраняем анимацию
    animation = camera.animate()
    animation.save('animation.gif')
    plt.ioff()
    plt.show()


def draw_polygon(points):
    n = len(points)
    for i in range(0, n - 1):
        plt.plot([points[i].x, points[i + 1].x], [points[i].y, points[i + 1].y], color="grey")
    plt.plot([points[n - 1].x, points[0].x], [points[n - 1].y, points[0].y], color="grey")


def draw_line(pts, color=False):
    if color:
        plt.plot([pts[0].x, pts[1].x], [pts[0].y, pts[1].y], color=color)
    else:
        plt.plot([pts[0].x, pts[1].x], [pts[0].y, pts[1].y])
