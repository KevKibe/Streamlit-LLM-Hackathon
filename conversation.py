from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from gmail_fetch import GmailAPI
from text_preprocessing import TextProcessor
from dotenv import load_dotenv

load_dotenv('.env')

class ConversationChain:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
    
    def preprocess_emails(self):
        text_processor = TextProcessor()
        gmail_api = GmailAPI()
        email_data_list = gmail_api.get_emails(3)
        processed_data = []

        for email_data in email_data_list:
            processed_email_data = text_processor.preprocess_email_data(email_data)
            processed_data.append(str(processed_email_data))

        return processed_data

    def initialize_embeddings_and_vectorstore(self, data):
        model_name = 'text-embedding-ada-002'

        embeddings = OpenAIEmbeddings(
            model=model_name,
            openai_api_key=self.openai_api_key
        )

        chunk_size = 1000
        chunk_overlap = 200
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len)

        all_text_chunks = []

        for item in data:
            text_chunks = text_splitter.split_text(item)
            all_text_chunks.extend(text_chunks)

        vectorstore = FAISS.from_texts(texts=all_text_chunks, embedding=embeddings)
        return vectorstore

    def initialize_conversation_chain(self, vectorstore):
        llm = ChatOpenAI(
            model_name='gpt-3.5-turbo',
            model_kwargs={'api_key': self.openai_api_key}
        )
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        conversation_chain = RetrievalQA.from_chain_type(
            llm=llm,
            memory=memory,
            retriever=vectorstore.as_retriever()
        )
        return conversation_chain

    def run_chat(self, user_input):
        emails = self.preprocess_emails()        
        vectorstore = self.initialize_embeddings_and_vectorstore(emails)
        conversation_chain = self.initialize_conversation_chain(vectorstore)

        return conversation_chain.run(user_input)


# if __name__ == "__main__":
#     openai_api_key = os.getenv("OPENAI_API_KEY")
#     chat_bot = ConversationChain(openai_api_key)
#     chat_bot.run_chat()
    # chat_bot = ConversationChain()
    # user_input = input("User: ")  # Prompt the user for input
    # response = chat_bot.run_chat(user_input)
    # print("Bot:", response) 