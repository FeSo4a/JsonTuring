def open_jst(file_name: str) -> str:
    try:
        with open(f'{file_name}.jst', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f'无法打开文件：{e}')
        exit()


def jst_init(code: list) -> tuple:
    """
    从解析后的代码中提取并初始化图灵机的配置参数。

    该函数会遍历代码令牌列表，查找 'init' 块，
    并从中提取表头(head)、初始值(value)、位置(pos)和纸带长度(max)四个配置项。
    若某项未在配置中指定，则使用默认值。

    参数:
        code: 解析后的代码令牌列表，包含 init/fn/main 等块的结构化数据

    返回:
        元组 (head, value, pos, max_size)，分别表示：
        - head: 表头标识符（默认为 'A'）
        - value: 初始数值（默认为 0）
        - pos: 初始位置坐标（默认为 0）
        - max_size: 纸带最大长度（默认为 256）
    """
    head = 'A'
    value = 0
    pos = 0
    max_size = 256

    for i in code:
        if i[0] != 'init':
            continue

        init_config: list = i[1]
        for index in range(len(init_config)):
            if init_config[index].startswith('head'):
                head = init_config[index][4:]
            elif init_config[index].startswith('value'):
                value = init_config[index][5:]
            elif init_config[index].startswith('pos'):
                pos = int(init_config[index][3:])
            elif init_config[index].startswith('max'):
                max_size = int(init_config[index][3:])

    return head, value, pos, max_size
