from typing import List, Dict, Any
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import json


class SearchTools:
    """搜索工具类，用于寻找写作素材"""
    
    def __init__(self):
        self.ddgs = DDGS()
    
    def search_writing_materials(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """搜索写作素材"""
        try:
            results = []
            search_results = self.ddgs.text(query, max_results=max_results)
            
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'content': result.get('body', ''),
                    'url': result.get('href', ''),
                    'source': 'duckduckgo'
                })
            
            return results
        except Exception as e:
            print(f"搜索出错: {e}")
            return []
    
    def search_story_elements(self, story_type: str, theme: str) -> Dict[str, Any]:
        """搜索故事元素"""
        materials = {
            'characters': [],
            'settings': [],
            'plot_elements': [],
            'writing_style': []
        }
        
        # 搜索角色相关素材
        character_query = f"{story_type} {theme} 角色设定 人物性格"
        character_results = self.search_writing_materials(character_query, 3)
        materials['characters'] = character_results
        
        # 搜索场景设定
        setting_query = f"{story_type} {theme} 场景设定 环境描写"
        setting_results = self.search_writing_materials(setting_query, 3)
        materials['settings'] = setting_results
        
        # 搜索情节元素
        plot_query = f"{story_type} {theme} 情节发展 故事结构"
        plot_results = self.search_writing_materials(plot_query, 3)
        materials['plot_elements'] = plot_results
        
        # 搜索写作风格
        style_query = f"{story_type} 写作技巧 文风特点"
        style_results = self.search_writing_materials(style_query, 3)
        materials['writing_style'] = style_results
        
        return materials
    
    def get_writing_prompts(self, story_type: str, theme: str) -> List[str]:
        """获取写作提示"""
        prompts = []
        
        # 根据故事类型生成提示
        if story_type == "科幻":
            prompts.extend([
                f"在{theme}的科幻背景下，设计一个引人入胜的开头",
                f"描述{theme}世界中的科技元素",
                f"创造{theme}主题下的未来社会结构"
            ])
        elif story_type == "奇幻":
            prompts.extend([
                f"在{theme}的奇幻世界中，设计魔法系统",
                f"描述{theme}主题下的神秘生物",
                f"创造{theme}背景下的冒险情节"
            ])
        elif story_type == "悬疑":
            prompts.extend([
                f"在{theme}的悬疑故事中，设计谜团线索",
                f"描述{theme}主题下的紧张氛围",
                f"创造{theme}背景下的推理过程"
            ])
        else:
            prompts.extend([
                f"在{theme}的{story_type}故事中，设计引人入胜的情节",
                f"描述{theme}主题下的情感冲突",
                f"创造{theme}背景下的角色发展"
            ])
        
        return prompts
    
    def extract_keywords(self, text: str) -> List[str]:
        """从文本中提取关键词"""
        # 简单的关键词提取（可以后续优化为更复杂的NLP方法）
        common_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        
        words = text.split()
        keywords = [word for word in words if len(word) > 1 and word not in common_words]
        
        # 返回前10个关键词
        return keywords[:10]
    
    def generate_search_queries(self, story_type: str, theme: str, target_reader: str) -> List[str]:
        """根据故事要求生成搜索查询"""
        queries = [
            f"{story_type} {theme} 写作技巧",
            f"{story_type} {theme} {target_reader} 适合",
            f"{story_type} 故事结构 大纲",
            f"{theme} 背景设定 世界观",
            f"{story_type} 角色塑造 人物性格"
        ]
        return queries
