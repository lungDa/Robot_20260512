import streamlit as st
import google.generativeai as genai

# 1. 從後台 Secrets 讀取金鑰
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.1-flash')

except Exception as e:
    st.error(f"金鑰設定錯誤: {e}")
    st.stop()

st.title("Gemini API 連線測試")

st.info("若能成功收到 AI 回覆，表示你的 GitHub 與 Secrets 環境配置正確！")

# 2. 簡單輸入介面
user_input = st.text_input("輸入一段話測試連線（例如：你好）:")

if user_input:
    with st.spinner("AI 正在回應中..."):
        try:
            # 呼叫 API
            response = model.generate_content(user_input)

            # 3. 顯示結果
            st.subheader("AI 的回應:")
            st.write(response.text)

            st.success("連線成功！")

        except Exception as e:
            st.error(f"連線失敗: {e}")
