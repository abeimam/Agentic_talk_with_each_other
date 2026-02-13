# Multi-Agent LLM Conversation Framework

This project provides a simple yet powerful framework for enabling real-time, autonomous conversations between multiple AI agents. It uses a central WebSocket server to route messages, while individual agents use OpenAI models to generate intelligent, context-aware responses.

## 🚀 Core Features

* **Real-time Messaging:** Built on WebSockets for low-latency, bidirectional communication.
* **Autonomous Agents:** Each agent runs in its own process, capable of thinking (via LLM) and responding independently.
* **Centralized Routing:** A simple server manages connections and routes messages between named agents.
* **Asynchronous:** Leverages Python's `asyncio` to efficiently handle multiple agents and API calls concurrently.
* **Extensible:** The simple architecture makes it easy to modify agent behavior (e.g., change prompts, models) or add more agents.

---

## 🛠️ How It Works

The system is composed of two main components: a central server and one or more agent clients.

### 1. The Server (`server.py`)

This script is the **message router**.
* It starts a WebSocket server on `ws://localhost:8765`.
* It maintains a `connection_dictionary` that maps agent names to their active WebSocket connections.
* When an agent connects, it must send a `register` message with its name.
* The server then listens for messages from that agent. Any message must be a JSON object containing a `target` (the name of the recipient agent) and `text` (the message content).
* The server looks up the `target` in its dictionary and forwards the message to the correct recipient.
* It also handles disconnections, gracefully removing agents from the dictionary.

### 2. The Agent (`agent.py`)

This script is the **autonomous client**. You can run multiple instances of this script, one for each agent.
* It takes command-line arguments for its **own name**, its **target's name**, and the **name of the agent who should speak first**.
* It connects to the server and sends the required `register` message.
* It runs three tasks concurrently using `asyncio.gather`:
    1.  **`receive_messages`**: Listens for messages from the server. When a message is received, it triggers the `send_messages` task to generate and send a reply.
    2.  **`send_messages`**: Responsible for generating a response. It checks if it's the agent's turn to speak (either by being the `first_to_speak` or by receiving a message). It then:
        * Calls `making_prompt()` (from `prompt.py`) to formulate a prompt for the LLM.
        * Sends the prompt to the OpenAI API (`gpt-4.1-nano`).
        * Sends the LLM's text response back to the server, addressed to its target.
    3.  **`keep_connection_alive`**: Sends a `ping` to the server every 10 seconds to prevent the connection from timing out.

---

## ⚙️ Setup and Installation

### Prerequisites

* Python 3.7+
* An OpenAI API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the required libraries:**
    * You'll need `websockets`, `openai`, and `python-dotenv`. Create a `requirements.txt` file with:
        ```
        websockets
        openai
        python-dotenv
        ```
    * Then install them:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Configure Environment Variables:**
    * Create a file named `.env` in the root of the project directory.
    * Add your OpenAI API key to this file:
        ```
        OPENAI_API_KEY=sk-YourSecretAPIKeyGoesHere
        ```

5.  **Create the `prompt.py` file:**
    * This project relies on a `prompt.py` file with a function `making_prompt(previous_message)`. You must create this file. Here is a simple example to get started:

    ```python
    # prompt.py
    def making_prompt(previous_message=""):
        """
        Creates a prompt for the LLM.
        """
        if not previous_message:
            # This is the first message in the conversation
            return "You are a helpful assistant. Start a new conversation with a friendly greeting."
        else:
            # This is a reply
            return f"The user said: '{previous_message}'. Respond to this in a helpful and concise way."
    ```

---

## ▶️ How to Run

You will need **three separate terminal windows** open.

### 1. Terminal 1: Start the Server

First, start the message routing server.
```bash
python server.py
