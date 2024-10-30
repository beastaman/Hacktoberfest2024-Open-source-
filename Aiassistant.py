import openai
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = 'your_openai_api_key'

def generate_response(prompt, max_tokens=100, temperature=0.7):
    """
    Generates a response from OpenAI's GPT model based on a given prompt.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/ask', methods=['POST'])
def ask_question():
    """
    Endpoint for handling general questions.
    """
    data = request.get_json()
    question = data.get("question", "")
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    prompt = f"Answer the following question: {question}"
    answer = generate_response(prompt)
    
    return jsonify({"response": answer})

@app.route('/summarize', methods=['POST'])
def summarize_text():
    """
    Endpoint for summarizing text.
    """
    data = request.get_json()
    text = data.get("text", "")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    prompt = f"Summarize the following text in simple terms: {text}"
    summary = generate_response(prompt, max_tokens=60)
    
    return jsonify({"summary": summary})

@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint for engaging in a conversation.
    """
    data = request.get_json()
    message = data.get("message", "")
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    prompt = f"Respond to this message conversationally: {message}"
    response = generate_response(prompt)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
