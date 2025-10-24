import json
import sys

import colorama

colorama.init(autoreset=True)

color = {
    "light_red": colorama.Fore.LIGHTRED_EX,
    "red": colorama.Fore.RED,
    "light_green": colorama.Fore.LIGHTGREEN_EX,
    "green": colorama.Fore.GREEN,
    "light_yellow": colorama.Fore.LIGHTYELLOW_EX,
    "yellow": colorama.Fore.YELLOW,
    "light_blue": colorama.Fore.LIGHTBLUE_EX,
    "blue": colorama.Fore.BLUE,
    "light_purple": colorama.Fore.LIGHTMAGENTA_EX,
    "purple": colorama.Fore.MAGENTA,
    "light_aqua": colorama.Fore.LIGHTCYAN_EX,
    "aqua": colorama.Fore.CYAN,
    "white": colorama.Fore.WHITE,
    "light_white": colorama.Fore.LIGHTWHITE_EX,
    "gray": colorama.Fore.LIGHTBLACK_EX,
    "black": colorama.Fore.BLACK,
    "reset": colorama.Fore.RESET
}

back_ground = {
    "light_red": colorama.Back.LIGHTRED_EX,
    "red": colorama.Back.RED,
    "light_green": colorama.Back.LIGHTGREEN_EX,
    "green": colorama.Back.GREEN,
    "light_yellow": colorama.Back.LIGHTYELLOW_EX,
    "yellow": colorama.Back.YELLOW,
    "light_blue": colorama.Back.LIGHTBLUE_EX,
    "blue": colorama.Back.BLUE,
    "light_purple": colorama.Back.LIGHTMAGENTA_EX,
    "purple": colorama.Back.MAGENTA,
    "light_aqua": colorama.Back.LIGHTCYAN_EX,
    "aqua": colorama.Back.CYAN,
    "white": colorama.Back.WHITE,
    "light_white": colorama.Back.LIGHTWHITE_EX,
    "gray": colorama.Back.LIGHTBLACK_EX,
    "black": colorama.Back.BLACK,
    "reset": colorama.Back.RESET
}

version = "JsonTuring Version V1.1.0"


def read_file(file, encoding):
    """
    读取并解析指定的JSON配置文件，提取操作序列和初始化参数

    参数:
        file (str): 要读取的文件路径
        encoding (str): 文件编码格式

    返回:
        tuple: 包含(head, pos, value, max_size, ops)的元组，其中
               head (str): 初始化字符串
               pos (int): 初始化位置
               value (int): 初始化值
               max_size (int): 最大大小限制，默认为256
               ops (list): 操作序列列表
        bool: 解析失败时返回False
    """
    try:
        with open(f"{file}.jst", 'r', encoding=encoding) as f:
            code = json.load(f)
            try:
                ops = code["ops"]
                init = code.get("init", {})
                if type(init) == dict:
                    head = init.get("head", "A")
                    pos = init.get("pos", 0)
                    value = init.get("value", 0)
                    max_size = init.get("max_size", 256)

                    # 验证必要字段类型
                    if not isinstance(head, str):
                        head = "A"

                    if not isinstance(pos, int):
                        pos = 0

                    if not isinstance(value, int):
                        value = 0

                    # 修正 max_size 类型检查逻辑
                    if not isinstance(max_size, int):
                        max_size = 256

                    # 验证 ops 是否为列表
                    if not isinstance(ops, list):
                        print(f"{colorama.Fore.RED}Error: Invalid ops format")
                        return False

                    return head, pos, value, max_size, ops
                else:
                    print(f"{colorama.Fore.RED}Error: Invalid init function")
                    return False
            except KeyError as e:
                print(f"{colorama.Fore.RED}Error: No {e} found in the file")
                return False
    except FileNotFoundError:
        print(f"{colorama.Fore.RED}Error: File {file}.jst not found")
        return False
    except json.JSONDecodeError:
        print(f"{colorama.Fore.RED}Error: Invalid JSON format")
        return False
    except Exception as e:
        print(f"{colorama.Fore.RED}Error: {str(e)}")
        return False


def run(table):
    """
    执行一个基于表驱动的图灵机模拟过程。

    参数:
        table (list): 包含图灵机初始状态和操作规则的列表，结构如下：
            table[0]: 初始头部状态（head）
            table[1]: 初始磁带位置（pos）
            table[2]: 初始写入磁带的值（value）
            table[3]: 磁带最大大小（max_size）
            table[4]: 操作规则列表（ops），每个操作是一部字典，包含条件和执行动作

    返回值:
        无返回值。函数通过打印输出执行过程中的信息或错误信息。
    """
    try:
        # 解析初始状态和参数
        head = table[0]
        pos = table[1]
        value = table[2]
        max_size = table[3]
        ops = table[4]
        user_input = None

        # 初始化磁带并设置初始值
        tape = [0] * max_size
        tape[pos] = value

        # 主循环：持续执行操作直到遇到停机指令
        while True:

            # 处理位置越界情况：循环磁带
            if pos >= max_size:
                pos = 0
            elif pos < 0:
                pos = max_size - 1

            # 遍历所有操作规则，查找匹配当前状态和磁带值的操作
            for op in ops:
                case = op.get("case", {})
                chead = case.get("head", head)
                cvalue = case.get("value", tape[pos])
                # 修改条件判断逻辑
                cond = case.get("cond", None)  # 改为 None 作为默认值

                # 更精确的条件匹配逻辑
                # noinspection PyUnusedLocal
                matched = False
                if cond is not None:
                    # 有条件字段，需要用户输入匹配
                    matched = (user_input is not None and cond == user_input) and (
                                chead == head and cvalue == tape[pos])
                else:
                    # 无条件字段，使用原有的 head 和 value 匹配
                    matched = (chead == head and cvalue == tape[pos])

                # 如果当前头部状态和磁带值匹配，则执行对应动作
                if matched:
                    code = op.get("run", {})
                    inputs = op.get("input", {})
                    setting = code.get("set", {})
                    text = code.get("text", [])
                    output = code.get("output", [])
                    head = setting.get("head", head)
                    value = setting.get("value", value)
                    move = setting.get("move", "N")
                    trigger = inputs.get("trigger", "")

                    if len(inputs) > 0:
                        texts = inputs.get("text", [])
                        trigger = inputs.get("trigger", "")

                        for i in texts:
                            print(f"{color.get(i.get('color', 'reset'))}"
                                  f"{back_ground.get(i.get('back', 'reset'))}"
                                  f"{i.get('text', '')}",
                                  end="")
                        user_input = input()

                    if user_input == trigger or len(inputs) == 0:

                        # 输出格式化文本内容
                        for i in text:
                            print(f"{color.get(i.get('color', 'reset'))}"
                                  f"{back_ground.get(i.get('back', 'reset'))}"
                                  f"{i.get('text', '')}",
                                  end="")

                        # 根据output字段输出调试信息
                        if "head" in output:
                            print(f"Head: {head}")
                        if "value" in output:
                            print(f"Value: {value}")
                        if "pos" in output:
                            print(f"Position: {pos}")

                        # 更新磁带当前位置的值
                        tape[pos] = value

                        # 根据移动指令更新磁头位置
                        if move == "L":
                            pos -= 1
                        elif move == "R":
                            pos += 1
                        elif move == "N":
                            pass
                        elif move == "H":
                            print(f"{colorama.Fore.GREEN}Run successfully")
                            return
                        else:
                            print(f"{colorama.Fore.RED}Error: Invalid move command")
                            return

                        # 处理位置越界情况：循环磁带
                        if pos >= max_size:
                            pos = 0
                        elif pos < 0:
                            pos = max_size - 1

    except IndexError as e:
        # 捕获索引越界错误
        print(f"{colorama.Fore.RED}Error: Index out of range - {str(e)}")
        return

    except KeyError as e:
        # 捕获缺少必要键的错误
        print(f"{colorama.Fore.RED}Error: Missing key {str(e)} in case")
        return

    except Exception as e:
        # 捕获其他未预期的错误
        print(f"{colorama.Fore.RED}Error: {str(e)}")
        return


def print_list(file, encoding):
    """
    从指定的JSON文件中读取数据并打印到控制台，支持颜色和背景色显示

    参数:
        file (str): 要读取的文件名（不包含.jtx扩展名）
        encoding (str): 文件编码格式

    返回值:
        无返回值

    异常处理:
        FileNotFoundError: 当文件不存在时
        json.JSONDecodeError: 当JSON格式无效时
        Exception: 其他未预期的异常
    """
    try:
        # 打开并读取JSON文件，然后按格式打印文本内容
        with open(f"{file}.jtx", "r", encoding=encoding) as f:
            file_data = json.load(f)
            for sentence in file_data:
                for texts in sentence:
                    print(f"{color.get(texts.get('color', 'reset'))}"
                          f"{back_ground.get(texts.get('back', 'reset'))}"
                          f"{texts.get('text', '')}",
                          end="")
                print()

    except FileNotFoundError:
        print(f"{colorama.Fore.RED}File {file}.jtx not found.")

    except json.JSONDecodeError:
        print(f"{colorama.Fore.RED}Invalid JSON format in {file}.jtx.")

    except Exception as e:
        print(f"{colorama.Fore.RED}Error reading file: {str(e)}")


def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python3 jst.py (run|info|read) <file>")
            return
        elif len(sys.argv) >= 2:
            if sys.argv[1] == "run":
                flag = read_file(sys.argv[2], "utf-8")
                run(flag)
            elif sys.argv[1] == "info":
                print(version)
            elif sys.argv[1] == "read":
                print_list(sys.argv[2], "utf-8")
            else:
                print("Usage: python3 jst.py (run|info|read) <file>")

    except Exception as e:
        print(f"{colorama.Fore.RED}Error: {str(e)}")


if __name__ == "__main__":
    main()
