import requests
import streamlit as st

API_BASE = "http://backend:8000"

st.set_page_config(page_title="Vietnamese Legal Chatbot")
st.title("Vietnamese Legal Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def send_request(text: str) -> dict:
    payload = {
        "user_message": text,
        "user_id": "1",
        "bot_id": "botLawyer",
        "sync_request": False,
    }
    resp = requests.post(f"{API_BASE}/chat/complete", json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def poll(task_id: str) -> str:
    resp = requests.get(f"{API_BASE}/chat/complete/{task_id}", timeout=120)
    resp.raise_for_status()
    data = resp.json()
    task_result = data.get("task_result")
    if isinstance(task_result, dict):
        content = task_result.get("content")
        if content:
            return content
    if isinstance(task_result, str) and task_result.strip():
        return task_result

    error_message = data.get("error_message")
    if error_message:
        return f"Lỗi từ backend: {error_message}"

    return f"Không có phản hồi. Trạng thái hiện tại: {data.get('task_status', 'UNKNOWN')}"


if prompt := st.chat_input("Hỏi về pháp luật Việt Nam..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        task = send_request(prompt)
        answer = poll(task["task_id"])
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
