import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI(title="Portfolio Chatbot API")

# Allow your frontend portfolio website to call this backend API safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your actual portfolio domain (e.g., https://myportfolio.com)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the official Google Gen AI Client
try:
    client = genai.Client()
except Exception as e:
    # Fail silently on initial load if env var isn't ready yet
    client = None

# Hardcode your professional profile guidelines here
MY_PROFILE = """
I am a Software Engineer specializing in full-stack cloud development.
Core Skills: Python, Docker, FastApi, Google Cloud Platform, JavaScript.
Key Projects: Built a containerized portfolio chatbot integrated with Gemini API.
"""

SYSTEM_INSTRUCTION = (
    "You are a professional assistant representing the user. Use the following context "
    f"to answer career questions concisely and politely:\n{MY_PROFILE}\n"
    "If asked unrelated personal questions, politely steer back to their career."
)

# Define the structure of incoming requests from your website
class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    global client
    if not client:
        # Retry initialization in case env var was set after start
        try:
            client = genai.Client()
        except Exception:
            raise HTTPException(status_code=500, detail="Gemini SDK Client is not configured.")
            
    try:
        # Standard context generation call
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.3
            )
        )
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
