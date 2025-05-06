import streamlit as st
import pandas as pd
import openai

# Replace below with your own LiteLLM API key and a correct model name from LiteLLM docs.
LITE_LL_API_KEY = "sk--uDUr70SjrvuIyRKHiCpag"    # put your LiteLLM key here
LITE_LL_BASE_URL = "https://litellm.deriv.ai/v1"
MODEL_NAME = "claude-3-7-sonnet-latest"  # or another supported model

client = openai.OpenAI(
    api_key=LITE_LL_API_KEY,
    base_url=LITE_LL_BASE_URL,
)

st.title("Marketing Ops Analysis Agent")

uploaded_file = st.file_uploader("Upload your data file (CSV)", type="csv")
user_query = st.text_input("Ask a question about your data", key="query_input")

# Initialize session state for storing the dataframe
if 'df' not in st.session_state:
    st.session_state.df = None

# Update dataframe when file is uploaded
if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file)

# Only process when user presses enter and both file and query are present
if user_query and st.session_state.df is not None:
    sample_data = st.session_state.df.head(500).to_csv(index=False)
    prompt = f"Dataset:\n{sample_data}\nUser question: {user_query}"
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    st.write("AI Analysis Result:")
    st.write(response.choices[0].message.content)