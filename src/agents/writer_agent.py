from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()


class WriterAgent:
    """故事编写Agent"""
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.8,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def write_chapter(self, outline: str, chapter_info: Dict[str, Any], 
                     story_requirement: Dict[str, Any], 
                     previous_chapters: List[Dict[str, Any]] = None) -> str:
        """编写单个章节"""
        
        system_prompt = """你是一位专业的小说创作专家。你需要根据故事大纲和章节信息创作具体的故事内容。

创作要求：
1. 严格按照章节信息中的字数要求控制篇幅
2. 保持与大纲的一致性
3. 语言生动，情节引人入胜
4. 符合目标读者的阅读习惯
5. 体现故事类型的特点
6. 如果有前面的章节，要保持情节的连贯性

输出格式：
请直接输出章节内容，不需要额外的格式标记。"""

        # 构建用户输入
        user_input = f"""
故事要求：
- 故事类型：{story_requirement['story_type']}
- 主题：{story_requirement['theme']}
- 目标读者：{story_requirement['target_reader']}
- 总字数：{story_requirement['word_count']}

故事大纲：
{outline}

当前章节信息：
- 章节标题：{chapter_info['title']}
- 字数要求：{chapter_info['word_count']}
- 内容概要：{chapter_info['summary']}

"""

        # 如果有前面的章节，添加上下文
        if previous_chapters:
            user_input += "\n前面章节概要：\n"
            for i, chapter in enumerate(previous_chapters, 1):
                user_input += f"第{i}章《{chapter['title']}》：{chapter['summary'][:100]}...\n"
            user_input += "\n请确保与前面章节的情节保持连贯。\n"

        user_input += "\n请根据以上信息创作这个章节的具体内容。"

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def revise_chapter(self, original_chapter: str, feedback: str, 
                      chapter_info: Dict[str, Any], 
                      story_requirement: Dict[str, Any]) -> str:
        """根据反馈修改章节"""
        
        system_prompt = """你是一位专业的小说修改专家。你需要根据读者反馈对原有章节进行修改。

修改要求：
1. 保持原有章节的基本结构和核心情节
2. 根据反馈意见进行有针对性的修改
3. 确保修改后的内容更符合目标读者需求
4. 保持与大纲的一致性
5. 控制好字数，不要大幅超出原定字数

请输出修改后的完整章节内容。"""

        user_input = f"""
原始章节内容：
{original_chapter}

读者反馈：
{feedback}

章节信息：
- 章节标题：{chapter_info['title']}
- 字数要求：{chapter_info['word_count']}
- 内容概要：{chapter_info['summary']}

故事要求：
- 故事类型：{story_requirement['story_type']}
- 主题：{story_requirement['theme']}
- 目标读者：{story_requirement['target_reader']}

请根据读者反馈修改章节内容。
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def extract_chapter_info_from_outline(self, outline: str, chapter_number: int) -> Dict[str, Any]:
        """从大纲中提取章节信息"""
        # 这里可以添加更复杂的解析逻辑
        # 目前使用简单的文本处理
        lines = outline.split('\n')
        chapter_info = {
            'title': f"第{chapter_number}章",
            'word_count': 0,
            'summary': ''
        }
        
        # 简单的章节信息提取
        for line in lines:
            if f"第{chapter_number}章" in line or f"### 第{chapter_number}章" in line:
                chapter_info['title'] = line.strip().replace('#', '').strip()
            elif "字数要求" in line and chapter_info['word_count'] == 0:
                try:
                    word_count = int(line.split('：')[1].strip())
                    chapter_info['word_count'] = word_count
                except:
                    pass
            elif "内容概要" in line:
                chapter_info['summary'] = line.split('：')[1].strip()
        
        return chapter_info
