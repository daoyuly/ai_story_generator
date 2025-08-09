from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import sqlite3
from pathlib import Path


@dataclass
class StoryRequirement:
    """故事要求"""
    id: int
    story_type: str  # 故事类型
    theme: str       # 主题
    word_count: int  # 字数要求
    chapters: int    # 章节数
    target_reader: str  # 目标读者
    created_at: datetime
    status: str = "pending"  # pending, in_progress, completed


@dataclass
class StoryOutline:
    """故事大纲"""
    id: int
    requirement_id: int
    version: int
    outline_content: str
    created_at: datetime


@dataclass
class StoryChapter:
    """故事章节"""
    id: int
    requirement_id: int
    outline_id: int
    version: int
    chapter_number: int
    chapter_title: str
    chapter_content: str
    word_count: int
    created_at: datetime


@dataclass
class ReaderFeedback:
    """读者反馈"""
    id: int
    requirement_id: int
    version: int
    feedback_content: str
    score: float  # 1-10分
    suggestions: str
    created_at: datetime


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = "data/story_generator.db"):
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_database()
    
    def _ensure_db_directory(self):
        """确保数据库目录存在"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def _init_database(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 故事要求表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS story_requirements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    story_type TEXT NOT NULL,
                    theme TEXT NOT NULL,
                    word_count INTEGER NOT NULL,
                    chapters INTEGER NOT NULL,
                    target_reader TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 故事大纲表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS story_outlines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requirement_id INTEGER NOT NULL,
                    version INTEGER NOT NULL,
                    outline_content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (requirement_id) REFERENCES story_requirements (id)
                )
            """)
            
            # 故事章节表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS story_chapters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requirement_id INTEGER NOT NULL,
                    outline_id INTEGER NOT NULL,
                    version INTEGER NOT NULL,
                    chapter_number INTEGER NOT NULL,
                    chapter_title TEXT NOT NULL,
                    chapter_content TEXT NOT NULL,
                    word_count INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (requirement_id) REFERENCES story_requirements (id),
                    FOREIGN KEY (outline_id) REFERENCES story_outlines (id)
                )
            """)
            
            # 读者反馈表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reader_feedbacks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requirement_id INTEGER NOT NULL,
                    version INTEGER NOT NULL,
                    feedback_content TEXT NOT NULL,
                    score REAL NOT NULL,
                    suggestions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (requirement_id) REFERENCES story_requirements (id)
                )
            """)
            
            conn.commit()
    
    def create_story_requirement(self, story_type: str, theme: str, word_count: int, 
                                chapters: int, target_reader: str) -> int:
        """创建故事要求"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO story_requirements (story_type, theme, word_count, chapters, target_reader)
                VALUES (?, ?, ?, ?, ?)
            """, (story_type, theme, word_count, chapters, target_reader))
            conn.commit()
            return cursor.lastrowid
    
    def get_story_requirement(self, requirement_id: int) -> Optional[StoryRequirement]:
        """获取故事要求"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, story_type, theme, word_count, chapters, target_reader, 
                       created_at, status
                FROM story_requirements WHERE id = ?
            """, (requirement_id,))
            row = cursor.fetchone()
            if row:
                return StoryRequirement(*row)
            return None
    
    def save_story_outline(self, requirement_id: int, version: int, outline_content: str) -> int:
        """保存故事大纲"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO story_outlines (requirement_id, version, outline_content)
                VALUES (?, ?, ?)
            """, (requirement_id, version, outline_content))
            conn.commit()
            return cursor.lastrowid
    
    def get_latest_outline(self, requirement_id: int) -> Optional[StoryOutline]:
        """获取最新版本的故事大纲"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, requirement_id, version, outline_content, created_at
                FROM story_outlines 
                WHERE requirement_id = ? 
                ORDER BY version DESC 
                LIMIT 1
            """, (requirement_id,))
            row = cursor.fetchone()
            if row:
                return StoryOutline(*row)
            return None
    
    def save_story_chapter(self, requirement_id: int, outline_id: int, version: int,
                          chapter_number: int, chapter_title: str, chapter_content: str,
                          word_count: int) -> int:
        """保存故事章节"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO story_chapters (requirement_id, outline_id, version, 
                                          chapter_number, chapter_title, chapter_content, word_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (requirement_id, outline_id, version, chapter_number, chapter_title, 
                  chapter_content, word_count))
            conn.commit()
            return cursor.lastrowid
    
    def get_story_chapters(self, requirement_id: int, version: int) -> List[StoryChapter]:
        """获取指定版本的所有章节"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, requirement_id, outline_id, version, chapter_number, 
                       chapter_title, chapter_content, word_count, created_at
                FROM story_chapters 
                WHERE requirement_id = ? AND version = ?
                ORDER BY chapter_number
            """, (requirement_id, version))
            rows = cursor.fetchall()
            return [StoryChapter(*row) for row in rows]
    
    def save_reader_feedback(self, requirement_id: int, version: int, feedback_content: str,
                            score: float, suggestions: str) -> int:
        """保存读者反馈"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reader_feedbacks (requirement_id, version, feedback_content, 
                                           score, suggestions)
                VALUES (?, ?, ?, ?, ?)
            """, (requirement_id, version, feedback_content, score, suggestions))
            conn.commit()
            return cursor.lastrowid
    
    def get_latest_feedback(self, requirement_id: int) -> Optional[ReaderFeedback]:
        """获取最新的读者反馈"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, requirement_id, version, feedback_content, score, 
                       suggestions, created_at
                FROM reader_feedbacks 
                WHERE requirement_id = ? 
                ORDER BY version DESC 
                LIMIT 1
            """, (requirement_id,))
            row = cursor.fetchone()
            if row:
                return ReaderFeedback(*row)
            return None
    
    def update_story_status(self, requirement_id: int, status: str):
        """更新故事状态"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE story_requirements SET status = ? WHERE id = ?
            """, (status, requirement_id))
            conn.commit()
