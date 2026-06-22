import time

from screen import *


def run_jst(head, value, pos, max_size, function, token, if_clear, if_pause, sleep_time) -> None:
    """
    执行 JST 图灵机程序的主运行循环。

    该函数会初始化纸带，解析 main 块中的操作序列，然后根据触发条件
    匹配并执行对应的函数定义，直到遇到停机指令（H）为止。

    参数:
        head: 当前表头标识符
        value: 当前格子的数值
        pos: 读写头的当前位置坐标
        max_size: 纸带的最大长度
        function: 从代码中提取的函数定义字典，键为函数名，值为包含 trigger 和 options 的字典
        token: 解析后的代码令牌列表，用于提取 main 块
        if_clear: 是否在每次结束后清屏（True 为清屏，False 为不清屏）
        if_pause: 是否在每次结束后等待用户输入（True 为等待，False 为不等待）
        sleep_time: 每次结束后的停顿秒数（None 或 0 为不停顿）

    返回值:
        无（函数执行完毕后直接返回）
    """
    paper = [0] * max_size
    paper[pos] = value

    main = []
    for i in token:
        if i[0] != 'main':
            continue
        main = i[1]

    while True:
        if if_clear:
            clear()

        # 打印当前纸带状态，标记读写头位置
        for i in range(len(paper)):
            if i == pos:
                print(f'>{paper[i]}<', end='')
            else:
                print(f' {paper[i]} ', end='')
        print(f'表头：{head}')

        if if_pause:
            input('按下回车下一步操作...')

        if sleep_time:
            time.sleep(sleep_time)

        # 遍历 main 中的操作序列，查找匹配的函数并执行
        for func_name in main:
            func = function[func_name]
            trigger_list = func['trigger']
            options_list = func['options']

            # 将扁平列表转换为字典：['head', '表头', 'value', '数值'] -> {'head': '表头', 'value': '数值'}
            trigger = {}
            for k in range(0, len(trigger_list), 2):
                trigger[trigger_list[k]] = trigger_list[k + 1]

            # 将拼接格式的列表转换为字典：['head设置表头', 'value变换数值'] -> {'head': '设置表头', 'value': '变换数值'}
            options = {}
            known_keys = ['head', 'value', 'move']  # 已知的有效键名

            for item in options_list:
                for key in known_keys:
                    if item.startswith(key):
                        val = item[len(key):]
                        options[key] = val
                        break

            cond_head = trigger.get('head', head)
            cond_value = trigger.get('value', value)

            if head == cond_head and value == cond_value:
                head = options.get('head', head)
                value = options.get('value', value)
                move = options.get('move', 'N')
                # noinspection PyTypeChecker
                paper[pos] = value

                if move == 'L':
                    pos -= 1
                    if pos < 0:
                        pos = max_size - 1

                elif move == 'R':
                    pos += 1
                    if pos > max_size - 1:
                        pos = 0

                elif move == 'N':
                    pass

                elif move == 'H':
                    print('程序已停机。')
                    return

                break
