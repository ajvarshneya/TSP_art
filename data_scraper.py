import re

def acquire_points():
    # filename i/o
    filename = input('Enter filename: ')
    f = open(filename, 'r')

    result = []

    # get points from .svg
    for line in f:
        if line.startswith('<circle'):
            # gets x and y coords as string
            x_s = re.search('cx="(.*)" cy="', line).group(1)
            y_s = re.search('cy="(.*)" r="', line).group(1)
            # converts x and y coords to floats, then ints
            point = (int(float(x_s)), int(float(y_s)))
            # adds point to list
            result.append(point)
            print(result)

    return result