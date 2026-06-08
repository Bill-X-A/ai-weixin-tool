import streamlit as st
from zhipuai import ZhipuAI

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
    st.session_state.last_style = "活泼"
style = st.selectbox("选择风格", styles, index = styles.index(st.session_state.last_style))

count = st.slider("生成几条", 1, 5, 3)

if st.button("生成文案"):
    if user_input:
        with st.spinner("AI生成中..."):
            check = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "user", "content": f"判断这句话是否与朋友圈文案相关，只回答'是'或'否'：{user_input}"}
                ]
            )
            is_relevant = check.choices[0].message.content.strip()

            if "否" in is_relevant:
                st.warning("傻狗，赶紧撤回，这个问题超出了我的服务范围，我只能帮你生成朋友圈文案")
            else:
                response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "system", "content": "你是一个专门写中文朋友圈文案的助手。如果用户的输入与朋友圈文案无关，你必须回复：「这个问题超出了我的服务范围，我只能帮你生成朋友圈文案哦～」然后停止回答，不做任何其他操作。"},
                    {"role": "user", "content": f"""我平时的朋友圈风格是这样的：
{style_sample}

请模仿我的语气，根据以下事件生成{count}条{style}风格的朋友圈文案：
{user_input}

要求：
- 模仿我的语气，不要有AI味
- 口语化，自然，有细节感
- 每条之间用空行隔开
- 不要加编号"""}
                ]
            )
                result = response.choices[0].message.content
                st.write(result)
                st.text_area("复制文案", result, height=200)
                st.session_state.last_style = style
    else:
        st.warning("请先输入内容")
