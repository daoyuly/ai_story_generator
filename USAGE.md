# 故事生成系统使用说明

## 系统概述

这是一个基于大模型的多Agent协作故事生成系统，使用LangChain + LangGraph技术栈。系统包含四个专门的Agent：

1. **故事大纲Agent** - 根据故事要求生成详细大纲
2. **故事编写Agent** - 根据大纲编写具体章节
3. **读者Agent** - 阅读故事并提供评价和反馈
4. **主编Agent** - 根据读者反馈决定是否继续完善

## 安装和配置

### 1. 环境要求

- Python 3.9+
- uv包管理器

### 2. 安装依赖

```bash
# 安装项目依赖
uv sync
```

### 3. 配置环境变量

复制环境变量示例文件并配置：

```bash
cp env.example .env
```

编辑`.env`文件，设置您的OpenAI API密钥：

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 使用方法

### 方法1：交互式主程序

运行主程序，按提示输入故事要求：

```bash
uv run python main.py
```

### 方法2：演示脚本

运行演示脚本，查看系统功能：

```bash
uv run python demo.py
```

### 方法3：测试

运行基本测试：

```bash
uv run python tests/test_basic.py
```

## 系统工作流程

### 1. 故事要求输入
用户输入故事的基本要求：
- 故事类型（科幻、奇幻、悬疑等）
- 主题
- 目标读者
- 字数要求
- 章节数
- 最大迭代次数

### 2. 写作素材搜索
系统自动搜索相关的写作素材，包括：
- 角色设定素材
- 场景设定素材
- 情节发展素材
- 写作风格素材

### 3. 故事大纲生成
故事大纲Agent根据要求生成详细的故事大纲，包括：
- 故事基本信息
- 故事梗概
- 主要人物
- 章节大纲
- 写作要点

### 4. 故事编写
故事编写Agent根据大纲逐个编写章节：
- 提取章节信息
- 编写章节内容
- 控制字数
- 保持情节连贯

### 5. 读者评价
读者Agent阅读完整故事并提供评价：
- 多维度评价（情节、人物、语言、结构）
- 1-10分评分
- 具体改进建议
- 是否推荐继续完善

### 6. 主编决策
主编Agent根据读者反馈做出决策：
- 评估故事质量
- 判断是否需要继续完善
- 提供修改指导
- 决定是否结束迭代

### 7. 迭代优化
如果决定继续完善：
- 根据反馈修改大纲
- 重新编写故事
- 再次评价和决策
- 直到达到质量标准或最大迭代次数

## 数据存储

系统使用SQLite数据库存储所有数据：

- **故事要求表** - 存储用户输入的故事要求
- **故事大纲表** - 存储各版本的故事大纲
- **故事章节表** - 存储各版本的章节内容
- **读者反馈表** - 存储读者评价和评分

数据库文件位置：`data/story_generator.db`

## 输出文件

生成的故事会保存为Markdown格式：

- 位置：`output/`目录
- 格式：`{主题}_{时间戳}.md`
- 内容：包含完整故事、评分、迭代信息

## 配置选项

### 模型配置

可以在Agent中修改模型参数：

```python
# 在agents文件中修改
self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # 可改为gpt-4
    temperature=0.7,         # 控制创造性
    api_key=os.getenv("OPENAI_API_KEY")
)
```

### 迭代配置

- 默认最大迭代次数：5次
- 评分达到9分以上自动结束
- 可自定义最大迭代次数

### 搜索配置

- 默认搜索结果数：5个
- 搜索类别：角色、场景、情节、写作风格
- 可自定义搜索参数

## 故障排除

### 常见问题

1. **API密钥错误**
   - 检查`.env`文件中的API密钥是否正确
   - 确保API密钥有足够的额度

2. **依赖安装失败**
   - 确保使用uv包管理器
   - 检查Python版本是否为3.9+

3. **数据库错误**
   - 检查`data`目录是否存在
   - 确保有写入权限

4. **网络连接问题**
   - 检查网络连接
   - 如果在中国大陆，可能需要配置代理

### 调试模式

可以启用详细日志输出：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 扩展功能

### 添加新的故事类型

在`src/utils/search_tools.py`中添加新的故事类型处理：

```python
elif story_type == "新类型":
    prompts.extend([
        # 添加新类型的写作提示
    ])
```

### 自定义评价标准

在`src/agents/reader_agent.py`中修改评价标准：

```python
def _extract_score(self, evaluation: str) -> float:
    # 修改评分提取逻辑
```

### 添加新的搜索源

在`src/utils/search_tools.py`中添加新的搜索源：

```python
def search_custom_source(self, query: str):
    # 实现新的搜索方法
```

## 性能优化

### 并行处理

可以启用并行处理来提高性能：

```python
# 在workflow中添加并行节点
workflow.add_node("parallel_search", self._parallel_search)
```

### 缓存机制

可以添加缓存来避免重复搜索：

```python
# 实现搜索结果缓存
self.cache = {}
```

## 贡献指南

欢迎提交Issue和Pull Request来改进系统！

### 开发环境设置

```bash
# 安装开发依赖
uv sync --dev

# 运行测试
uv run pytest

# 代码格式化
uv run black src/
uv run isort src/
```

## 许可证

本项目采用MIT许可证。
