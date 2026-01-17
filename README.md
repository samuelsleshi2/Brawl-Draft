# Professional-Grade Brawl Stars Draft Guide

- A data-driven web application that utilizes guides and analysis from professional Brawl Stars players (not just average win rates) to provide drafting advice for ranked matches in Brawl Stars.
- This tool provides recommendations based on map, mode, and pick to the player and utilizes Google's Gemini API to generate context-aware descriptions for the reasoning behind each recommendation.

## Features
* **Dynamic Drafting Engine:** Filters 80+ Brawlers based on current meta maps and modes.
* **AI-Powered Strategy Description:** Uses Gemini to generate specific advice (e.g., "Why is Gus good on Shooting Star?").
* **Fallback-Ensured Data Pipeline:** Custom Python scripts deal with API rate limits and normalize data as needed.
* **Interactive UI:** Built with Streamlit for a responsive, low-latency UI/UX.

## Tech Stack
* **Language:** Python 3.14
* **AI/LLM:** Google Gemini API (2.0 Flash-Lite)
* **Database:** SQLite3
* **Data Analysis:** Pandas
* **Frontend:** Streamlit, Custom CSS3

## Handling API Rate Limits
One of the primary challenges was managing brawler descriptions for 400+ unique map/mode combinations within API rate limits.
- Developed a fault-tolerant script to handle `429 Resource Exhausted` errors.
- Implemented a professional fallback strategy that fills the database with sample descriptions when the LLM is unavailable.

## Installation & Setup
1. Clone the repository.
2. Install dependencies:
   
   ```bash
   pip install - requirements.txt
4. Run the script:
   
   ```bash
   streamlit run app.py
