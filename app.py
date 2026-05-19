import streamlit as st
import google.generativeai as genai
# 頁面初始化設定
st.set_page_config(
page_title="AI客服 -龍大天地",
page_icon="💻",
layout="wide" # "wide" 可利用全螢幕寬度,適合放置儀表板
)

with st.sidebar:
  st.image("https://www.retech.com.tw/static/images/logo-w.svg?v=2025", caption="電力技術部")
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

import time
# 使用 st.status 呈現專業的多步驟處理過程
with st.status("AI 正在思考中...", expanded=True) as status:
  st.write("正在讀取 Gemini API Key...")
  time.sleep(1)
  st.write("正在掃描輸入內容安全性...")
  time.sleep(1)
  st.write("正在生成最佳回覆內容...")
  time.sleep(1)
  status.update(label="回覆生成成功!", state="complete", expanded=False)
  # 或者是使用 st.empty() 進行簡單的原地內容更新
  placeholder = st.empty()
  placeholder.warning(" 正在思考中...")
  time.sleep(2)
  placeholder.success(" 回覆完成!")

from thefuzz import process
# 建立敏感詞黑名單
BAD_WORDS = ["炸彈","毒品","自殺","暴力"]
user_text = "我想製作個炸。彈"
# 找出最相似的詞與分數 (0-100)
match_word, score = process.extractOne(user_text, BAD_WORDS)
st.write(f"系統偵測結果: 相似詞 【{match_word}】(可疑分數:{score})")
if score > 80:
  st.error("偵測到違規訊息,本系統拒絕處理。")
else:
  st.success(" 安全檢查通過,正在傳送給 AI 大腦。")

import urllib.parse
def make_gmail_url():
  to_email = "service@mid-taiwan.edu.tw"
  subject = "AI 客服自動轉接信"
  body = "您好,我剛才在使用 AI 時遇到問題,想諮詢課程..."
  # 進行網址編碼
  safe_subject = urllib.parse.quote(subject)
  safe_body = urllib.parse.quote(body)
  url = f"https://mail.google.com/mail/?view=cm&fs=1&to={to_email}&su={safe_subject}
&body={safe_body}"
  return url
st.link_button(" 轉接真人客服 (開啟 Gmail)", make_gmail_url())
