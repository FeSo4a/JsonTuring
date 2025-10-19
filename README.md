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
- `run <file>` - 运行指定的 [.jst](example.jst) 文件
- `read <file> <encoding>` - 读取并显示 [.jst](example.jst) 文件内容
- `color [<color>|info]` - 设置文字颜色或查看当前颜色
- `back [<background>|info]` - 设置背景颜色或查看当前背景
- `save` - 保存当前主题设置
- [clear](src\JsonTuring.py#L109-L113) - 清屏
- `about` - 显示作者信息
- `exit` - 退出程序

### JST 文件格式

JST 文件采用 JSON 格式，包含以下主要部分：

- `init`: 初始化配置
  - `head`: 初始状态
  - `value`: 初始值
  - `pos`: 初始位置
  - `max_size`: 磁带最大长度
- `ops`: 操作规则数组
  - `case`: 条件判断
  - [run](src\JsonTuring.py#L234-L368): 执行动作
    - `set`: 设置新状态
    - `output`: 输出信息
    - `text`: 显示文本

## 示例

查看 example.jst 文件了解基本用法。

## 许可证

MIT License

## 关于
作者：FeSo4a  
版本：v1.0.0  
Github: https://github.com/FeSo4a  
Bilibili: https://space.bilibili.com/3546674548967510