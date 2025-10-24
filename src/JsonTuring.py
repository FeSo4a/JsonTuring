import json
import logging
import os
import sys
import time

import colorama

# 定义日志级别映射字典，将字符串级别的日志映射到 logging 模块对应的常量
logging_level = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

# 定义日志配置字典，包括默认日志级别、输出文件路径、文件打开模式、日期格式和日志格式
log = {
    "level": "info",
    "filename": "../log/log.log",
    "filemode": "w",
    "datefmt": "%d/%m/%Y %I:%M:%S %p",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# 定义前景色字典，使用 colorama 库提供的颜色常量，用于在终端中设置文字颜色
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

# 定义背景色字典，使用 colorama 库提供的背景色常量，用于在终端中设置文字背景色
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

# 尝试加载主题配置文件，设置前景色和背景色
# 如果文件不存在，则使用默认颜色
try:
    with open("../save/save.json", "r", encoding="utf-8") as s:
        save = json.load(s)
        tcolor = save.get("color", "reset")
        tback = save.get("back", "reset")
        theme = f"{color.get(tcolor, colorama.Fore.RESET)}{back_ground.get(tback, colorama.Back.RESET)}"
        logging.info("Theme loaded.")
except FileNotFoundError:
    tcolor = "reset"
    tback = "reset"
    theme = f"{color.get(tcolor, colorama.Fore.RESET)}{back_ground.get(tback, colorama.Back.RESET)}"
    logging.error("Error loading the file")

# 初始化colorama库，用于在终端中显示颜色
colorama.init(autoreset=True)

# 尝试加载日志配置文件并设置日志记录参数
# 如果配置文件不存在，则使用默认的日志设置
try:
    with open("../config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

        filename = config.get("loggings", log).get("filename", "../log/log.log")
        filemode = config.get("loggings", log).get("filemode", "w")
        log_level = config.get("loggings", log).get("level", "info")
        log_level = logging_level.get(log_level, logging.INFO)
        log_datefmt = config.get("loggings", log).get("datefmt", "%d/%m/%Y %I:%M:%S %p")
        log_format = config.get("loggings", log).get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        logging.basicConfig(
            filename=filename,
            format=log_format,
            datefmt=log_datefmt,
            filemode=filemode,
            level=log_level
        )
    logging.info("Logging started.")
except FileNotFoundError:
    logging.basicConfig(
        filename="../log/log.log",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
        filemode="w",
        level=logging.INFO
    )
    logging.error("Error creating log file.")


def clear():
    """
    清空终端屏幕

    该函数根据操作系统类型执行相应的清屏命令：
    - Windows系统(nt)：执行cls命令
    - 非Windows系统：执行clear命令

    无参数

    无返回值
    """
    # 根据操作系统类型选择合适的清屏命令
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")



def pr_about():
    """
    打印程序相关信息

    该函数用于输出程序的版本信息、作者信息以及相关的链接地址。
    包括GitHub仓库地址和Bilibili个人空间链接。

    参数:
        无

    返回值:
        无
    """
    print("Version: V1.1.0")
    print("Author: @FeSo4a")
    print("Github: https://github.com/FeSo4a")
    print("Bilibili: https://space.bilibili.com/3546674548967510")



def pr_help():
    """
    打印帮助菜单，显示所有可用命令及其功能说明

    该函数输出程序支持的所有命令，包括：
    - pass: 通过当前操作
    - about: 显示作者信息
    - clear: 清屏
    - exit: 退出程序
    - help: 显示帮助菜单或特定命令的帮助
    - color: 设置颜色或显示当前颜色
    - back: 设置背景或显示当前背景
    - save: 保存主题设置
    - read: 读取并显示.jtx文件
    - run: 运行.jst文件

    参数:
        无

    返回值:
        无
    """
    print(f"{theme}pass/  -> Pass")
    print(f"{theme}about -> Print author information")
    print(f"{theme}clear -> Clear the screen")
    print(f"{theme}exit -> Exit the program")
    print(f"{theme}help (color|back) -> Print help menu or command help")
    print(f"{theme}color [<color>|info] -> Set color or show current color")
    print(f"{theme}back [<background>|info] -> Set background or show current background")
    print(f"{theme}save -> Save the theme")
    print(
        f"{theme}read <file> <encoding> -> Read and display a .jtx file (You don't need to add .jtx to the file name)")
    print(f"{theme}run <file> -> Run a .jst file (You don't need to add .jst to the file name)")


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
        print(f"{theme}File {file}.jtx not found.")
        logging.error(f"File {file}.jtx not found.")

    except json.JSONDecodeError:
        print(f"{theme}Invalid JSON format in {file}.jtx.")
        logging.error(f"Invalid JSON format in {file}.jtx.")

    except Exception as e:
        print(f"{theme}Error reading file: {str(e)}")
        logging.error(f"Error reading file: {str(e)}")


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
            logging.info(f"Reading file: {file}.jst")
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
                        print(f"{theme}Error: Invalid ops format")
                        return False

                    return head, pos, value, max_size, ops
                else:
                    print(f"{theme}Error: Invalid init function")
                    logging.warning("Invalid init function")
                    return False
            except KeyError as e:
                print(f"{theme}Error: No {e} found in the file")
                logging.error(f"No {e} found in the file")
                return False
    except FileNotFoundError:
        print(f"{theme}Error: File {file}.jst not found")
        logging.error(f"File {file}.jst not found")
        return False
    except json.JSONDecodeError:
        print(f"{theme}Error: Invalid JSON format")
        logging.error("Invalid JSON format")
        return False
    except Exception as e:
        print(f"{theme}Error: {str(e)}")
        logging.error(f"Error: {str(e)}")
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
                            print(f"{theme}Head: {head}")
                        if "value" in output:
                            print(f"{theme}Value: {value}")
                        if "pos" in output:
                            print(f"{theme}Position: {pos}")

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
                            print(f"{theme}Run successfully")
                            return
                        else:
                            print(f"{theme}Error: Invalid move command")
                            logging.warning("Invalid move command")
                            return

                        # 处理位置越界情况：循环磁带
                        if pos >= max_size:
                            pos = 0
                        elif pos < 0:
                            pos = max_size - 1

    except IndexError as e:
        # 捕获索引越界错误
        print(f"{theme}Error: Index out of range - {str(e)}")
        logging.error(f"Index out of range - {str(e)}")
        return

    except KeyError as e:
        # 捕获缺少必要键的错误
        print(f"{theme}Error: Missing key {str(e)} in case")
        logging.error(f"Missing key {str(e)} in case")
        return

    except Exception as e:
        # 捕获其他未预期的错误
        print(f"{theme}Error: {str(e)}")
        logging.error(f"Error: {str(e)}")
        return


def set_color(colors):
    """
    设置或显示当前主题颜色

    参数:
        colors (str): 颜色名称字符串，支持的颜色在color字典中定义

    返回值:
        None
    """
    global tcolor
    colors = colors.lower()

    # 处理info命令，显示当前颜色
    if colors == "info":
        print(f"{theme}Color: {tcolor}")
        return

    # 验证颜色是否有效
    if colors not in color:
        print(f"{theme}Unknown color, type 'help' for help.")
        logging.warning("Unknown color")
        return

    # 设置新颜色并记录日志
    tcolor = colors
    if tcolor == "reset":
        print(f"{theme}Color reset.")
    else:
        print(f"{theme}Color set to {tcolor}")
    logging.info(f"Color set to {tcolor}")


def set_back(backs):
    """
    设置背景主题的函数

    参数:
        backs (str): 背景主题名称或命令

    返回值:
        无返回值

    功能说明:
        - 处理背景主题的设置和查询
        - 支持查询当前背景、设置新背景、重置背景等功能
        - 包含输入验证和日志记录
    """
    global tback
    backs = backs.lower()

    # 处理背景信息查询命令
    if backs == "info":
        print(f"{theme}Background: {tback}")
        return

    # 验证背景名称是否有效
    if backs not in back_ground:
        print(f"{theme}Unknown background, type 'help' for help.")
        logging.warning("Unknown background")
        return

    # 设置新的背景主题
    tback = backs
    if tback == "reset":
        print(f"{theme}Background reset.")
    else:
        print(f"{theme}Background set to {tback}")
    logging.info(f"Background set to {tback}")


def operate(command):
    command = command.lower()
    command = command.split()

    if len(command) == 0 or command[0] == "pass":
        pass
    elif command[0] == "about":
        pr_about()
    elif command[0] == "exit":
        print(f"{theme}Exiting...")
        time.sleep(1)
        sys.exit()
    elif command[0] == "clear":
        clear()
        print(f"{theme}Type 'help' for help.")
    elif command[0] == "help":
        if len(command) < 2:
            pr_help()
            return
        else:
            if command[1] == "color":
                print(f"{theme}Available colors: {', '.join(color.keys())}")
            elif command[1] == "back":
                print(f"{theme}Available backgrounds: {', '.join(back_ground.keys())}")
            else:
                print(f"{theme}Unknown command. Type 'help' for help.")
                logging.warning("Unknown command")

    elif command[0] == "color":
        if len(command) < 2:
            print(f"{theme}Invalid arguments. Usage: color <color>|info")
            logging.warning("Invalid arguments")
            return
        set_color(command[1])
    elif command[0] == "back":
        if len(command) < 2:
            print(f"{theme}Invalid arguments. Usage: back <background>|info")
            logging.warning("Invalid arguments")
            return
        set_back(command[1])

    elif command[0] == "save":
        save = {
            "color": tcolor,
            "back": tback
        }
        try:
            with open("../save/save.json", "w", encoding="utf-8") as s:
                json.dump(save, s, ensure_ascii=False, indent=4)
                print(f"{theme}Theme saved successfully.")
            logging.info("Theme saved successfully.")
        except FileNotFoundError:
            os.makedirs("../save")
            with open("../save/save.json", "w", encoding="utf-8") as s:
                json.dump(save, s, ensure_ascii=False, indent=4)
                print(f"{theme}Theme saved successfully.")
            logging.error("File not found")


    elif command[0] == "read":
        if len(command) < 2:
            print(f"{theme}Invalid arguments. Usage: read <file> <encoding>")
            return
        elif len(command) == 2:
            print_list(command[1], "utf-8")
        elif len(command) == 3:
            print_list(command[1], command[2])
        else:
            print(f"{theme}Invalid arguments. Usage: read <file> <encoding>")

    elif command[0] == "run":
        flag = None
        if len(command) < 2:
            print(f"{theme}Invalid arguments. Usage: run <file> <encoding>")
            return
        elif len(command) == 2:
            flag = read_file(command[1], "utf-8")
        elif len(command) == 3:
            flag = read_file(command[1], command[2])
        else:
            print(f"{theme}Invalid arguments. Usage: run <file> <encoding>")
        run(flag)


    else:
        print(f"{theme}Unknown command. Type 'help' for help.")


def main():
    """
    主函数，负责程序的主要运行循环
    该函数初始化主题颜色，显示帮助信息，并持续接收用户输入命令进行处理

    全局变量:
        theme: 主题颜色样式

    无参数
    无返回值
    """
    global theme
    print(f"{theme}Type 'help' for help.")

    # 主循环：持续接收用户命令并执行操作
    while True:
        # 更新主题颜色样式
        theme = f"{color.get(tcolor, colorama.Fore.RESET)}{back_ground.get(tback, colorama.Back.RESET)}"
        # 获取用户输入的命令
        command = input(f"{theme}> ")
        # 执行对应的命令操作
        operate(command)


if __name__ == "__main__":
    # 清理操作，为程序运行做准备
    clear()
    # 执行程序的主要逻辑
    main()
