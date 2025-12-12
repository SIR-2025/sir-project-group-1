# NAO Theater Performance – “I Don’t Dance”

This project implements an interactive theater performance for the Socially Intelligent Robotics (SIR) course. The NAO robot performs a scripted dialogue and choreography inspired by the “I Don’t Dance” scene from High School Musical. The system uses Dialogflow CX for intent detection, built-in NAO animations for expressive gestures, custom recorded motions for dance sequences, and a GPT-based fallback when no scripted intent matches the user’s input.

---
### Requirements
Install everything via:
pip install -r requirements.txt

### 🔑 Environment Variables

Store the Google Dialogflow (google-key.json) key in:
conf/google

Create a `.env` file in the project root with the following fields:
- OPENAI_API_KEY=your_openai_api_key_here
- OPENAI_MODEL=gpt-4o-mini


## Running the Performance

Before running the performance, ensure the following are active:

### 1. Activate the virtual environment
```bash
source venv_sic/bin/activate

### 2. Start Redis 
redis-server

### 2. Start Dialogflow
run-dialogflow-cx

### 3. Start GPT
run-gpt

### 4. Confirm NAO setup
The NAO robot is powered on
The robot is connected to the same network
The IP address in theater_performance/config.py matches the robot

### 4. Run the full performance (from root folder)
python -m theater_performance.main



