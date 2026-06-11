import os
import json
import streamlit as st
from zhipuai import ZhipuAI

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "你是一个专门写中文朋友圈文案的助手。你的文案风格真实自然，不要有AI味。"}
    ]

def load_prefs():
    if os.path.exists("prefs.json"):
        with open("prefs.json", "r") as f:
            return json.load(f)
    else:
        return {"last_style": "活泼"}
def save_prefs(style):
    with open("prefs.json", "w") as f:
        json.dump({"last_style": style}, f)

client = ZhipuAI(api_key=st.secrets["ZHIPU_API_KEY"])

st.title("🤖 朋友圈文案生成器")
st.write("输入一件事，选择风格，谢鹏辉大王帮你生成文案")

style_sample = st.text_area(
    "粘贴你平时的朋友圈（2-3条，AI会模仿你的风格）",
    placeholder="比如：今天摸鱼摸到怀疑人生，但工资还没到账所以继续摸",
    height=100
)

user_input = st.text_input("发生了什么？", placeholder="比如：今天去了西湖")
styles =["活泼", "文艺", "简约", "搞笑", "感悟"]
if "last_style" not in st.session_state:
    prefs = load_prefs()
    st.session_state.last_style = prefs["last_style"]
style = st.selectbox("选择风格", styles, index = styles.index(st.session_state.last_style))

count = st.slider("生成几条", 1, 5, 3)

if st.button("生成文案"):
    if user_input:
        with st.spinner("AI生成中..."):
            check = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "user", "content": f"用户正在使用朋友圈文案生成器。判断这句话是否与朋友圈文案相关，只回答'是'或'否'：{user_input}"}
                ]
            )
            is_relevant = check.choices[0].message.content.strip()

            if "否" in is_relevant:
                st.warning("傻狗，赶紧撤回，这个问题超出了我的服务范围，我只能帮你生成朋友圈文案")
            else:
                                # 把用户输入加入历史
                st.session_state.chat_history.append({
                    "role": "user", 
                    "content": f"""我平时的朋友圈风格是这样的：
                {style_sample}

                请模仿我的语气，根据以下事件生成{count}条{style}风格的朋友圈文案：
                {user_input}

                要求：
                - 模仿我的语气，不要有AI味
                - 口语化，自然，有细节感
                - 每条之间用空行隔开
                - 不要加编号"""
                })

                response = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=st.session_state.chat_history
                )

                # 把AI回复也加入历史
                result = response.choices[0].message.content
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result
                })
    st.divider()
    adjust_input = st.text_input("对文案有什么调整意见？", placeholder="比如：再活泼一点、写短一点")

    if st.button("调整文案"):
        if adjust_input:
            st.session_state.chat_history.append({
                "role": "user",
                "content": adjust_input
            })
            with st.spinner("调整中..."):
                response = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=st.session_state.chat_history
                )
                result = response.choices[0].message.content
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result
                })
                st.write(result)
                st.text_area("复制文案", result, height=200)

                st.text_area("复制文案", result, height=200)
                st.session_state.last_style = style
                save_prefs(st.session_state.last_style)
    else:
        st.warning("请先输入内容")
