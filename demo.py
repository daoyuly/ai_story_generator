#!/usr/bin/env python3
"""
故事生成系统演示脚本
"""

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from graph.story_workflow import StoryWorkflow

load_dotenv()


def demo_story_generation():
    """演示故事生成功能"""
    print("🎭 故事生成系统演示")
    print("=" * 50)
    
    # 检查环境变量
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 错误：未设置OPENAI_API_KEY环境变量")
        print("请复制env.example为.env并设置您的OpenAI API密钥")
        return
    
    # 演示用的故事要求
    demo_requirement = {
        "story_type": "科幻",
        "theme": "人工智能与人类共存",
        "target_reader": "青少年",
        "word_count": 2000,
        "chapters": 2,
        "max_iterations": 2  # 演示时使用较少的迭代次数
    }
    
    print("📋 演示故事要求：")
    print(f"故事类型：{demo_requirement['story_type']}")
    print(f"主题：{demo_requirement['theme']}")
    print(f"目标读者：{demo_requirement['target_reader']}")
    print(f"字数要求：{demo_requirement['word_count']}字")
    print(f"章节数：{demo_requirement['chapters']}章")
    print(f"最大迭代次数：{demo_requirement['max_iterations']}次")
    print("-" * 50)
    
    try:
        # 创建工作流
        workflow = StoryWorkflow()
        
        # 运行工作流
        result = workflow.run(demo_requirement, demo_requirement["max_iterations"])
        
        # 显示结果
        print("\n" + "=" * 50)
        print("🎉 故事生成完成！")
        print(f"📊 最终评分：{result['final_score']}/10")
        print(f"🔄 迭代次数：{result['iterations']}")
        print(f"📚 章节数：{len(result['chapters'])}")
        
        # 保存故事到文件
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{output_dir}/demo_story.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(result['final_story'])
        
        print(f"📄 故事已保存到：{filename}")
        
        # 显示故事预览
        print("\n📖 故事预览：")
        print("-" * 40)
        print(result['final_story'][:500] + "...")
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ 演示过程中出错：{e}")
        import traceback
        traceback.print_exc()


def demo_agents():
    """演示各个Agent的功能"""
    print("🤖 Agent功能演示")
    print("=" * 50)
    
    # 这里可以添加各个Agent的单独演示
    print("✅ 所有Agent已准备就绪")
    print("- 故事大纲Agent：负责生成和修改故事大纲")
    print("- 故事编写Agent：负责根据大纲编写具体章节")
    print("- 读者Agent：负责阅读和评价故事")
    print("- 主编Agent：负责根据反馈决定是否继续完善")


def main():
    """主函数"""
    print("🚀 故事生成系统演示")
    print("基于大模型的多Agent协作故事生成系统")
    print("=" * 60)
    
    while True:
        print("\n请选择演示功能：")
        print("1. 完整故事生成演示")
        print("2. Agent功能演示")
        print("3. 退出")
        
        try:
            choice = input("请输入选择 (1-3): ").strip()
            
            if choice == "1":
                demo_story_generation()
            elif choice == "2":
                demo_agents()
            elif choice == "3":
                print("👋 再见！")
                break
            else:
                print("❌ 请输入1-3之间的数字")
                
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 出错：{e}")


if __name__ == "__main__":
    main()
