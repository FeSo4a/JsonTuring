import argparse

from code_ast import *
from run_jst import *


def main() -> None:
    parser = argparse.ArgumentParser(
        description='''
        v1.1.0 | MIT许可证 | By FeSo4a
        一个简单的模拟图灵机运行的程序。
        ''',
        
    )

    parser.add_argument('-r', '--run', type=str, help='运行.jst文件（无需后缀）')
    parser.add_argument('-a', '--ast', type=str, help='显示分词以后的.jst文件（无需后缀）')
    parser.add_argument('-c', '--clear', action='store_true', help='每步结束以后是否清空屏幕')
    parser.add_argument('-t', '--time', type=int, help='每步结束后会停顿几秒', default=0)
    parser.add_argument('-p', '--pause', action='store_true', help='每步结束后是否暂停')

    args = parser.parse_args()

    if args.run:
        jst_code: str = open_jst(args.run)
        jst: Ast = Ast(jst_code)
        jst.divide()
        jst.set_function()
        head, value, pos, max_size = jst_init(jst.token)

        run_jst(head, value, pos, max_size, jst.function, jst.token, args.clear, args.pause, args.time)

    elif args.ast:
        jst_code: str = open_jst(args.ast)
        jst: Ast = Ast(jst_code)
        jst.divide()
        print('分词以后的代码：')
        print(jst.token)

        jst.set_function()
        print('提取到的函数定义：')
        print(jst.function)

if __name__ == '__main__':
    main()
