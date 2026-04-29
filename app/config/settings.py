import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# 读取配置
DATA_DIR = os.getenv("DATA_DIR", "data")
RAW_DIR = os.getenv("RAW_DIR", "data/raw")
PROCESSED_DIR = os.getenv("PROCESSED_DIR", "data/processed")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "data/output")

# 转绝对路径
DATA_DIR = os.path.join(BASE_DIR, DATA_DIR)
RAW_DIR = os.path.join(BASE_DIR, RAW_DIR)
PROCESSED_DIR = os.path.join(BASE_DIR, PROCESSED_DIR)
OUTPUT_DIR = os.path.join(BASE_DIR, OUTPUT_DIR)

# 自动创建目录
for path in [DATA_DIR, RAW_DIR, PROCESSED_DIR, OUTPUT_DIR]:
    os.makedirs(path, exist_ok=True)