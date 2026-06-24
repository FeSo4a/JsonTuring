import time

from screen import *


def run_jst(
    head: str,
    value: int,
    pos: int,
    max_size: int,
    function: dict,
    token: list,
    if_clear: bool,
    if_pause: bool,
    sleep_time: float|int
) -> None:
    """
    max_size:
        - 纸带允许的最大格子数（键值对数量）
        - 超过后自动变成循环纸带
    """

    paper = {pos: value}
    size = max_size  # 当前纸带大小（固定）

    # 提取 main
    main = []
    for i in token:
        if i[0] == 'main':
            main = i[1]
            break

    while True:
        if if_clear:
            clear()

        print_tape(paper, pos, head, size)

        if if_pause:
            input('按下回车下一步操作...')

        if sleep_time:
            time.sleep(sleep_time)

        for func_name in main:
            func = function[func_name]
            trigger_list = func['trigger']
            options_list = func['options']

            trigger = {}
            for k in range(0, len(trigger_list), 2):
                trigger[trigger_list[k]] = trigger_list[k + 1]

            options = {}
            for item in options_list:
                for key in ('head', 'value', 'move'):
                    if item.startswith(key):
                        options[key] = item[len(key):]
                        break

            cond_head = trigger.get('head', head)
            cond_value = trigger.get('value', value)

            if head == cond_head and value == cond_value:
                head = options.get('head', head)
                value = options.get('value', value)
                move = options.get('move', 'N')

                # 写入当前格
                paper[pos] = value

                # 超过最大格子数 → 循环模式
                if len(paper) >= size:
                    new_paper = {}
                    for k in paper:
                        new_paper[k % size] = paper[k]
                    paper = new_paper

                # 移动（统一模运算）
                if move == 'L':
                    pos = (pos - 1) % size
                elif move == 'R':
                    pos = (pos + 1) % size
                elif move == 'N':
                    pass
                elif move == 'H':
                    print('程序已停机。')
                    return

                break
