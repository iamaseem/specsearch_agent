import streamlit as st

from utils import generate_response, create_gemini_file, get_all_files_uploaded

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

gemini_uploaded_files = []

st.title("Spec Doc Analyzer")
already_uploaded_files = list(get_all_files_uploaded())
if already_uploaded_files:
    st.sidebar.write("Already uploaded files:")
    for file in already_uploaded_files:
        if file.display_name:
            st.sidebar.write(f"- {file.display_name}")

# File uploader
uploaded_files = st.file_uploader("Choose files (optional, content not yet sent to Gemini)", accept_multiple_files=True)

if uploaded_files:
    st.sidebar.write("Uploaded files:")
    for uploaded_file in uploaded_files:
        st.sidebar.write(f"- {uploaded_file.name} ({uploaded_file.type})")
        gemini_uploaded_files.append(create_gemini_file(uploaded_file))
        # You can add further processing for each file here
        # For example, to display the content of a text file:
        # if uploaded_file.type == "text/plain":
        #     with st.expander(f"Content of {uploaded_file.name}"):
        #         st.text(uploaded_file.getvalue().decode())

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask Gemini..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            assistant_response_content = generate_response(prompt, gemini_uploaded_files)

            # Append information about uploaded files if they exist
            # This part is just an acknowledgment and doesn't send file content to Gemini yet.
            if uploaded_files:
                file_names = ", ".join([f.name for f in uploaded_files])
                assistant_response_content += f"\n\n*(Files uploaded: {file_names}. Their content is not yet processed by Gemini in this version.)*"
            
            st.markdown(assistant_response_content)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response_content})

        except Exception as e:
            error_message = f"Sorry, I encountered an error while trying to reach Gemini: {e}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})