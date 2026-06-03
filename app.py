import streamlit as st
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="0e11fc3a1a2d4288827f7f8bafee75c4.vO0zGOmcZ3P8iEzU")

st.title("🤖 朋友圈文案生成器")
st.write("输入一件事，谢鹏辉大王帮你生成朋友圈文案")

user_input = st.text_input("发生了什么？", placeholder="比如：今天去了西湖")

if st.button("生成文案"):
    if user_input:
        with st.spinner("AI生成中..."):
            response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "user", "content": f"请根据以下内容生成3种风格的朋友圈文案（活泼、文艺、简约），每种风格一条：{user_input}"}
                ]
            )
            result = response.choices[0].message.content
            st.write(result)
    else:
        st.warning("请先输入内容")
