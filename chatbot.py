from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os

# Set page configuration
st.set_page_config(page_title="Ask your PDF")

# Load environment variables
load_dotenv()

def main():
    st.header("Ask your PDF 💬")

    # Upload file
    pdf = st.file_uploader("Upload your PDF", type="pdf")

    # Extract the text
    if pdf is not None:
        pdf_reader = PdfReader(pdf)

        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_text(pdf_text)

        # Create metadata for each chunk
        metadatas = [{"source": f"{i+1}"} for i in range(len(texts))]

        # Create embeddings and Chroma vector store
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_texts(texts, embeddings, metadatas=metadatas)

        # Show user input
        user_question = st.text_input("Ask a question about your PDF:")
        if user_question:
            docs = docsearch.similarity_search(user_question)

            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)
                print(cb)

            # Display the response
            st.write(response)

            # Display sources in dropdown menus
            st.write("Sources:")
            sources = {}
            for doc in docs:
                source = doc.metadata['source']
                if source not in sources:
                   

            for source, content in sources.items():
               
                    st.write(content)

if __name__ == '__main__':
    main()
