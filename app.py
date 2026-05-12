import streamlit as st
import google.generativeai as genai
# 頁面初始化設定
st.set_page_config(
page_title="中科 AI 客服 -龍大的小天地",
page_icon=" ",
layout="wide" # "wide" 可利用全螢幕寬度,適合放置儀表板
)

with st.sidebar:
  st.image("https://via.placeholder.com/150", caption="中科推廣部")
  st.title("系統控制台")
  # 建立下拉選單讓使用者切換服務
  service_type = st.selectbox(
  "請選擇服務類別:",
  ["一般諮詢","技術支援","投訴建議"]
  )
  # 增加 AI 創意度調整桿
  temp = st.slider("AI 靈活度(Temperature)", 0.0, 1.0, 0.7)
  
  st.divider() # 畫出一條美觀的分隔線
  st.info(f"當前連線:{service_type}")
