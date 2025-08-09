# 故事生成系统

基于大模型的多Agent协作故事生成系统，使用LangChain + LangGraph技术栈。


## 🎯 项目特色

- **多Agent协作**：四个专门Agent各司其职，协同工作
- **智能迭代优化**：通过读者反馈不断优化故事质量
- **数据持久化**：使用SQLite存储完整的故事生成过程
- **搜索素材**：自动搜索相关写作素材，提升故事质量
- **灵活配置**：支持自定义故事类型、字数、章节等参数

## 🏗️ 系统架构

### 四个核心Agent

1. **故事大纲Agent** 📝
   - 根据故事要求生成详细大纲
   - 支持根据反馈修改大纲
   - 确保故事结构完整

2. **故事编写Agent** ✍️
   - 根据大纲编写具体章节
   - 控制字数，保持情节连贯
   - 体现故事类型特点

3. **读者Agent** 📖
   - 从目标读者角度评价故事
   - 多维度评分（情节、人物、语言、结构）
   - 提供具体改进建议

4. **主编Agent** 🎯
   - 根据读者反馈做出决策
   - 判断是否需要继续完善
   - 提供修改指导

### 工作流程

```
用户输入 → 搜索素材 → 生成大纲 → 编写故事 → 读者评价 → 主编决策 → 迭代优化 → 输出最终故事
```

## 🚀 快速开始

### 方法1：使用启动脚本（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd story-generator

# 运行启动脚本
./start.sh
```

启动脚本会自动：
- 检查Python版本和uv包管理器
- 安装项目依赖
- 创建环境变量文件
- 运行基本测试
- 提供使用指导

### 方法2：手动安装

#### 1. 环境要求

- Python 3.9+
- uv包管理器

#### 2. 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd story-generator

# 安装依赖
uv sync
```

#### 3. 配置环境变量

```bash
# 复制环境变量文件
cp env.example .env

# 编辑.env文件，设置OpenAI API密钥
OPENAI_API_KEY=your_openai_api_key_here
```

#### 4. 运行系统

```bash
# 交互式主程序
uv run python main.py

# 或运行演示脚本
uv run python demo.py
```

## 📁 项目结构

```
story-generator/
├── src/
│   ├── agents/          # 四个核心Agent
│   │   ├── outline_agent.py    # 故事大纲Agent
│   │   ├── writer_agent.py     # 故事编写Agent
│   │   ├── reader_agent.py     # 读者Agent
│   │   └── editor_agent.py     # 主编Agent
│   ├── database/        # 数据库模型和操作
│   │   └── models.py
│   ├── graph/           # LangGraph工作流
│   │   └── story_workflow.py
│   └── utils/           # 工具函数
│       └── search_tools.py
├── data/                # 数据文件
├── tests/               # 测试文件
├── output/              # 输出文件
├── main.py              # 主程序入口
├── demo.py              # 演示脚本
└── USAGE.md             # 详细使用说明
```

## 🎮 使用示例

### 基本使用

1. 运行主程序：`uv run python main.py`
2. 选择故事类型（科幻、奇幻、悬疑等）
3. 输入故事主题
4. 选择目标读者
5. 设置字数要求和章节数
6. 系统自动生成故事

### 演示模式

```bash
uv run python demo.py
```

选择演示功能查看系统工作过程。

## 📊 数据存储

系统使用SQLite数据库存储所有数据：

- **故事要求表** - 用户输入的故事要求
- **故事大纲表** - 各版本的故事大纲
- **故事章节表** - 各版本的章节内容
- **读者反馈表** - 读者评价和评分

## 🔧 配置选项

### 模型配置

可在Agent中修改模型参数：

```python
self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # 可改为gpt-4
    temperature=0.7,         # 控制创造性
)
```

### 迭代配置

- 默认最大迭代次数：5次
- 评分达到9分以上自动结束
- 可自定义最大迭代次数

## 🧪 测试

```bash
# 运行基本测试
uv run python tests/test_basic.py
```

## 📚 详细文档

- [使用说明](USAGE.md) - 详细的使用指南
- [架构文档](arch.md) - 系统架构设计

## 🤝 贡献

欢迎提交Issue和Pull Request来改进系统！

### 开发环境

```bash
# 安装开发依赖
uv sync --dev

# 代码格式化
uv run black src/
uv run isort src/
```

## 📄 许可证

本项目采用MIT许可证。
