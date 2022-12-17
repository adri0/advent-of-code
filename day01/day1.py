input_str = open("input.txt").read()

calories = [
    sum(map(int, cal_str.split("\n"))) 
    for cal_str in input_str.split("\n\n")
]

print(max(calories))

print(sum(sorted(calories)[-3:]))