import os
from flask import Flask, request, jsonify
from conversation import ConversationChain  
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__)
api_key = os.getenv("OPENAI_API_KEY")
conversation_chain = ConversationChain(api_key)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('user_input')
    if user_input is None:
        return jsonify({'error': 'Invalid input'}), 400

    response = conversation_chain.run_chat(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
