import pandas as pd
import os
from app.config.settings import RAW_DIR


def parse_bid_excel(file_name: str) -> pd.DataFrame:
    file_path = os.path.join(RAW_DIR, file_name)

    df = pd.read_excel(
        file_path,
        sheet_name="分部分项工程项目清单计价表",
        header=None
    )

    print("=== 原始预览 ===")
    print(df.head(20))

    # =========================
    # 1️⃣ 提取工程名称
    # =========================
    project_name = None
    for i in range(len(df)):
        row_str = "".join(map(str, df.iloc[i].tolist()))

        if "" in row_str:
            project_name = df.iloc[i][2]
            print(f"\n工程名称: {project_name}")
            break

    # =========================
    # 2️⃣ 找表头（项目编码所在行）
    # =========================
    header_row = None
    for i in range(len(df)):
        row = df.iloc[i].astype(str)
        if "项目编码" in row.values:
            header_row = i
            break

    if header_row is None:
        raise ValueError("未找到表头")

    print(f"表头行: {header_row}")

    # =========================
    # 3️⃣ 列识别（动态）
    # =========================
    header = df.iloc[header_row]

    col_map = {}
    for idx, col in enumerate(header):
        col_str = str(col)

        if "项目编码" in col_str:
            col_map["item_code"] = idx
        elif "项目名称" in col_str:
            col_map["item_name"] = idx
        elif "工程量" in col_str:
            col_map["quantity"] = idx
        elif "综合单价" in col_str:
            col_map["unit_price"] = idx
        elif "合价" in col_str:
            col_map["total_price"] = idx
        elif "特征" in col_str:
            col_map["feature_desc"] = idx

    print("列映射:", col_map)

    # =========================
    # 4️⃣ 遍历解析
    # =========================
    data = []
    current_category = None
    last_record = None

    for i in range(header_row + 1, len(df)):
        row = df.iloc[i]

        item_code = row.get(col_map.get("item_code"))
        item_name = row.get(col_map.get("item_name"))

        # 转字符串用于判断
        item_name_str = str(item_name)

        # -------------------------
        # 跳过无效行
        # -------------------------
        if pd.isna(item_code) and pd.isna(item_name):
            continue

        if "小计" in item_name_str:
            continue

        if "分部分项工程项目清单计价表" in item_name_str:
            continue

        if "序号" in item_name_str:
            continue

        # -------------------------
        # 🧠 特征描述行（关键逻辑）
        # -------------------------
        if pd.isna(item_code) and pd.isna(item_name):
            feature_idx = col_map.get("feature_desc")

            if feature_idx is not None:
                feature_val = row.get(feature_idx)

                if pd.notna(feature_val) and last_record:
                    last_record["feature_desc"] += str(feature_val)

            continue

        # -------------------------
        # 分部工程行（分类）
        # -------------------------
        if pd.isna(item_code) and pd.notna(item_name):
            current_category = item_name
            continue

        # -------------------------
        # 正常数据行
        # -------------------------
        if pd.notna(item_code):
            record = {
                "project_name": project_name,
                "category": current_category,
                "item_code": item_code,
                "item_name": item_name,
                "quantity": row.get(col_map.get("quantity")),
                "unit_price": row.get(col_map.get("unit_price")),
                "total_price": row.get(col_map.get("total_price")),
                "feature_desc": ""
            }

            data.append(record)
            last_record = record

    result_df = pd.DataFrame(data)

    print("\n=== 解析结果 ===")
    
    print(result_df.head())


    return result_df


if __name__ == "__main__":
    parse_bid_excel("input.xlsx")