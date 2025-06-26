"""
REST API for a minimal web‑based chatbot.

The application serves a small HTML/JavaScript front‑end (in the /static
folder) and exposes two HTTP endpoints:
    • GET  /          – returns the chat page (index.html)
    • POST /generate  – generates a reply from a Hugging Face transformer

A Gemma‑2B‑IT causal‑language model is loaded once at start‑up and moved to
GPU if one is available. The /generate endpoint builds a prompt from the
user input, samples up to 64 new tokens, and returns the assistant’s reply
as JSON.

Author: Praveen Kumar
LinkedIn: https://www.linkedin.com/in/praveen-kumar-b2096391/
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
import pathlib

# Fixed system message that defines the assistant’s personality.
PREFIX = (
    "You are an sarcastic Assistant who responds to prompt_text."
)

# Re‑use model files between runs to save bandwidth and start‑up time
# os.environ["TRANSFORMERS_CACHE"] = os.path.abspath("./transformers_cache")

app = FastAPI()

# Allow any origin while experimenting; restrict in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expose everything inside /static as "/static/*" URLs.
STATIC_DIR = pathlib.Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    """Return the front‑end (index.html) so the browser can load the chat UI."""
    return FileResponse(STATIC_DIR / "index.html")


# ---------- Model loading ----------
model_name = "google/gemma-2b-it"

# The tokenizer converts between text and token IDs.
tokenizer = AutoTokenizer.from_pretrained(model_name)

# The causal‑language model generates the assistant’s reply.
model = AutoModelForCausalLM.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)


class Message(BaseModel):
    """Pydantic model for the JSON body of /generate requests."""

    inputs: str


@app.post("/generate")
async def generate(msg: Message):
    """Generate a chatbot reply from *msg.inputs*.

    Steps
    -----
    1. Build a full prompt by prepending the fixed *PREFIX*.
    2. Tokenise the prompt and move tensors to the same device as the model.
    3. Sample up to 64 new tokens using nucleus sampling (top‑p) with a
       moderate temperature for creativity while avoiding nonsense.
    4. Decode the generated token IDs back to text.
    5. Extract everything that follows the string "Assistant:" and return it.
    """

    # Combine the persona prefix with the user input.
    prompt = f"{PREFIX} prompt_text: {msg.inputs.strip()}\nAssistant:"

    # Tokenise and move tensors to GPU/CPU as appropriate.
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # Autoregressively sample new tokens.
    output = model.generate(
        **inputs,
        max_new_tokens=64,      # Ensures the reply is long enough.
        do_sample=True,
        top_p=0.9,              # Nucleus (top‑p) sampling.
        temperature=0.5,        # Lower temperature → slightly more focused.
        pad_token_id=tokenizer.eos_token_id,
    )

    # Decode the tensor of token IDs into a Python string.
    decoded = tokenizer.decode(output[0], skip_special_tokens=True)

    # Keep only the assistant’s reply (everything after the marker).
    reply = decoded.split("Assistant:", 1)[-1].strip()

    return {"generated_text": reply}
