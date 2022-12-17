from collections import defaultdict

current_pwd = [] 
directories = defaultdict(int)  # name -> size

with open("input.txt") as input_file:
    for terminal_out in map(lambda s: s.strip(), input_file):
        match terminal_out.split():
            case "$", "cd", "..":
                current_pwd.pop()
            case "$", "cd", dirname:
                current_pwd.append(dirname)
            case ("$", *_) | ("dir", _):
                pass
            case size, _ if size.isnumeric():
                for i, dirname in enumerate(current_pwd):
                    path = "/".join(current_pwd[:i+1])
                    directories[path] += int(size)
            case _:
                raise Exception(f"Unrecognized input: {terminal_out}")

sum_sizes = sum(
    [size for size in directories.values() if size <= 100_000]
)
print("Sum size:", sum_sizes)

# -- Part 2 -- #
occupied = directories["/"]
free_space = 70_000_000 - occupied
missing_space = 30_000_000 - free_space

dir_size_to_delete = min(
    [size for size in directories.values() if size >= missing_space]
)
print("Dir size to delete:", dir_size_to_delete)