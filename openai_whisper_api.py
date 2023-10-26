import os
from pydub import AudioSegment
import openai

# Load OpenAI API key from a file
with open('api_key.txt', 'r') as key_file:
    openai.api_key = key_file.readline().strip()

# Define constants
MAX_FILE_SIZE_MB = 25
AUDIO_CHUNK_LENGTH_MS = 10 * 60 * 1000  # 10 minutes in milliseconds

def split_audio_file(file_path):
    """Splits an audio file into chunks of 10 minutes each.
    
    Args:
        file_path (str): Path to the audio file.
        
    Returns:
        list: List of audio chunks.
    """
    audio = AudioSegment.from_mp3(file_path)
    audio_chunks = []
    
    for i in range(0, len(audio), AUDIO_CHUNK_LENGTH_MS):
        chunk = audio[i:i + AUDIO_CHUNK_LENGTH_MS]
        audio_chunks.append(chunk)
    
    return audio_chunks

def transcribe_chunk(chunk, prompt=""):
    """Transcribes an audio chunk using OpenAI's API.
    
    Args:
        chunk (AudioSegment): Audio segment to be transcribed.
        prompt (str, optional): Additional text to help guide the transcription. Defaults to "".
        
    Returns:
        str: Transcription of the audio chunk.
    """
    # Save chunk to a temporary file
    temp_file = "temp_chunk.mp3"
    chunk.export(temp_file, format="mp3")
    
    with open(temp_file, "rb") as audio_file:
        # Pass the prompt parameter to the transcription API
        transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt=prompt).get('text')
    
    # Remove temporary file
    os.remove(temp_file)
    
    return transcript

def main():
    """Main function to transcribe audio files in a directory."""
    directory = '/path/to/mp3/files'
    
    for filename in os.listdir(directory):
        if filename.endswith('.mp3'):
            file_path = os.path.join(directory, filename)
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            
            # If the file is larger than the MAX_FILE_SIZE_MB, split it into chunks
            if file_size_mb > MAX_FILE_SIZE_MB:
                audio_chunks = split_audio_file(file_path)
                transcriptions = []
                previous_transcript = ""  # Initialize an empty previous transcript
                
                for chunk in audio_chunks:
                    # Prepend the previous transcript to the chunk transcription
                    transcript_chunk = transcribe_chunk(chunk, prompt=previous_transcript)
                    transcriptions.append(transcript_chunk)
                    # Update previous_transcript for the next chunk
                    previous_transcript = transcript_chunk
                
                full_transcription = '\n'.join(transcriptions)
                
            else:
                # If the file is smaller than the maximum size, transcribe it directly
                with open(file_path, "rb") as audio_file:
                    full_transcription = openai.Audio.transcribe("whisper-1", audio_file).get('text')
            
            # Write transcription to a .txt file
            with open(os.path.splitext(file_path)[0] + '.txt', 'w') as txt_file:
                txt_file.write(full_transcription)

if __name__ == "__main__":
    # Execute the main function when the script is run directly
    main()
