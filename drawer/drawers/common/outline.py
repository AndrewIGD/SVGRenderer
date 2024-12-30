import math

def points_to_vector_eq(a, b):
    x1, y1 = a
    x2, y2 = b

    return a, (x2 - x1, y2 - y1)

def line_intersection(l1, l2):
    a, b = l1
    c, d = l2

    v1 = points_to_vector_eq(a, b)
    v2 = points_to_vector_eq(c, d)

    dx1 = v1[1][0]
    dy1 = v1[1][1]
    dx2 = v2[1][0]
    dy2 = v2[1][1]

    A = dx1
    B = -dx2
    C = dy1
    D = -dy2
    E = v2[0][0] - v1[0][0]
    F = v2[0][1] - v1[0][1]

    denominator = A * D - B * C
    if denominator == 0:
        return None

    t = (E * D - B * F) / denominator

    return v1[0][0] + t * v1[1][0], v1[0][1] + t * v1[1][1]

def offset(a, b, offset):
    v = points_to_vector_eq(a, b)
    perpendicular_vector = -v[1][1], v[1][0]

    magnitude = math.sqrt(perpendicular_vector[0] ** 2 + perpendicular_vector[1] ** 2)

    normalized_perpendicular = perpendicular_vector[0] / magnitude, perpendicular_vector[1] / magnitude

    return (a[0] + offset * normalized_perpendicular[0], a[1] + offset * normalized_perpendicular[1]), (b[0] + offset * normalized_perpendicular[0], b[1] + offset * normalized_perpendicular[1])


def outline(config, points, color, width):
    config.image.line(points, fill=color, width=width, joint=config.linecap)

    if config.linecap != "miter":
        return

    # Draw Miter Joints

    point_list = points[:]
    point_list.extend(points[:2])

    index = 0
    while index < len(point_list) - 1:
        if point_list[index][0] == point_list[index + 1][0] and point_list[index][1] == point_list[index + 1][1]:
            point_list.pop(index)
        else: index += 1

    for i in range(len(point_list) - 2):
        a, b, c = point_list[i:i+3]

        l1 = offset(a, b, width / 2)
        l2 = offset(b, c, width / 2)

        intersection = line_intersection(l1, l2)

        if intersection is None:
            continue

        config.image.polygon([(round(l1[1][0]), round(l1[1][1])), (round(intersection[0]), round(intersection[1])), (round(l2[0][0]), round(l2[0][1])), b], fill=color)