# Audio Transcription with OpenAI

Automate the transcription of audio files using OpenAI's API. Especially designed to manage and transcribe large audio files by splitting them into manageable 10-minute chunks.

## Features
- **Audio Splitting:** Automatically splits audio files larger than 25MB into 10-minute chunks.
- **OpenAI Integration:** Uses OpenAI's API to transcribe each audio chunk.
- **Contextual Prompts:** Provides an option to include a prompt for better context during the transcription.

## Requirements
- Python 3.6+
- **pydub:** To split audio files.
- **openai:** To interact with OpenAI's API for transcription.

Install the required packages using:

```
pip install pydub openai
```

## Usage
1. Store your OpenAI API key in a file named **api_key.txt** in the same directory as the script.
2. Set the **directory** variable in the **main()** function to point to the folder containing your **.mp3** files.
3. Run the script:
```
python [script_name].py
```
