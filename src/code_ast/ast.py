"""
一门语言系统，
特性是先读取init初始化，然后用main主类进入程序，从上到下依次循环执行操作，直到停机。
若有操作满足条件，则立即执行，后续操作跳过直接开启下一轮循环。
"""

# 语言示例代码
example = '''
init {
    head 表头;
    value 当前这格数值;
    pos 一维坐标;
    max 纸带长
}

fn 操作名称 {
    if (
        head = 判断表头是否满足条件;
        value = 判断表头指向数值是否满足条件
    )

    head 设置表头;
    value 变换表头所指向的数值;
    move 设置操作（L左 R右 N空 H停机）
}

main {
    操作名称;
    ...
}
'''


def flatten(lst: list) -> list:
    """
    递归展平嵌套列表为一维列表。

    该函数会将任意深度的嵌套列表结构（包含字符串和列表的混合类型）
    转换为扁平的一维列表。

    参数:
        lst: 待展平的列表，可能包含嵌套的子列表或其他类型元素

    返回:
        展平后的一维列表，所有嵌套结构被移除
    """
    result: list = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def remove_comments(text: str) -> str:
    """
    删除文本中用 // 包裹的单行注释

    参数:
        text: 包含注释的原始文本

    返回:
        删除注释后的文本
    """
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        # 查找 // 的位置，但需要排除字符串中的 //
        cleaned_line = _remove_line_comment(line)
        cleaned_lines.append(cleaned_line)

    return '\n'.join(cleaned_lines)


def _remove_line_comment(line: str) -> str:
    """
    删除单行中的 // 注释，处理字符串内的 // 情况

    参数:
        line: 单行文本

    返回:
        删除注释后的行
    """
    in_single_quote = False
    in_double_quote = False
    i = 0

    while i < len(line):
        char = line[i]

        # 处理转义字符
        if char == '\\' and i + 1 < len(line):
            i += 2
            continue

        # 处理双引号字符串
        if char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        # 处理单引号字符串
        elif char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
        # 检测 // 注释（不在字符串内）
        elif char == '/' and i + 1 < len(line) and line[i + 1] == '/':
            if not in_single_quote and not in_double_quote:
                return line[:i].rstrip()

        i += 1

    return line


class Ast:
    def __init__(self, code) -> None:
        self.text: str = code
        self.token: list = []
        self.function: dict = {}

    def divide(self) -> None:
        """
        将 JST 代码文本解析为分层令牌结构。

        该函数会执行以下步骤：
        1. 清除所有空白字符（空格、制表符、换行符）
        2. 按 '}' 分割代码块
        3. 对每个代码块按 '{' 进一步分割
        4. 根据不同块类型（init/fn/main）进行精细化解析

        解析后的结果存储在 self.token 中，形成二维或三维列表结构。

        返回值:
            无（直接修改 self.token 属性）
        """
        self.text: str = remove_comments(self.text)
        self.text: str = self.text.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
        self.token: list = self.text.split('}')
        temp_token: list = []

        for i in self.token:
            # noinspection PyTypeChecker
            i = i.split('{')

            if i[0] == 'init':
                # 解析 init 块的键值对配置
                i[1] = i[1].split(';')
                i[1] = flatten(i[1])

            elif i[0].startswith('fn'):
                # 解析 fn 函数定义的条件和执行体
                i[1] = i[1].split(')')
                i = flatten(i)

                i[1] = i[1].split('(')
                i[1][1] = i[1][1].split(';')
                i[1][1] = flatten(i[1][1])

                for j in range(len(i[1][1])):
                    i[1][1][j] = i[1][1][j].split('=')
                i[1][1] = flatten(i[1][1])

                i[2] = i[2].split(';')
                i[2] = flatten(i[2])

            elif i[0] == 'main':
                # 解析 main 主程序的操作序列
                i[1] = i[1].split(';')
                i[1] = flatten(i[1])

            temp_token.append(i)

        self.token = temp_token

    def set_function(self):
        """
        从解析后的令牌中提取函数定义并存储到 self.function 字典中。

        该函数会遍历 self.token，识别以 'fn' 开头的函数块，
        提取触发条件（trigger）和执行选项（options），
        并以函数字典格式存储。

        返回值:
            无（直接修改 self.function 属性）
        """
        # 使用列表推导式创建新列表，排除已处理的 'fn' 项，同时提取函数信息
        new_token = []
        for i in self.token:
            if i[0].startswith('fn'):
                trigger: list = []
                run: list = []
                for j in i:
                    if type(j) != list:
                        continue

                    if j[0] == 'if':
                        # 提取 if 条件部分作为触发器
                        trigger = j[1]
                    else:
                        # 提取其他部分作为执行选项
                        run = j
                self.function[i[0][2:]] = {'trigger': trigger, 'options': run}
                # 该项已存储到 function，不再保留在 token 中，因此不加入 new_token
            else:
                # 非 fn 项（如 init, main）保留在 token 中
                new_token.append(i)

        self.token = new_token


# divide输出示例：
'''
[
    [
        'init',
        [
            'head表头',
            'value当前这格数值',
            'pos一维坐标',
            'max纸带长'
        ]
    ],
    [
        'fn操作名称',
        [
            'if',
            [
                'head', '判断表头是否满足条件',
                'value', '判断表头指向数值是否满足条件'
            ]
        ],
        [
            'head设置表头',
            'value变换表头所指向的数值',
            'move设置操作（L左R右N空H停机）'
        ]
    ],
    [
        'main',
        [
            '操作名称...'
        ]
    ]
]
'''

# function输出示例：
'''
{
    '操作名称': {
        'trigger': [
            'head', '判断表头是否满足条件', 
            'value', '判断表头指向数值是否满足条件'
        ], 
        'options': [
            'head设置表头', 
            'value变换表头所指向的数值', 
            'move设置操作（L左R右N空H停机）'
        ]
    }
}
'''

# 最终token示例：
'''
[
    [
        'init', 
        [
            'head表头', 
            'value当前这格数值', 
            'pos一维坐标', 
            'max纸带长'
        ]
    ], 
    [
        'main', [
            '操作名称...'
        ]
    ]
]
'''