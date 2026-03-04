import streamlit as st
from app import process_input, answer_question

st.set_page_config(page_title="RAG Chatbot", layout="wide")

# -----------------------------
# Session state
# -----------------------------
st.session_state.setdefault("vectorstore", None)
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("cached_responses", {})
st.session_state.setdefault("preview_text", "")

# -----------------------------
# Sidebar (unchanged)
# -----------------------------
with st.sidebar:
    st.title("📄 RAG Chatbot")
    if st.button("Reset App"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.markdown("---")
    st.markdown("**How to use**")
    st.markdown(
        """
        1. Upload a document or paste text  
        2. Process documents  
        3. Ask questions & follow up  
        """
    )

# -----------------------------
# Main UI
# -----------------------------
st.title("📄Multi Document Chatbot")

input_type = st.selectbox(
    "Select input type",
    ["Link", "PDF", "DOCX", "TXT", "Text"]
)

input_data = None

if input_type == "Link":
    n_links = st.number_input("Number of links", 1, 5, 1)
    input_data = [st.text_input(f"URL {i+1}") for i in range(n_links)]

elif input_type == "Text":
    input_data = st.text_area("Paste your text here", height=180)

else:
    input_data = st.file_uploader(
        f"Upload {input_type}",
        type=[input_type.lower()]
    )

# -----------------------------
# Process Documents
# -----------------------------
if st.button("Process Documents"):
    if input_data:
        with st.spinner("Processing documents..."):
            st.session_state.vectorstore = process_input(input_type, input_data)

            # build preview text
            if input_type == "Text":
                st.session_state.preview_text = input_data[:500]
            elif input_type == "Link":
                st.session_state.preview_text = "\n".join(input_data)[:500]
            else:
                st.session_state.preview_text = "Document uploaded successfully."

        st.success("✅ Documents processed successfully!")
    else:
        st.warning("Please provide valid input.")

# -----------------------------
# Preview Section
# -----------------------------
if st.session_state.preview_text:
    st.markdown(
        f"""
        <div style="
            background-color:#d4d4d4;
            color:#1f1f1f;
            padding:14px;
            border-radius:10px;
            border:1px solid #e0e0e0;
            box-shadow:0 2px 6px rgba(0,0,0,0.05);
            margin-bottom:20px;
            max-height:200px;
            overflow-y:auto;
            font-size:14px;
            line-height:1.5;
        ">
            <b>Document Preview</b><br><br>
            {st.session_state.preview_text}
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------
# Chat Section (input first, history below)
# -----------------------------
if st.session_state.vectorstore:
    st.subheader("💬 Ask questions")

    user_query = st.text_input(
        
        "Type your question here...",
        placeholder="E.g., 'Summarize the main points', 'Explain briefly', 'What are the key things?'",
        
        key="user_query"
    )

    if st.button("Ask") and user_query.strip():
        # append user message first
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        # check cache
        if user_query in st.session_state.cached_responses:
            answer = st.session_state.cached_responses[user_query]
        else:
            answer = answer_question(
                st.session_state.vectorstore,
                user_query,
                st.session_state.chat_history  # <-- pass chat history to backend
            )
            st.session_state.cached_responses[user_query] = answer

        # append bot response
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

        # No need for experimental_rerun()
        # Streamlit will refresh automatically after button click


        

# -----------------------------
# Display chat history below input
# -----------------------------
if st.session_state.chat_history:
    st.markdown("### 🗨️ Conversation")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div style="
                    background-color:#c9dec9;  /* light grey-blue for user */
                    color:#0d47a1;
                    padding:12px 14px;
                    border-radius:10px;
                    margin-bottom:6px;
                    max-width:90%;
                ">
                    <b>You:</b> {msg["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            answer = msg["content"]
            if answer.startswith("⚠️"):
                st.markdown(
                    f"""
                    <div style="
                        background-color:#fff3cd;
                        color:#856404;
                        padding:12px 14px;
                        border-radius:10px;
                        border:1px solid #ffeeba;
                        max-width:90%;
                        margin-bottom:12px;
                    ">
                        {answer}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#daedf4;
                        color:#212121;
                        padding:12px 14px;
                        border-radius:10px;
                        max-width:90%;
                        margin-bottom:12px;
                    ">
                        {answer}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

