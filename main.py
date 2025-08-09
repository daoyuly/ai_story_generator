#!/usr/bin/env python3
"""
故事生成系统主程序
基于大模型的多Agent协作故事生成系统
"""

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from graph.story_workflow import StoryWorkflow
from database.models import DatabaseManager

load_dotenv()


def get_story_requirement() -> Dict[str, Any]:
    """获取用户输入的故事要求"""
    print("📝 故事生成系统")
    print("=" * 50)
    
    # 故事类型选择
    print("\n请选择故事类型：")
    print("1. 科幻")
    print("2. 奇幻")
    print("3. 悬疑")
    print("4. 言情")
    print("5. 历史")
    print("6. 其他")
    
    story_types = ["科幻", "奇幻", "悬疑", "言情", "历史", "其他"]
    while True:
        try:
            choice = int(input("请输入选择 (1-6): "))
            if 1 <= choice <= 6:
                story_type = story_types[choice - 1]
                break
            else:
                print("❌ 请输入1-6之间的数字")
        except ValueError:
            print("❌ 请输入有效的数字")
    
    # 主题输入
    theme = input("\n请输入故事主题 (例如：人工智能、魔法世界、侦探破案等): ").strip()
    if not theme:
        theme = "未知主题"
    
    # 目标读者
    print("\n请选择目标读者：")
    print("1. 儿童 (6-12岁)")
    print("2. 青少年 (13-18岁)")
    print("3. 成年人 (18岁以上)")
    print("4. 全年龄段")
    
    reader_types = ["儿童", "青少年", "成年人", "全年龄段"]
    while True:
        try:
            choice = int(input("请输入选择 (1-4): "))
            if 1 <= choice <= 4:
                target_reader = reader_types[choice - 1]
                break
            else:
                print("❌ 请输入1-4之间的数字")
        except ValueError:
            print("❌ 请输入有效的数字")
    
    # 字数要求
    print("\n请选择字数要求：")
    print("1. 短篇 (1000-3000字)")
    print("2. 中篇 (3000-10000字)")
    print("3. 长篇 (10000-50000字)")
    print("4. 自定义")
    
    word_count_options = [2000, 6000, 25000, 0]
    while True:
        try:
            choice = int(input("请输入选择 (1-4): "))
            if 1 <= choice <= 4:
                if choice == 4:
                    word_count = int(input("请输入自定义字数: "))
                else:
                    word_count = word_count_options[choice - 1]
                break
            else:
                print("❌ 请输入1-4之间的数字")
        except ValueError:
            print("❌ 请输入有效的数字")
    
    # 章节数
    print("\n请选择章节数：")
    print("1. 短篇 (1-3章)")
    print("2. 中篇 (3-8章)")
    print("3. 长篇 (8-15章)")
    print("4. 自定义")
    
    chapter_options = [2, 5, 10, 0]
    while True:
        try:
            choice = int(input("请输入选择 (1-4): "))
            if 1 <= choice <= 4:
                if choice == 4:
                    chapters = int(input("请输入自定义章节数: "))
                else:
                    chapters = chapter_options[choice - 1]
                break
            else:
                print("❌ 请输入1-4之间的数字")
        except ValueError:
            print("❌ 请输入有效的数字")
    
    # 最大迭代次数
    print("\n请选择最大迭代次数：")
    print("1. 3次 (快速生成)")
    print("2. 5次 (标准生成)")
    print("3. 8次 (精细生成)")
    print("4. 自定义")
    
    iteration_options = [3, 5, 8, 0]
    while True:
        try:
            choice = int(input("请输入选择 (1-4): "))
            if 1 <= choice <= 4:
                if choice == 4:
                    max_iterations = int(input("请输入自定义迭代次数: "))
                else:
                    max_iterations = iteration_options[choice - 1]
                break
            else:
                print("❌ 请输入1-4之间的数字")
        except ValueError:
            print("❌ 请输入有效的数字")
    
    return {
        "story_type": story_type,
        "theme": theme,
        "target_reader": target_reader,
        "word_count": word_count,
        "chapters": chapters,
        "max_iterations": max_iterations
    }


def display_story_requirement(requirement: Dict[str, Any]):
    """显示故事要求"""
    print("\n📋 故事要求确认：")
    print("-" * 30)
    print(f"故事类型：{requirement['story_type']}")
    print(f"主题：{requirement['theme']}")
    print(f"目标读者：{requirement['target_reader']}")
    print(f"字数要求：{requirement['word_count']}字")
    print(f"章节数：{requirement['chapters']}章")
    print(f"最大迭代次数：{requirement['max_iterations']}次")
    print("-" * 30)


def save_story_to_file(story_content: str, theme: str):
    """保存故事到文件"""
    import datetime
    
    # 创建输出目录
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{theme}_{timestamp}.md"
    
    # 保存文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(story_content)
    
    print(f"📄 故事已保存到：{filename}")
    return filename


def main():
    """主函数"""
    print("🎭 欢迎使用故事生成系统！")
    print("基于大模型的多Agent协作故事生成系统")
    print("=" * 60)
    
    # 检查环境变量
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 错误：未设置OPENAI_API_KEY环境变量")
        print("请在.env文件中设置您的OpenAI API密钥")
        return
    
    try:
        # 获取故事要求
        requirement = get_story_requirement()
        
        # 显示确认
        display_story_requirement(requirement)
        
        confirm = input("\n确认开始生成故事？(y/n): ").lower()
        if confirm != 'y':
            print("❌ 已取消故事生成")
            return
        
        # 创建工作流
        workflow = StoryWorkflow()
        
        # 运行工作流
        result = workflow.run(requirement, requirement["max_iterations"])
        
        # 显示结果
        print("\n" + "=" * 60)
        print("🎉 故事生成完成！")
        print(f"📊 最终评分：{result['final_score']}/10")
        print(f"🔄 迭代次数：{result['iterations']}")
        print(f"📚 章节数：{len(result['chapters'])}")
        
        # 保存故事到文件
        filename = save_story_to_file(result['final_story'], requirement['theme'])
        
        # 显示故事预览
        print("\n📖 故事预览：")
        print("-" * 40)
        print(result['final_story'][:500] + "...")
        print("-" * 40)
        print(f"完整故事请查看：{filename}")
        
    except KeyboardInterrupt:
        print("\n❌ 用户中断了程序")
    except Exception as e:
        print(f"\n❌ 程序运行出错：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
