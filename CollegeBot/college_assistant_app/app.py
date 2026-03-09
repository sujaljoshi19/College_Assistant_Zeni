from flask import Flask, request, jsonify
from googletrans import Translator
from sentence_transformers import SentenceTransformer
from datetime import datetime
import faiss
import requests
import os
import asyncio
from intent_rules import match_intent

app = Flask(__name__)
translator = Translator()

# ---------------- Config ----------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"
DATA_DIR = "college_data"
MEMORY_FILE = "memory.txt"
EMBED_MODEL_PATH = "./embedding_models/all-MiniLM-L6-v2"
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

print("[INFO] Loading embedding model and data...")
embed_model = SentenceTransformer(EMBED_MODEL_PATH)
documents = load_documents()
embeddings = embed_model.encode(documents, normalize_embeddings=True)
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)
print(f"[INFO] {len(documents)} context documents loaded.")

# ---------------- Helper Functions ----------------
def _run_coroutine_safe(coro):
    """Safely run a coroutine, handling event loop issues"""
    try:
        # Try to get existing event loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is running, we can't use asyncio.run()
            # Create a new event loop in a new thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(lambda: asyncio.run(coro))
                return future.result()
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        # No event loop exists, create new one
        try:
            return asyncio.run(coro)
        except RuntimeError:
            # Event loop was closed, create new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(coro)
            finally:
                loop.close()

def translate_to_english(text):
    try:
        # Handle async translation
        result = translator.translate(text, src='hi', dest='en')
        # Check if it's a coroutine (async) and run it
        if asyncio.iscoroutine(result):
            result = _run_coroutine_safe(result)
        return result.text
    except Exception as e:
        print(f"[ERROR] Translation to English failed: {e}")
        # Fallback: return original text if translation fails
        return text

def translate_to_hindi(text):
    """Translate English text to Hindi"""
    if not text:
        return text
    
    try:
        # Handle async translation
        result = translator.translate(text, src='en', dest='hi')
        # Check if it's a coroutine (async) and run it
        if asyncio.iscoroutine(result):
            result = _run_coroutine_safe(result)
        
        translated_text = result.text
        print(f"[DEBUG] Translation successful: {text[:30]}... -> {translated_text[:30]}...")
        
        # Verify translation happened (should be different from original)
        if translated_text and translated_text != text:
            return translated_text
        else:
            print(f"[WARNING] Translation returned same text, may have failed")
            # Try one more time
            try:
                result = translator.translate(text, src='en', dest='hi')
                if asyncio.iscoroutine(result):
                    result = _run_coroutine_safe(result)
                if result.text and result.text != text:
                    return result.text
            except:
                pass
            return text
    except Exception as e:
        print(f"[ERROR] Translation to Hindi failed: {e}")
        print(f"[ERROR] Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        # Fallback: return original text if translation fails
        return text

def retrieve_context(query, k=3):
    query_vec = embed_model.encode([query], normalize_embeddings=True)
    _, I = index.search(query_vec, k)
    return "\n---\n".join([documents[i] for i in I[0]])

def build_prompt(query, context):
    return f"""You are a helpful college assistant at Graphic Era Hill University, Bhimtal Campus.

📌 Communication Guidelines:
"tone": "friendly"
"tone": "talkative"
"tone": "humorous"
- Keep replies short and natural — 1–2 sentences unless asked otherwise.
- Speak conversationally like a real person.
- Don't invent facts.

Conversation History:
{format_history()}

Context:
{context}

User: {query}
Answer:"""

def query_ollama(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })
    response.raise_for_status()
    return response.json()["response"].strip()

# ---------------- API Endpoint ----------------
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    user_lang = data.get("lang", "en")  # default to English if not provided
    
    print(f"[DEBUG] Received request - Message: {user_message[:50] if user_message else 'None'}..., Lang: {user_lang}")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Translate input to English if user is using Hindi mode
    if user_lang == 'hi':
        translated_input = translate_to_english(user_message)
    else:
        translated_input = user_message

    # Check for intent match (rule-based responses)
    intent_response = match_intent(translated_input)
    
    if intent_response:
        # Intent matched - return fixed response (translate back if needed)
        print(f"[DEBUG] Intent matched! User lang: {user_lang}, Intent response: {intent_response[:50]}...")
        if user_lang == 'hi':
            print(f"[DEBUG] Translating intent response to Hindi...")
            final_reply = translate_to_hindi(intent_response)
            # Verify translation actually happened (check if it's different from original)
            if final_reply == intent_response:
                print(f"[WARNING] Translation may have failed - response unchanged!")
            else:
                print(f"[DEBUG] Translation successful: {final_reply[:50]}...")
        else:
            final_reply = intent_response
            print(f"[DEBUG] User lang is English, no translation needed")
        
        # Save to history and log (but don't store in memory)
        chat_history.append({"user": user_message, "bot": final_reply})
        log_chat_to_file(user_message, final_reply)
        
        return jsonify({"response": final_reply})

    # No intent match - fallback to existing FAISS + LLM pipeline
    # Retrieve relevant college data
    context = retrieve_context(translated_input)
    prompt = build_prompt(translated_input, context)

    try:
        raw_reply = query_ollama(prompt)
    except Exception as e:
        return jsonify({"error": f"Ollama request failed: {str(e)}"}), 500

    # Translate reply back to Hindi if needed
    final_reply = translate_to_hindi(raw_reply) if user_lang == 'hi' else raw_reply

    # Save to history and log
    chat_history.append({"user": user_message, "bot": final_reply})
    log_chat_to_file(user_message, final_reply)

    return jsonify({"response": final_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)