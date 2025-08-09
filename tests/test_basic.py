"""
基本测试文件
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from database.models import DatabaseManager
from utils.search_tools import SearchTools


def test_database_creation():
    """测试数据库创建"""
    try:
        db = DatabaseManager(":memory:")  # 使用内存数据库进行测试
        print("✅ 数据库创建测试通过")
        return True
    except Exception as e:
        print(f"❌ 数据库创建测试失败：{e}")
        return False


def test_search_tools():
    """测试搜索工具"""
    try:
        search = SearchTools()
        # 测试搜索功能（不实际调用API）
        print("✅ 搜索工具初始化测试通过")
        return True
    except Exception as e:
        print(f"❌ 搜索工具测试失败：{e}")
        return False


def run_basic_tests():
    """运行基本测试"""
    print("🧪 运行基本测试...")
    
    tests = [
        test_database_creation,
        test_search_tools
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 测试结果：{passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有基本测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查配置")


if __name__ == "__main__":
    run_basic_tests()
