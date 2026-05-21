import streamlit as st
import json

# JSON読み込み
with open("models.json", "r", encoding="utf-8") as f:
    models = json.load(f)

st.title("製麺機 型式検索")

# 型式入力
query = st.text_input("型式を入力してください")

if query:
    results = []

    for item in models:
        code = item.get("code", "")
        internal = item.get("internal", "")
        series = item.get("series", "")
        specs = item.get("specs", [])

        text = (
            code + " " +
            internal + " " +
            series + " " +
            " ".join(specs)
        )

        if query.lower() in text.lower():
            results.append(item)

    st.write(f"{len(results)} 件見つかりました")

    for r in results:
        st.subheader(r["code"])

        st.write("内部型式:", r["internal"])
        st.write("シリーズ:", r["series"])

        if r["specs"]:
            st.write("仕様:")
            for s in r["specs"]:
                st.write("- " + s)

        st.divider()