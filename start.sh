#!/bin/bash

echo "🎭 故事生成系统启动脚本"
echo "================================"

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
if [[ $(echo "$python_version >= 3.9" | bc -l) -eq 1 ]]; then
    echo "✅ Python版本检查通过: $(python3 --version)"
else
    echo "❌ 需要Python 3.9或更高版本"
    exit 1
fi

# 检查uv是否安装
if ! command -v uv &> /dev/null; then
    echo "❌ 未找到uv包管理器，请先安装uv"
    echo "安装命令: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ uv包管理器已安装"

# 安装依赖
echo "📦 正在安装依赖..."
uv sync

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "📝 创建环境变量文件..."
    cp env.example .env
    echo "⚠️  请编辑.env文件，设置您的OpenAI API密钥"
    echo "   文件位置: .env"
    echo "   需要设置: OPENAI_API_KEY=your_api_key_here"
    echo ""
    echo "💡 提示：您可以从 https://platform.openai.com/api-keys 获取API密钥"
    echo ""
    read -p "设置完成后按回车键继续..."
fi

# 运行测试
echo "🧪 运行基本测试..."
uv run python tests/test_basic.py

echo ""
echo "🚀 系统准备就绪！"
echo ""
echo "使用方法："
echo "1. 交互式主程序: uv run python main.py"
echo "2. 演示脚本: uv run python demo.py"
echo "3. 测试: uv run python tests/test_basic.py"
echo ""
echo "📚 详细文档请查看 README.md 和 USAGE.md"
