from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()


class ReaderAgent:
    """读者Agent"""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.5,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def read_and_evaluate(self, story_chapters: List[Dict[str, Any]], 
                         story_requirement: Dict[str, Any]) -> Dict[str, Any]:
        """阅读故事并评价"""
        
        system_prompt = """你是一位专业的文学评论家和读者代表。你需要阅读故事并提供详细的评价。

评价要求：
1. 从目标读者的角度进行评价
2. 评价要客观、具体、有建设性
3. 从多个维度进行评价：情节、人物、语言、结构等
4. 给出1-10分的评分（10分为满分）
5. 提供具体的改进建议
6. 评价要符合故事类型和目标读者的特点

输出格式：
请按照以下格式输出评价：

## 总体评价
[总体评价内容]

## 评分
[1-10分，并说明评分理由]

## 详细评价
### 情节方面
[情节评价]

### 人物方面
[人物评价]

### 语言方面
[语言评价]

### 结构方面
[结构评价]

## 改进建议
[具体的改进建议]

## 是否推荐继续完善
[是/否，并说明理由]"""

        # 构建故事内容
        story_content = ""
        for i, chapter in enumerate(story_chapters, 1):
            story_content += f"\n\n第{i}章：{chapter['title']}\n"
            story_content += f"{chapter['content']}\n"
            story_content += f"字数：{chapter['word_count']}\n"

        user_input = f"""
故事要求：
- 故事类型：{story_requirement['story_type']}
- 主题：{story_requirement['theme']}
- 目标读者：{story_requirement['target_reader']}
- 总字数：{story_requirement['word_count']}
- 章节数：{story_requirement['chapters']}

故事内容：
{story_content}

请从目标读者的角度对这篇故事进行详细评价。
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.invoke(messages)
        evaluation = response.content
        
        # 解析评分
        score = self._extract_score(evaluation)
        
        # 解析是否推荐继续完善
        should_continue = self._extract_should_continue(evaluation)
        
        return {
            'evaluation': evaluation,
            'score': score,
            'should_continue': should_continue
        }
    
    def _extract_score(self, evaluation: str) -> float:
        """从评价中提取评分"""
        try:
            # 查找评分
            lines = evaluation.split('\n')
            for line in lines:
                if '评分' in line or '分数' in line:
                    # 提取数字
                    import re
                    numbers = re.findall(r'\d+\.?\d*', line)
                    if numbers:
                        score = float(numbers[0])
                        if 1 <= score <= 10:
                            return score
            
            # 如果没有找到明确的评分，返回默认值
            return 7.0
        except:
            return 7.0
    
    def _extract_should_continue(self, evaluation: str) -> bool:
        """从评价中提取是否应该继续完善"""
        try:
            lower_eval = evaluation.lower()
            if '是' in lower_eval and ('继续' in lower_eval or '完善' in lower_eval):
                return True
            elif '否' in lower_eval and ('继续' in lower_eval or '完善' in lower_eval):
                return False
            
            # 根据评分判断
            score = self._extract_score(evaluation)
            return score < 8.0  # 评分低于8分建议继续完善
        except:
            return True
    
    def provide_feedback_for_revision(self, evaluation: str, 
                                    story_requirement: Dict[str, Any]) -> str:
        """为修改提供具体的反馈建议"""
        
        system_prompt = """你是一位专业的文学编辑。你需要根据读者评价为故事修改提供具体的指导建议。

要求：
1. 建议要具体、可操作
2. 要针对评价中提到的问题
3. 要符合故事类型和目标读者特点
4. 要给出明确的修改方向
5. 建议要简洁明了"""

        user_input = f"""
读者评价：
{evaluation}

故事要求：
- 故事类型：{story_requirement['story_type']}
- 主题：{story_requirement['theme']}
- 目标读者：{story_requirement['target_reader']}

请根据读者评价提供具体的修改建议。
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
