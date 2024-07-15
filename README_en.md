# Audio Transcription and Response Bot

This repository contains a Python-based bot that can record audio input, transcribe it into text using OpenAI's Whisper model, generate a response using GPT-3.5, and convert the response back into speech. The bot can be used for creating interactive voice-based applications.

## Features

- Record audio input from the microphone.
- Transcribe audio to text using OpenAI's Whisper model.
- Generate a text response using GPT-3.5.
- Convert the text response to speech.
- Play back the generated speech.

## Requirements

- Python 3.9.19

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yayoi-exe/audio-chat-bot.git
    cd audio-chat-bot
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your OpenAI API key:

    Create a `.env` file or edit an existing `.env` file in the root of the project and add your OpenAI API key:

    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Usage

1. Run the main script:

    ```bash
    python main.py
    ```

2. Follow the on-screen instructions to start and stop recording audio, or to quit the application.

## Project Structure

- `main.py`: The main script to run the bot.
- `.env`: File to store environment variables, specifically the OpenAI API key.
- `requirements.txt`: A list of required Python packages.

## Error Handling

The script includes comprehensive error handling to manage issues such as:

- Missing or invalid API keys
- Audio recording errors
- API call failures
- File read/write errors

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
