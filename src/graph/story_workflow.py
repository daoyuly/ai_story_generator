from typing import Dict, Any, List, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.agents.outline_agent import OutlineAgent
from src.agents.writer_agent import WriterAgent
from src.agents.reader_agent import ReaderAgent
from src.agents.editor_agent import EditorAgent
from src.utils.search_tools import SearchTools
from src.database.models import DatabaseManager

import os
from dotenv import load_dotenv

load_dotenv()

class StoryState(TypedDict):
    """故事生成状态"""
    requirement_id: int
    story_requirement: Dict[str, Any]
    current_iteration: int
    max_iterations: int
    outline: str
    outline_id: int
    chapters: List[Dict[str, Any]]
    reader_feedback: Dict[str, Any]
    editor_decision: Dict[str, Any]
    writing_materials: Dict[str, Any]
    should_continue: bool
    final_story: str


class StoryWorkflow:
    """故事生成工作流"""
    
    def __init__(self):
        self.outline_agent = OutlineAgent(model_name=os.getenv("OUTLINE_AGENT_MODEL"))
        self.writer_agent = WriterAgent(model_name=os.getenv("WRITER_AGENT_MODEL"))
        self.reader_agent = ReaderAgent(model_name=os.getenv("READER_AGENT_MODEL"))
        self.editor_agent = EditorAgent(model_name=os.getenv("EDITOR_AGENT_MODEL"))
        self.search_tools = SearchTools()
        self.db_manager = DatabaseManager()
        
        # 创建工作流图
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """创建工作流图"""
        
        # 创建状态图
        workflow = StateGraph(StoryState)
        
        # 添加节点
        workflow.add_node("search_materials", self._search_materials)
        workflow.add_node("generate_outline", self._generate_outline)
        workflow.add_node("write_story", self._write_story)
        workflow.add_node("read_and_evaluate", self._read_and_evaluate)
        workflow.add_node("editor_decide", self._editor_decide)
        workflow.add_node("save_final_story", self._save_final_story)
        
        # 设置入口点
        workflow.set_entry_point("search_materials")
        
        # 添加边
        workflow.add_edge("search_materials", "generate_outline")
        workflow.add_edge("generate_outline", "write_story")
        workflow.add_edge("write_story", "read_and_evaluate")
        workflow.add_edge("read_and_evaluate", "editor_decide")
        
        # 条件边
        workflow.add_conditional_edges(
            "editor_decide",
            self._should_continue,
            {
                "continue": "generate_outline",
                "finish": "save_final_story"
            }
        )
        
        workflow.add_edge("save_final_story", END)
        
        return workflow.compile(checkpointer=MemorySaver())
    
    def _search_materials(self, state: StoryState) -> StoryState:
        """搜索写作素材"""
        print("🔍 正在搜索写作素材...")
        
        story_req = state["story_requirement"]
        materials = self.search_tools.search_story_elements(
            story_req["story_type"], 
            story_req["theme"]
        )
        
        state["writing_materials"] = materials
        print("✅ 写作素材搜索完成")
        return state
    
    def _generate_outline(self, state: StoryState) -> StoryState:
        """生成故事大纲"""
        print(f"📝 正在生成故事大纲 (第{state['current_iteration']}次迭代)...")
        
        story_req = state["story_requirement"]
        writing_materials = state.get("writing_materials", {})
        
        # 如果是第一次生成大纲
        if state["current_iteration"] == 1:
            outline = self.outline_agent.generate_outline(story_req, writing_materials)
        else:
            # 根据反馈修改大纲
            feedback = state["reader_feedback"]["evaluation"]
            outline = self.outline_agent.revise_outline(
                state["outline"], feedback, story_req
            )
        
        # 保存大纲到数据库
        outline_id = self.db_manager.save_story_outline(
            state["requirement_id"], 
            state["current_iteration"], 
            outline
        )
        
        state["outline"] = outline
        state["outline_id"] = outline_id
        print("✅ 故事大纲生成完成")
        return state
    
    def _write_story(self, state: StoryState) -> StoryState:
        """编写故事"""
        print(f"✍️ 正在编写故事 (第{state['current_iteration']}次迭代)...")
        
        story_req = state["story_requirement"]
        outline = state["outline"]
        chapters = []
        
        # 获取章节数量
        num_chapters = story_req["chapters"]
        
        for chapter_num in range(1, num_chapters + 1):
            print(f"  正在编写第{chapter_num}章...")
            
            # 提取章节信息
            chapter_info = self.writer_agent.extract_chapter_info_from_outline(
                outline, chapter_num
            )
            
            # 如果没有提取到字数，平均分配
            if chapter_info["word_count"] == 0:
                chapter_info["word_count"] = story_req["word_count"] // num_chapters
            
            # 获取前面章节的信息
            previous_chapters = chapters if chapters else None
            
            # 编写章节
            chapter_content = self.writer_agent.write_chapter(
                outline, chapter_info, story_req, previous_chapters
            )
            
            # 计算实际字数
            actual_word_count = len(chapter_content)
            
            # 保存章节到数据库
            chapter_id = self.db_manager.save_story_chapter(
                state["requirement_id"],
                state["outline_id"],
                state["current_iteration"],
                chapter_num,
                chapter_info["title"],
                chapter_content,
                actual_word_count
            )
            
            chapters.append({
                "title": chapter_info["title"],
                "content": chapter_content,
                "word_count": actual_word_count,
                "summary": chapter_info["summary"]
            })
        
        state["chapters"] = chapters
        print("✅ 故事编写完成")
        return state
    
    def _read_and_evaluate(self, state: StoryState) -> StoryState:
        """阅读和评价故事"""
        print(f"📖 正在阅读和评价故事 (第{state['current_iteration']}次迭代)...")
        
        story_req = state["story_requirement"]
        chapters = state["chapters"]
        
        # 读者评价
        feedback = self.reader_agent.read_and_evaluate(chapters, story_req)
        
        # 保存读者反馈到数据库
        feedback_id = self.db_manager.save_reader_feedback(
            state["requirement_id"],
            state["current_iteration"],
            feedback["evaluation"],
            feedback["score"],
            feedback.get("suggestions", "")
        )
        
        state["reader_feedback"] = feedback
        print(f"✅ 读者评价完成，评分：{feedback['score']}/10")
        return state
    
    def _editor_decide(self, state: StoryState) -> StoryState:
        """主编决策"""
        print(f"🎯 主编正在评估和决策 (第{state['current_iteration']}次迭代)...")
        
        story_req = state["story_requirement"]
        reader_feedback = state["reader_feedback"]
        
        # 主编决策
        decision = self.editor_agent.evaluate_feedback_and_decide(
            reader_feedback,
            story_req,
            state["current_iteration"],
            state["max_iterations"]
        )
        
        state["editor_decision"] = decision
        state["should_continue"] = decision["should_continue"]
        
        if decision["should_continue"]:
            state["current_iteration"] += 1
            print(f"🔄 决定继续完善，进入第{state['current_iteration']}次迭代")
        else:
            print("🏁 决定完成故事")
        
        return state
    
    def _should_continue(self, state: StoryState) -> str:
        """判断是否应该继续"""
        return "continue" if state["should_continue"] else "finish"
    
    def _save_final_story(self, state: StoryState) -> StoryState:
        """保存最终故事"""
        print("💾 正在保存最终故事...")
        
        # 构建最终故事内容
        final_story = f"# {state['story_requirement']['theme']}\n\n"
        final_story += f"**故事类型：**{state['story_requirement']['story_type']}\n"
        final_story += f"**目标读者：**{state['story_requirement']['target_reader']}\n"
        final_story += f"**总字数：**{state['story_requirement']['word_count']}\n\n"
        
        for i, chapter in enumerate(state["chapters"], 1):
            final_story += f"## 第{i}章：{chapter['title']}\n\n"
            final_story += f"{chapter['content']}\n\n"
            final_story += f"*字数：{chapter['word_count']}*\n\n"
        
        final_story += f"\n---\n"
        final_story += f"**最终评分：**{state['reader_feedback']['score']}/10\n"
        final_story += f"**迭代次数：**{state['current_iteration']}\n"
        
        state["final_story"] = final_story
        
        # 更新故事状态为完成
        self.db_manager.update_story_status(state["requirement_id"], "completed")
        
        print("✅ 最终故事保存完成")
        return state
    
    def run(self, story_requirement: Dict[str, Any], max_iterations: int = 5) -> Dict[str, Any]:
        """运行故事生成工作流"""
        
        # 创建故事要求
        requirement_id = self.db_manager.create_story_requirement(
            story_requirement["story_type"],
            story_requirement["theme"],
            story_requirement["word_count"],
            story_requirement["chapters"],
            story_requirement["target_reader"]
        )
        
        # 初始化状态
        initial_state = StoryState(
            requirement_id=requirement_id,
            story_requirement=story_requirement,
            current_iteration=1,
            max_iterations=max_iterations,
            outline="",
            outline_id=0,
            chapters=[],
            reader_feedback={},
            editor_decision={},
            writing_materials={},
            should_continue=True,
            final_story=""
        )
        
        # 运行工作流
        print("🚀 开始故事生成工作流...")
        print(f"📋 故事要求：{story_requirement['story_type']} - {story_requirement['theme']}")
        print(f"👥 目标读者：{story_requirement['target_reader']}")
        print(f"📝 字数要求：{story_requirement['word_count']}")
        print(f"📚 章节数：{story_requirement['chapters']}")
        print(f"🔄 最大迭代次数：{max_iterations}")
        print("-" * 50)
        
        result = self.workflow.invoke(
            initial_state,
            config={"configurable": {"thread_id": f"story-{requirement_id}"}}
        )
        
        print("-" * 50)
        print("🎉 故事生成工作流完成！")
        
        return {
            "requirement_id": requirement_id,
            "final_story": result["final_story"],
            "final_score": result["reader_feedback"]["score"],
            "iterations": result["current_iteration"],
            "chapters": result["chapters"]
        }
