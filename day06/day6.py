def find_n_diff_chars(input_stream, n_chars):
    init_window = list(input_stream.read(n_chars))
    count = len(init_window)

    while len(set(init_window)) < n_chars:
        next_char = input_stream.read(1)
        if not next_char:
            raise Exception("End of stream")
        init_window = init_window[1:] + [next_char]
        count += 1

    return count

result1 = find_n_diff_chars(open("input.txt"), 4)
print(result1)


# -- Part 2 -- #

result2 = find_n_diff_chars(open("input.txt"), 14)
print(result2)