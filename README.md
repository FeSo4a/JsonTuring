# JsonTuring

JsonTuring 是一个基于 JSON 配置文件的图灵机模拟器，可以通过定义简单的 JSON 文件来创建和运行图灵机。

## 功能特点

- 基于 JSON 配置文件的图灵机模拟
- 支持自定义颜色和背景主题
- 提供命令行交互界面
- 支持读取和运行 [.jst](example.jst) 文件
- 可视化显示执行过程

## 安装与运行

确保已安装 Python 3.x 和 colorama 库：

```bash
pip install colorama
```

运行程序：

```bash
python src/jsonTexts.py
```

## 使用方法

### 命令行指令

- `help` - 显示帮助菜单
- `run <file>` - 运行指定的 [.jst](example.jst) 文件 _(JsonTuring)_
- `read <file> <encoding>` - 读取并显示 [.jst](example.jst) 文件内容 _(JsonText)_
- `color [<color>|info]` - 设置文字颜色或查看当前颜色
- `back [<background>|info]` - 设置背景颜色或查看当前背景
- `save` - 保存当前主题设置
- [clear](src\JsonTuring.py#L109-L113) - 清屏
- `about` - 显示作者信息
- `exit` - 退出程序

### JST 文件格式

JsonText 文件采用 JSON 格式，包含以下主要部分：
- [**[]**](#1145 "list") `根列表（自动换行）` [$_*$](#1145 "在JsonTuring中使用时省略最外层")
  - [**[]**](#1145 "list") `存储字符（不会换行）的列表`
    - [**{}**](#1145 "dict") `字符串根标签` [*](#1145 "此项为必选项")
      - [**S**](#1145 "str") `text` -> 输出的文字
      - [**S**](#1145 "str") `color` -> 文字颜色
      - [**S**](#1145 "str") `back` -> 背景颜色


JsonTuring 文件采用 JSON 格式，包含以下主要部分：
- [**{}**](#1145 "dict") `根标签`
  - [**{}**](#1145 "dict") `init` -> 初始化标签
    - [**S**](#1145 "str") `head` -> 表头
    - [**I**](#1145 "int") `value` -> 指针指向的值
    - [**I**](#1145 "int") `pos` -> 初始指针坐标
  - [**[]**](#1145 "list") `ops` [*](#1145 "此项为必选项") -> 操作表
    - [**{}**](#1145 "dict") `操作根标签`
      - [**{}**](#1145 "dict") `case` -> 若满足条件，则执行同操作根标签下的`run`
        - [**S**](#1145 "str") `head` -> 检查表头是否满足条件
        - [**I**](#1145 "int") `value` -> 检查值是否满足条件
        - [**S**](#1145 "str") `cond` -> 检查user_input是否满足条件（与上面两种不能同时存在）
      - [**{}**](#1145 "dict") `input` -> 读取标签
        - [**T**](#1145 "JsonText") `text` -> 屏幕上的提示词（换行请用`\n`）
        - [**S**](#1145 "str") `trigger` -> 若输入满足trigger，则执行同操作根标签下的`run`
      - [**{}**](#1145 "dict") `run` -> 操作执行标签
        - [**T**](#1145 "JsonText") `text` -> 输出文本（不会换行）
        - [**[]**](#1145 "list") `output` -> 列表内存在"head"、"value"、"pos"则输出对应的值（自动换行）
        - [**{}**](#1145 "dict") `set` -> 设置表头、值、操作
          - [**S**](#1145 "str") `head` -> 设置表头
          - [**I**](#1145 "int") `value` -> 设置指针所指向的值
          - [**S**](#1145 "str") `move` -> 设置操作（"L"左、"R"右、"N"空、"H"停机）


## 示例

查看 example.jst 文件了解基本用法。  

## 许可证

MIT License

## 关于
作者：FeSo4a  
版本：v1.0.0  
Github: https://github.com/FeSo4a  
Bilibili: https://space.bilibili.com/3546674548967510