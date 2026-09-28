import streamlit as st
from openai import OpenAI

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Islamic RAG Demo", page_icon="🕌")

# --- CUSTOM CSS FOR ARABIC (RIGHT-TO-LEFT) SUPPORT ---
# This makes the chat bubbles align correctly for Arabic text
st.markdown("""
<style>
    /* Flip text alignment for RTL languages in chat messages */
    [data-testid="stChatMessageContent"] {
        direction: rtl;
        text-align: right;
    }
    /* Keep the input box LTR so typing works normally */
    [data-testid="stChatInput"] {
        direction: ltr; 
    }
</style>
""", unsafe_allow_html=True)

# Show title and description (Bilingual)
st.title("🕌 Islamic RAG AI Demo")
st.write(
    "This is a simple chatbot using free AI models. You can chat in **English** or **Arabic**.\n\n"
    "هذا روبوت محادثة بسيط يستخدم نماذج ذكاء اصطناعي مجانية. يمكنك الدردشة باللغة **الإنجليزية** أو **العربية**."
)

# Ask user for their OpenRouter API key
openrouter_api_key = st.text_input("OpenRouter API Key / مفتاح API", type="password")

if not openrouter_api_key:
    st.info("Please add your OpenRouter API key to continue. / يرجى إضافة مفتاح API للمتابعة.", icon="🗝️")
else:
    # Create an OpenAI client pointing to OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
        default_headers={
            "HTTP-Referer": "https://streamlit.io",
            "X-Title": "Streamlit Free Demo",
        }
    )

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        # We add a "system" message first to tell the AI how to behave.
        st.session_state.messages = [
            {
                "role": "system", 
                "content": "You are a helpful Islamic AI assistant. You must reply in the same language the user speaks to you. If they speak Arabic, reply in fluent Arabic. If they speak English, reply in English. Keep answers respectful and accurate."
            }
        ]

    # Display the existing chat messages (skipping the system prompt).
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Create a chat input field.
    if prompt := st.chat_input("Ask a question... / اسأل سؤالاً..."):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenRouter Free Models Router.
        try:
            stream = client.chat.completions.create(
                model="openrouter/free",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            # Stream the response to the chat.
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Tip: This often happens if the free model is busy. Try again in a moment.")
