from collections import defaultdict


def parse_directories_sizes(input_path):
    cwd = [] 
    directories = defaultdict(int)  # name -> size
    for terminal_out in open(input_path):
        match terminal_out.strip().split():
            case "$", "cd", "..":
                cwd.pop()
            case "$", "cd", dirname:
                cwd.append(dirname)
            case size, _ if size.isnumeric():
                for i, dirname in enumerate(cwd):
                    path = "/".join(cwd[:i+1])
                    directories[path] += int(size)
            case ("$", *_) | ("dir", _):
                pass
            case _:
                raise Exception(f"Unrecognized input: {terminal_out}")
    return directories


def sum_sizes(directories):
    return sum(filter(lambda size: size <= 100_000, directories.values()))


def dir_size_to_delete(directories):
    occupied = directories["/"]
    free_space = 70_000_000 - occupied
    missing_space = 30_000_000 - free_space
    return min(filter(lambda size: size >= missing_space, directories.values()))


directories = parse_directories_sizes("input.txt")
print("Sum sizes:", sum_sizes(directories))
print("Dir size to delete:", dir_size_to_delete(directories))