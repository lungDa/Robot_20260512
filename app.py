#import streamlit as st
#import google.generativeai as genai
# #頁面初始化設定
#st.set_page_config(
#page_title="AI客服 -龍大天地",
#page_icon="💻",
#layout="wide" # "wide" 可利用全螢幕寬度,適合放置儀表板
#)

#with st.sidebar:
#  st.image("https://www.retech.com.tw/static/images/logo-w.svg?v=2025", caption="電力技術部")
#  st.title("系統控制台")
#  # 建立下拉選單讓使用者切換服務
#  service_type = st.selectbox(
#  "請選擇服務類別:",
#  ["一般諮詢","技術支援","投訴建議"]
#  )
#  # 增加 AI 創意度調整桿
#  temp = st.slider("AI 靈活度(Temperature)", 0.0, 1.0, 0.7)
  
#  st.divider() # 畫出一條美觀的分隔線
#  st.info(f"當前連線:{service_type}")




import streamlit as st
import google.generativeai as genai
import urllib.parse
import time

# =========================
# 頁面設定
# =========================
st.set_page_config(
    page_title="AI客服 - 龍大天地",
    page_icon="💻",
    layout="wide"
)

# =========================
# CSS 美化
# =========================
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: 800;
    margin-top: 20px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.chat-box {
    margin-top: 80px;
    padding: 25px;
    border-radius: 18px;
    background-color: #f7f9fc;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
}

.user-msg {
    background-color: #dbeafe;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
}

.ai-msg {
    background-color: #dcfce7;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.image(
        "https://www.retech.com.tw/static/images/logo-w.svg?v=2025",
        caption="電力技術部"
    )

    st.title("系統控制台")

    service_type = st.selectbox(
        "請選擇服務類別:",
        ["一般諮詢", "技術支援", "投訴建議"]
    )

    temp = st.slider("AI 靈活度 Temperature", 0.0, 1.0, 0.7)

    st.divider()
    st.info(f"當前連線：{service_type}")

    if st.button("清除對話紀錄"):
        st.session_state.messages = []
        st.rerun()

# =========================
# Session State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# Gmail URL
# =========================
def make_gmail_url(user_question=""):
    to_email = "willy_huang@retech.com.tw"
    subject = "AI 客服自動轉接信"
    body = f"""您好：

我剛才在使用 AI 客服時遇到問題，想轉接真人客服。

服務類別：{service_type}

我的問題：
{user_question}

謝謝。
"""
    safe_subject = urllib.parse.quote(subject)
    safe_body = urllib.parse.quote(body)

    return (
        "https://mail.google.com/mail/?view=cm&fs=1"
        f"&to={to_email}"
        f"&su={safe_subject}"
        f"&body={safe_body}"
    )

# =========================
# AI 回覆函式
# =========================
def get_ai_reply(user_input):
    try:
        api_key = st.secrets.get("AIzaSyCd7jNF-4YsLLuyk4BimgIJNGg6b4sYrn0")

        if not api_key:
            return "目前尚未設定 Gemini API Key，因此先使用系統預設回覆。請到 Streamlit Secrets 新增 GEMINI_API_KEY。"

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": temp
            }
        )

        prompt = f"""
你是龍大天地的 AI 客服。
目前服務類別：{service_type}

請用繁體中文、專業但親切的方式回答使用者。

使用者問題：
{user_input}
"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"AI 回覆發生錯誤：{e}"

# =========================
# 主畫面
# =========================
st.markdown('<div class="main-title">AI 客服 - 龍大天地</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">請在下方輸入問題，AI 將協助你進行初步判斷</div>', unsafe_allow_html=True)

left, center, right = st.columns([1, 2.2, 1])

with center:
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    st.subheader("客服對話區")

    # 顯示歷史訊息
    if st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="user-msg"><b>你：</b><br>{msg["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="ai-msg"><b>AI客服：</b><br>{msg["content"]}</div>',
                    unsafe_allow_html=True
                )
    else:
        st.info("目前尚無對話紀錄，請在下方輸入問題。")

    st.divider()

    # 中間偏下的對話輸入欄
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "請輸入你的問題：",
            placeholder="例如：設備異常、課程問題、退款問題、技術支援...",
            height=120
        )

        submit = st.form_submit_button("送出問題")

    if submit and user_input.strip():
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.status("AI 正在處理中...", expanded=True) as status:
            st.write("讀取服務類別設定...")
            time.sleep(0.3)

            st.write("分析使用者問題...")
            time.sleep(0.3)

            st.write("生成回覆內容...")
            ai_reply = get_ai_reply(user_input)

            status.update(
                label="回覆生成完成",
                state="complete",
                expanded=False
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_reply
        })

        st.rerun()

    st.link_button(
        "轉接真人客服：開啟 Gmail",
        make_gmail_url()
    )

    st.markdown('</div>', unsafe_allow_html=True)
