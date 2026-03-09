from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator
from sentence_transformers import SentenceTransformer
from datetime import datetime
import faiss
import requests
import os

app = Flask(__name__)

# ---------------- Config ----------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"
DATA_DIR = "college_data"
MEMORY_FILE = "memory.txt"
HISTORY_DEPTH = 1

# ---------------- Chat History Setup ----------------
chat_history = []
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs("chats", exist_ok=True)
chat_file_path = f"chats/chat_{timestamp}.txt"


def format_history():
    return "\n".join([
        f"User: {turn['user']}\nBot: {turn['bot']}"
        for turn in chat_history[-HISTORY_DEPTH:]
    ])


def log_chat_to_file(user, bot):
    with open(chat_file_path, "a", encoding="utf-8") as f:
        f.write(f"User: {user}\nBot: {bot}\n\n")


# ---------------- Load Documents ----------------
def load_documents():
    docs = []
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                    for chunk in f.read().split("\n\n"):
                        if chunk.strip():
                            docs.append(chunk.strip())

    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            docs += [line.strip() for line in f if line.strip()]

    return docs


# ---------------- Load Embedding Model & FAISS ----------------
print("[INFO] Loading embedding model...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

print("[INFO] Loading documents...")
documents = load_documents()

if not documents:
    raise ValueError("No documents found in college_data or memory.txt")

print("[INFO] Creating embeddings...")
embeddings = embed_model.encode(documents, normalize_embeddings=True)

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

print(f"[INFO] {len(documents)} context documents loaded.")


# ---------------- Helper Functions ----------------
def translate_to_english(text):
    # Translate from Hindi to English
    return GoogleTranslator(source='hi', target='en').translate(text)


def translate_to_hindi(text):
    # Translate from English to Hindi
    return GoogleTranslator(source='en', target='hi').translate(text)


def retrieve_context(query, k=3):
    query_vec = embed_model.encode([query], normalize_embeddings=True)
    _, I = index.search(query_vec, k)
    return "\n---\n".join([documents[i] for i in I[0]])


def build_prompt(query, context):
    return f"""You are a helpful college assistant at Graphic Era Hill University, Bhimtal Campus.

Communication style:
- Friendly
- Talkative
- Slightly humorous
- Short, natural replies (1–2 sentences)
- Never invent facts

Conversation History:
{format_history()}

Context:
{context}

User: {query}
Answer:"""


def query_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()["response"].strip()


# ---------------- API Endpoint ----------------
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    user_lang = data.get("lang", "en")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Translate to English if user sends Hindi
    translated_input = (
        translate_to_english(user_message)
        if user_lang == 'hi'
        else user_message
    )

    context = retrieve_context(translated_input)
    prompt = build_prompt(translated_input, context)

    try:
        raw_reply = query_ollama(prompt)
    except Exception as e:
        return jsonify({"error": f"Ollama request failed: {str(e)}"}), 500

    # Translate response back to Hindi if needed
    final_reply = (
        translate_to_hindi(raw_reply)
        if user_lang == 'hi'
        else raw_reply
    )

    chat_history.append({"user": user_message, "bot": final_reply})
    log_chat_to_file(user_message, final_reply)

    return jsonify({"response": final_reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
