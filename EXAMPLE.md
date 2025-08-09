# 故事生成系统使用示例

## 🎯 示例1：生成科幻短篇故事

### 输入参数
- 故事类型：科幻
- 主题：人工智能与人类共存
- 目标读者：青少年
- 字数要求：2000字
- 章节数：2章
- 最大迭代次数：3次

### 运行命令
```bash
uv run python demo.py
# 选择选项1：完整故事生成演示
```

### 预期输出
```
🚀 开始故事生成工作流...
📋 故事要求：科幻 - 人工智能与人类共存
👥 目标读者：青少年
📝 字数要求：2000
📚 章节数：2
🔄 最大迭代次数：3
--------------------------------------------------
🔍 正在搜索写作素材...
✅ 写作素材搜索完成
📝 正在生成故事大纲 (第1次迭代)...
✅ 故事大纲生成完成
✍️ 正在编写故事 (第1次迭代)...
  正在编写第1章...
  正在编写第2章...
✅ 故事编写完成
📖 正在阅读和评价故事 (第1次迭代)...
✅ 读者评价完成，评分：7.5/10
🎯 主编正在评估和决策 (第1次迭代)...
🔄 决定继续完善，进入第2次迭代
...
🎉 故事生成完成！
📊 最终评分：8.5/10
🔄 迭代次数：2
📚 章节数：2
```

## 🎯 示例2：生成奇幻中篇故事

### 输入参数
- 故事类型：奇幻
- 主题：魔法学院的神秘事件
- 目标读者：成年人
- 字数要求：6000字
- 章节数：5章
- 最大迭代次数：5次

### 运行命令
```bash
uv run python main.py
# 按提示输入参数
```

## 🎯 示例3：生成悬疑故事

### 输入参数
- 故事类型：悬疑
- 主题：密室杀人案
- 目标读者：成年人
- 字数要求：4000字
- 章节数：3章
- 最大迭代次数：4次

## 📊 输出文件示例

### 生成的故事文件
```markdown
# 人工智能与人类共存

**故事类型：**科幻
**目标读者：**青少年
**总字数：**2000

## 第1章：初遇

[故事内容...]

*字数：1000*

## 第2章：共存之路

[故事内容...]

*字数：1000*

---

**最终评分：**8.5/10
**迭代次数：**2
```

### 数据库记录
系统会在`data/story_generator.db`中保存：
- 故事要求记录
- 各版本的故事大纲
- 各版本的章节内容
- 读者反馈记录

## 🔧 自定义配置示例

### 修改模型参数
```python
# 在src/agents/outline_agent.py中
self.llm = ChatOpenAI(
    model="gpt-4",  # 使用GPT-4
    temperature=0.8,  # 提高创造性
    api_key=os.getenv("OPENAI_API_KEY")
)
```

### 修改迭代条件
```python
# 在src/graph/story_workflow.py中
def _parse_decision(self, decision: str, reader_feedback: Dict[str, Any], 
                   current_iteration: int, max_iterations: int) -> bool:
    # 修改评分阈值
    if reader_feedback['score'] >= 8.5:  # 从9.0改为8.5
        return False
```

### 添加新的故事类型
```python
# 在src/utils/search_tools.py中
elif story_type == "恐怖":
    prompts.extend([
        f"在{theme}的恐怖故事中，营造紧张氛围",
        f"描述{theme}主题下的恐怖元素",
        f"创造{theme}背景下的惊悚情节"
    ])
```

## 🎨 高级用法

### 批量生成故事
```python
from src.graph.story_workflow import StoryWorkflow

workflow = StoryWorkflow()

stories = [
    {
        "story_type": "科幻",
        "theme": "时间旅行",
        "target_reader": "青少年",
        "word_count": 2000,
        "chapters": 2
    },
    {
        "story_type": "奇幻",
        "theme": "龙与魔法",
        "target_reader": "成年人",
        "word_count": 4000,
        "chapters": 3
    }
]

for i, story_req in enumerate(stories):
    print(f"生成第{i+1}个故事...")
    result = workflow.run(story_req, max_iterations=3)
    print(f"故事{i+1}完成，评分：{result['final_score']}/10")
```

### 自定义搜索源
```python
# 在src/utils/search_tools.py中添加
def search_custom_source(self, query: str):
    # 实现自定义搜索逻辑
    pass
```

## 📈 性能优化建议

1. **并行处理**：可以修改工作流支持并行章节生成
2. **缓存机制**：添加搜索结果缓存避免重复搜索
3. **模型选择**：根据需求选择不同的模型（GPT-3.5 vs GPT-4）
4. **批量处理**：一次性生成多个故事提高效率

## 🐛 常见问题解决

### 问题1：API密钥错误
```
❌ 错误：未设置OPENAI_API_KEY环境变量
```
**解决方案**：检查`.env`文件中的API密钥是否正确

### 问题2：依赖安装失败
```
❌ 依赖安装失败
```
**解决方案**：确保使用uv包管理器，检查Python版本

### 问题3：搜索功能异常
```
❌ 搜索出错
```
**解决方案**：检查网络连接，可能需要配置代理

### 问题4：数据库错误
```
❌ 数据库错误
```
**解决方案**：检查`data`目录权限，确保有写入权限
