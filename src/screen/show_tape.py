def print_tape(paper, pos, head, size):
    half = 5
    head_line = ''
    tape_line = ''

    for i in range(-half, half + 1):
        idx = (pos + i) % size
        val = paper.get(idx, 0)

        if i == 0:
            tape_line += f'>{val}<'
            head_line += f' {head} '
        else:
            tape_line += f' {val} '
            head_line += '   '

    print(head_line)
    print(tape_line)
    print()