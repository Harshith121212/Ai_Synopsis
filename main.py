import streamlit as st
from llm_connector import llm_connection_helper
from pdf_handler import extract_text_from_pdf, save_text_to_json, upload_pdf_to_mongodb

st.markdown(
    """
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Playwrite+VN:wght@100..400&display=swap");

        .title {
            font-family: 'Playwrite VN', serif;
            color: orange;
            font-size: 5em;
            font-weight: bold;
            text-align: center;
        }
    </style>
    <h1 class="title">AiSynopsis! 🤖</h1>
    <h3 style="text-align: center; font-size: 2em; font-weight: bold">AI-Powered PDF Summarizer</h3>
    <p style="text-align: center;">📚 Unlock rapid insights from your PDFs with our cutting-edge summarization tool. Powered by the efficient Llama 3.3 language model and accelerated by the Groq Cloud API, we deliver concise summaries of even the most extensive documents in record time.</p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p style="text-align: center; font-size: 1em; font-weight: bold; color: red;">⚠️ Note: Please upload a PDF file smaller than 2 MB.</p>
    """,
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader("Upload your PDF file (Max: 2 MB)", type="pdf")

no_of_line = st.select_slider(
    "In how many lines do you need summary?",
    options=[5, 10, 15, 20, 25],
)

if uploaded_file is not None:
    # Check file size (2 MB = 2 * 1024 * 1024 bytes)
    if uploaded_file.size <= 2 * 1024 * 1024:
        st.write("Uploaded file details:")
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**File size:** {uploaded_file.size / 1024:.2f} KB")

        # Upload the PDF to MongoDB using GridFS
        file_id = upload_pdf_to_mongodb(uploaded_file)
        if file_id:
            #st.success(f"File uploaded successfully to MongoDB with ID: {file_id}")

            # Extract text from the uploaded PDF directly from the file object
            try:
                extracted_text = extract_text_from_pdf(uploaded_file)
                st.success("Text successfully extracted from the PDF.")

                # Save the extracted text to a JSON file
                json_file = save_text_to_json(extracted_text)

                # Optionally, upload the JSON file to MongoDB
                # file_id = upload_pdf_to_mongodb(json_file)
                # st.success(f"JSON file uploaded to MongoDB with ID: {file_id}")

                if st.button("Generate Summary"):
                    summary_response = llm_connection_helper(no_of_line)

                    # Extract summary content from response
                    if summary_response:
                        # Create a bulleted list of the points in the summary
                        bullet_points = summary_response.split("\n")  # Assuming each point is separated by a new line

                        # Format the points into a bullet list
                        formatted_summary = "\n".join(
                            [f" {point.strip()}" for point in bullet_points if point.strip()]  # Add '•' for bullets
                        )

                        # Display the summary in a clean, intuitive format
                        st.markdown(
                            """
                            <p style="text-align: center; font-weight: bold; font-size: 1.5em; color: #FFA500;">Summary 😎:</p>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.text_area("Summary", formatted_summary, height=300)
            except Exception as e:
                st.error(f"An error occurred while processing the PDF: {e}")
        else:
            st.error("Failed to upload the file to MongoDB.")
    else:
        st.error("File size exceeds the 2 MB limit. Please upload a smaller file.")

else:
    st.info("Please upload a PDF file to get started.")
