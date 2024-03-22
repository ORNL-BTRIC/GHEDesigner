from ghedesigner.shape import point_polygon_check


def remove_cutout(coordinates, boundary, remove_inside=True, keep_contour=True):
    inside_points_idx = []
    outside_points_idx = []
    boundary_points_idx = []

    inside = 1
    outside = -1
    on_edge = 0

    for idx, coordinate in enumerate(coordinates):
        coordinate = coordinates[idx]
        ret = point_polygon_check(boundary, coordinate)
        if ret == inside:
            inside_points_idx.append(idx)
        elif ret == outside:
            outside_points_idx.append(idx)
        elif ret == on_edge:
            boundary_points_idx.append(idx)
        else:
            raise ValueError("Something bad happened")

    new_coordinates = []
    for idx, _ in enumerate(coordinates):
        # if we want to remove inside points and keep contour points
        if remove_inside and keep_contour:
            if idx in inside_points_idx:
                continue
            else:
                new_coordinates.append(coordinates[idx])
        # if we want to remove inside points and remove contour points
        elif remove_inside and not keep_contour:
            if idx in inside_points_idx or idx in boundary_points_idx:
                continue
            else:
                new_coordinates.append(coordinates[idx])
        # if we want to keep outside points and remove contour points
        elif not remove_inside and not keep_contour:
            if idx in outside_points_idx or idx in boundary_points_idx:
                continue
            else:
                new_coordinates.append(coordinates[idx])
        # if we want to keep outside points and keep contour points
        else:
            if idx in outside_points_idx:
                continue
            else:
                new_coordinates.append(coordinates[idx])

    return new_coordinates


def determine_largest_rectangle(property_boundary):
    x_max = float('-inf')
    y_max = float('-inf')
    x_min = float('inf')
    y_min = float('inf')
    for bf_outline in property_boundary:
        for x, y in bf_outline:
            if x > x_max:
                x_max = x
            if y > y_max:
                y_max = y
            if x < x_min:
                x_min = x
            if y < y_min:
                y_min = y

    rectangle = [[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max], [x_min, y_min]]

    return rectangle
