from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()


class EditorAgent:
    """主编Agent"""
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def evaluate_feedback_and_decide(self, reader_feedback: Dict[str, Any], 
                                   story_requirement: Dict[str, Any],
                                   current_iteration: int, 
                                   max_iterations: int = 5) -> Dict[str, Any]:
        """评估读者反馈并决定是否继续完善"""
        
        system_prompt = """你是一位资深的主编，负责根据读者反馈和故事要求决定是否继续完善故事。

决策标准：
1. 读者评分是否达到9分以上
2. 是否已达到最大迭代次数
3. 读者反馈是否表明故事质量已经很高
4. 修改建议是否具有可操作性
5. 是否符合故事要求和目标读者需求

输出格式：
请按照以下格式输出决策：

## 决策结果
[继续完善/完成故事]

## 决策理由
[详细的决策理由]

## 修改指导
[如果继续完善，给出具体的修改指导]

## 下一步行动
[具体的下一步行动计划]"""

        user_input = f"""
故事要求：
- 故事类型：{story_requirement['story_type']}
- 主题：{story_requirement['theme']}
- 目标读者：{story_requirement['target_reader']}
- 总字数：{story_requirement['word_count']}
- 章节数：{story_requirement['chapters']}

读者反馈：
- 评分：{reader_feedback['score']}/10
- 评价：{reader_feedback['evaluation']}
- 是否建议继续完善：{reader_feedback['should_continue']}

当前状态：
- 当前迭代次数：{current_iteration}
- 最大迭代次数：{max_iterations}

请根据以上信息做出决策。
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.invoke(messages)
        decision = response.content
        
        # 解析决策结果
        should_continue = self._parse_decision(decision, reader_feedback, current_iteration, max_iterations)
        
        return {
            'decision': decision,
            'should_continue': should_continue,
            'modification_guidance': self._extract_modification_guidance(decision)
        }
    
    def _parse_decision(self, decision: str, reader_feedback: Dict[str, Any], 
                       current_iteration: int, max_iterations: int) -> bool:
        """解析决策结果"""
        try:
            # 检查是否达到最大迭代次数
            if current_iteration >= max_iterations:
                return False
            
            # 检查评分是否达到9分以上
            if reader_feedback['score'] >= 9.0:
                return False
            
            # 检查决策文本
            lower_decision = decision.lower()
            if '完成' in lower_decision and '故事' in lower_decision:
                return False
            elif '继续' in lower_decision and '完善' in lower_decision:
                return True
            
            # 根据评分和读者建议判断
            if reader_feedback['score'] < 7.0 or reader_feedback['should_continue']:
                return True
            
            return False
        except:
            return True
    
    def _extract_modification_guidance(self, decision: str) -> str:
        """提取修改指导"""
        try:
            lines = decision.split('\n')
            guidance = ""
            in_guidance = False
            
            for line in lines:
                if '修改指导' in line:
                    in_guidance = True
                    continue
                elif in_guidance and line.strip().startswith('##'):
                    break
                elif in_guidance:
                    guidance += line + '\n'
            
            return guidance.strip() if guidance else "根据读者反馈进行针对性修改"
        except:
            return "根据读者反馈进行针对性修改"
    
    def provide_revision_plan(self, reader_feedback: Dict[str, Any], 
                            story_requirement: Dict[str, Any]) -> str:
        """提供修改计划"""
        
        system_prompt = """你是一位专业的文学编辑，需要根据读者反馈制定详细的修改计划。

要求：
1. 计划要具体、可操作
2. 要针对读者反馈中的问题
3. 要符合故事类型和目标读者特点
4. 要给出明确的修改优先级
5. 要考虑到故事的整体性"""

        user_input = f"""
读者反馈：
- 评分：{reader_feedback['score']}/10
- 评价：{reader_feedback['evaluation']}

故事要求：
- 故事类型：{story_requirement['story_type']}
- 主题：{story_requirement['theme']}
- 目标读者：{story_requirement['target_reader']}

请制定详细的修改计划。
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
