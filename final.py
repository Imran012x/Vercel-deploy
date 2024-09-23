import openai  # Import OpenAI library for interacting with the GPT model
import PyPDF2  # Import PyPDF2 for reading PDF files
import streamlit as st  # Import Streamlit for creating the web app

# Setup OpenAI API Key
openai.api_key = 

# Replace with your actual OpenAI API key

# Function to read PDF and extract text
def read_pdf(file_path):
    pdf_text = ""  # Initialize an empty string to store the PDF text
    with open(file_path, 'rb') as file:  # Open the PDF file in binary read mode
        reader = PyPDF2.PdfReader(file)  # Create a PDF reader object
        for page in reader.pages:  # Loop through each page in the PDF
            pdf_text += page.extract_text()  # Extract and append the text from the page
    return pdf_text  # Return the full extracted text

# Function to query GPT-3.5 Turbo
def query_gpt_turbo(question, context):
    # Call the OpenAI API to get a response from GPT-3.5
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Specify the model to use
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},  # System message to set context
            {"role": "user", "content": f"{question}\n\n{context}"}  # User message with the question and context
        ],
        max_tokens=4096,  # Set the maximum number of tokens for the response
        temperature=0.5  # Control randomness of the response
    )
    return response.choices[0].message['content']  # Return the content of the response

# Streamlit app
st.markdown("<h1 style='text-align: center;'>BOUSST AI PORTAL</h1>", unsafe_allow_html=True)  # Centered title

# Ask for a question
question = st.text_input("Enter your question")  # Create an input field for the user to enter a question

# PDF file path (set the path to your PDF file)
pdf_file_path = 'cse.pdf'  # Update with your PDF file path
pdf_text = read_pdf(pdf_file_path)  # Read the PDF content at the start

# Automatically provide the answer when the user presses Enter
if question:  # Check if a question is provided
    with st.spinner("Searching..."):  # Show a spinner while processing
        start = 0
        answer_found = False
        while start < len(pdf_text):  # Loop until all text is processed
            # Get a chunk of text (up to the token limit for GPT)
            chunk = pdf_text[start:start + 4000]  # Adjust as necessary for safety margin
            answer = query_gpt_turbo(question, chunk)  # Query GPT with the PDF text chunk
            
            # Check if the response indicates the answer is not available
            if "not available" not in answer.lower():
                st.write(answer)  # Display the answer found in the chunk
                answer_found = True
                break  # Exit loop if answer is found

            start += 4000  # Move to the next chunk

        # If no answer was found in any chunks, provide a general answer
        if not answer_found:
            st.write("Sorry, I couldn't find that in the PDF. Here is a general answer to your question.")

# Optional: Provide a message if no question is entered
if not question:
    st.info("Please enter a question to get started.")  # Show an info message if the input is empty
