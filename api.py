import os
from flask import Flask, request, jsonify
from conversation import ConversationChain  

app = Flask(__name__)
conversation_chain = ConversationChain()

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
