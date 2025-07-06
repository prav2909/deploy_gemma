# Gemma-2B Chatbot on AWS EC2

A compact, production-grade template that serves Google’s **Gemma-2B-IT** model via a FastAPI back-end and a single-page web client.

> For the complete, step-by-step deployment guide, read the Medium article:  
> <https://praveenkumar2909.medium.com/fastapi-based-chatbot-deployment-on-aws-0d8c7a0be965>

---

## User-Interface Preview

<table>
<tr>
  <td align="center"><img src="resources/snapshot1.png" width="340"/></td>
  <td align="center"><img src="resources/snapshot2.png" width="340"/></td>
</tr>
<tr>
  <td align="center"><em>Chat Snapshots</em></td>
  <td align="center"><em>Chat Snapshots</em></td>
</tr>
</table>

---

## Repository Structure
```text
.
├── app.py             # FastAPI + Transformers inference server
├── conda_env.yaml     # Reproducible Conda environment
├── Dockerfile         # GPU-ready container build
├── static/index.html  # Minimal chat front-end
└── resources/         # UI screenshots
```

---

## Quick Start (Local Docker — GPU or CPU)
```bash
git clone https://github.com/prav2909/gemma-chatbot.git
cd gemma-chatbot

docker build -t gemma_chatbot .
docker run --gpus all \
           -e HF_TOKEN=<your_huggingface_token> \
           -p 8080:8080 \
           gemma_chatbot

# Open http://localhost:8080
```

---

## One-Command EC2 Deployment
```bash
# On a GPU-enabled EC2 instance
git clone https://github.com/prav2909/gemma-chatbot.git
cd gemma-chatbot

docker build -t gemma_chatbot .
docker run --gpus all \
           -e HF_TOKEN=<your_huggingface_token> \
           -p 8080:8080 \
           gemma_chatbot

# Application available at http://<EC2_IP>:8080
```
> **Remember:** Terminate the instance when finished to avoid unnecessary charges.

---

## Environment Variables

| Variable   | Description                                           |
|------------|-------------------------------------------------------|
| `HF_TOKEN` | Personal Hugging Face access token (required to pull Gemma model weights) |

---

Licensed under the MIT License © Praveen Kumar
