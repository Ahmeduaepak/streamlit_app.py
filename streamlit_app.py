import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Free Chatbot Demo")
st.write(
    "This is a simple chatbot using a **free** open-source model via OpenRouter. "
    "To use this app, you need to provide an OpenRouter API key, which you can get [here](https://openrouter.ai/keys)."
)

# Ask user for their OpenRouter API key
openrouter_api_key = st.text_input("OpenRouter API Key", type="password")

if not openrouter_api_key:
    st.info("Please add your OpenRouter API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client, but point it to OpenRouter's servers.
    # We also add the optional headers recommended by OpenRouter.
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
        default_headers={
            "HTTP-Referer": "https://streamlit.io", # Optional, for OpenRouter rankings
            "X-Title": "Streamlit Free Demo",       # Optional, for OpenRouter rankings
        }
    )

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenRouter API.
        try:
            stream = client.chat.completions.create(
                # We are using a different, highly reliable free model here.
                model="mistralai/mistral-7b-instruct:free", 
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
            # If OpenRouter rejects the request, show a friendly error message.
            st.error(f"An error occurred: {e}")
            st.info("Tip: This often happens if the free model is busy. Check your OpenRouter privacy settings or try a different free model.")
