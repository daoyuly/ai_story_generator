from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()


class OutlineAgent:
    """故事大纲Agent"""
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def generate_outline(self, story_requirement: Dict[str, Any], 
                        writing_materials: Dict[str, Any] = None) -> str:
        """生成故事大纲"""
        
        # 构建提示模板
        system_prompt = """你是一位专业的故事大纲创作专家。你需要根据故事要求创作一个详细的故事大纲。

创作要求：
1. 大纲要结构清晰，层次分明
2. 每个章节都要有明确的标题和内容概要
3. 要符合目标读者的阅读习惯
4. 要体现故事的主题和类型特点
5. 要控制好字数分配，确保总字数符合要求

输出格式：
请按照以下格式输出大纲：

# 故事大纲

## 故事基本信息
- 类型：[故事类型]
- 主题：[主题]
- 目标读者：[目标读者]
- 总字数：[总字数]
- 章节数：[章节数]

## 故事梗概
[简要描述整个故事的核心情节]

## 主要人物
[列出主要人物及其特点]

## 章节大纲

### 第一章：[章节标题]
- 字数要求：[字数]
- 内容概要：[详细描述本章节的主要内容]

### 第二章：[章节标题]
- 字数要求：[字数]
- 内容概要：[详细描述本章节的主要内容]

[继续其他章节...]

## 写作要点
[列出写作时需要注意的要点]"""

        # 构建用户输入
        user_input = f"""
故事要求：
- 故事类型：{story_requirement['story_type']}
- 主题：{story_requirement['theme']}
- 目标读者：{story_requirement['target_reader']}
- 总字数：{story_requirement['word_count']}
- 章节数：{story_requirement['chapters']}

请根据以上要求创作一个详细的故事大纲。
"""

        # 如果有写作素材，添加到输入中
        if writing_materials:
            user_input += f"\n\n写作素材参考：\n"
            for category, materials in writing_materials.items():
                if materials:
                    user_input += f"\n{category}素材：\n"
                    for material in materials[:2]:  # 只取前2个素材
                        user_input += f"- {material.get('title', '')}: {material.get('content', '')[:200]}...\n"

        # 生成大纲
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def revise_outline(self, original_outline: str, feedback: str, 
                      story_requirement: Dict[str, Any]) -> str:
        """根据反馈修改大纲"""
        
        system_prompt = """你是一位专业的故事大纲修改专家。你需要根据读者反馈对原有大纲进行修改。

修改要求：
1. 保持原有大纲的基本结构
2. 根据反馈意见进行有针对性的修改
3. 确保修改后的内容更符合目标读者需求
4. 保持故事的整体连贯性
5. 确保字数分配合理

请输出修改后的完整大纲。"""

        user_input = f"""
原始大纲：
{original_outline}

读者反馈：
{feedback}

故事要求：
- 故事类型：{story_requirement['story_type']}
- 主题：{story_requirement['theme']}
- 目标读者：{story_requirement['target_reader']}
- 总字数：{story_requirement['word_count']}
- 章节数：{story_requirement['chapters']}

请根据读者反馈修改大纲。
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
