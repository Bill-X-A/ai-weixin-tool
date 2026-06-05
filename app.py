import streamlit as st
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="0e11fc3a1a2d4288827f7f8bafee75c4.vO0zGOmcZ3P8iEzU")

st.title("🤖 朋友圈文案生成器")
st.write("输入一件事，选择风格，谢鹏辉大王帮你生成文案")

user_input = st.text_input("发生了什么？", placeholder="比如：今天去了西湖")

style = st.selectbox("选择风格", ["活泼", "文艺", "简约", "搞笑", "感悟"])

count = st.slider("生成几条", 1, 5, 3)

if st.button("生成文案"):
    if user_input:
        with st.spinner("AI生成中..."):
            response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "user", "content": f"""请根据以下内容生成{count}条{style}风格的朋友圈文案。
要求：
- 像真人写的，不要用烂大街词汇
- 口语化，自然，有细节感
- 每条之间用空行隔开
- 不要加编号

事件：{user_input}"""}
                ]
            )
            result = response.choices[0].message.content
            st.write(result)
    else:
        st.warning("请先输入内容")
