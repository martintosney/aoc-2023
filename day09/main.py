import fileinput

input = [i.strip().split(" ") for i in fileinput.input()]


def build_ext_pyramid(number_list):
    if len([d for d in number_list if d != 0]) == 0:
        return [number_list + [0]]
    else:
        next_list = [r - l for l, r in zip(number_list[:-1], number_list[1:])]
        sub_lists = build_ext_pyramid(next_list)
        next_value = number_list[-1] + sub_lists[0][-1]
        return [number_list + [next_value]] + sub_lists


pyramids = [build_ext_pyramid([int(d) for d in i]) for i in input]

print(sum([l[0][-1] for l in pyramids]))
