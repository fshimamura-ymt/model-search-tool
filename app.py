import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="製麺機 絞り込み検索", layout="wide")

# JSON読み込み
with open("models.json", "r", encoding="utf-8") as f:
    models = json.load(f)

# 全シリーズ取得
all_series = sorted(list(set(item["series"] for item in models)))

# 全仕様取得
all_specs = set()
for item in models:
    for s in item["specs"]:
        all_specs.add(s)

all_specs = sorted(list(all_specs))

st.title("製麺機 絞り込み検索")

# -----------------------------
# サイドバー
# -----------------------------
st.sidebar.header("検索条件")

# シリーズ
selected_series = st.sidebar.multiselect(
    "シリーズ",
    all_series
)

# 仕様
selected_specs = st.sidebar.multiselect(
    "仕様",
    all_specs
)

# 型式キーワード
keyword = st.sidebar.text_input("型式キーワード")

# -----------------------------
# 絞り込み
# -----------------------------
results = []

for item in models:

    # シリーズ判定
    if selected_series:
        if item["series"] not in selected_series:
            continue

    # 仕様判定（AND検索）
    if selected_specs:
        if not all(spec in item["specs"] for spec in selected_specs):
            continue

    # キーワード判定
    if keyword:
        text = (
            item["code"] +
            item["internal"] +
            item["series"] +
            "".join(item["specs"])
        ).lower()

        if keyword.lower() not in text:
            continue

    results.append(item)

# -----------------------------
# 表示
# -----------------------------
st.subheader(f"検索結果: {len(results)} 件")

if results:

    table_data = []

    for r in results:
        table_data.append({
            "型式": r["code"],
            "内部型式": r["internal"],
            "シリーズ": r["series"],
            "仕様": ", ".join(r["specs"])
        })

    df = pd.DataFrame(table_data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # CSVダウンロード
    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "CSVダウンロード",
        csv,
        file_name="search_result.csv",
        mime="text/csv"
    )

else:
    st.warning("条件に一致する型式がありません")
