# 🤖 AI-Powered Brawl Stars Draft Guide

A data-driven web application that provides real-time drafting strategies for Brawl Stars. This tool utilizes **Google's Gemini 2.0 Flash-Lite AI** to generate context-aware strategy descriptions for every Brawler based on map, mode, and pick order.

## 🚀 Features
* **Dynamic Drafting Engine:** Filters 80+ Brawlers based on current meta maps and modes.
* **AI-Generated Strategy:** Uses Large Language Models (LLMs) to generate specific advice (e.g., "Why is Gus good on Shooting Star?").
* **Fault-Tolerant Data Pipeline:** Custom Python scripts manage API rate limits and data normalization.
* **Interactive UI:** Built with Streamlit for a responsive, low-latency user experience.

## 🛠️ Tech Stack
* **Language:** Python 3.12
* **AI/ML:** Google Gemini API (2.0 Flash-Lite & 1.5 Flash)
* **Database:** SQLite3
* **Frontend:** Streamlit
* **Data Processing:** Pandas

## 🧩 Technical Challenges & Solutions
### Handling API Rate Limits
One of the core engineering challenges was managing the throughput of the Free Tier Gemini API.
* **Problem:** The API limits requests per minute, causing `429 Resource Exhausted` errors during bulk database population.
* **Solution:** Implemented an **exponential backoff algorithm** in the generator script. If a limit is hit, the system pauses dynamically, retries with a safe delay, and utilizes a "fallback" strategy to ensure database integrity is never compromised.

## 📦 Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/Brawl-Draft-Guide.git](https://github.com/yourusername/Brawl-Draft-Guide.git)