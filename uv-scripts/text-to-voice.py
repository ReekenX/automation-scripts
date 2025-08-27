#!/usr/bin/env python3
# /// script
# dependencies = [
#   "elevenlabs",
#   "pydub",
# ]
# ///
"""
Simple ElevenLabs CLI script to play "Task finished successfully" message
Usage: uv run uv-scripts/text-to-voice.py [custom_message]
"""

import sys
import os
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import io
import os
import subprocess
import tempfile

def main():
    # Get message from command line argument or use default
    message = sys.argv[1] if len(sys.argv) > 1 else "Task finished successfully"
    
    # Initialize ElevenLabs client
    # Make sure to set your API key as an environment variable: ELEVENLABS_API_KEY
    client = ElevenLabs()
    
    try:
        # Available female voice IDs
        rachel_voice_id = "21m00Tcm4TlvDq8ikWAM"
        domi_voice_id = "AZnzlk1XvdvUeBnXmlld"
        bella_voice_id = "EXAVITQu4vr4xnSDxMaL"      # Bella - warm, engaging
        elli_voice_id = "MF3mGyEYCl7XYWbV9V6O"       # Elli - young, energetic  
        charlotte_voice_id = "XB0fDUnXU5powFXDhCwa"  # Charlotte - seductive, mature
        serena_voice_id = "pMsXgVXv3BLzUgSXRplE"     # Serena - middle-aged, pleasant
        grace_voice_id = "oWAxZDx7w5VEj9dCyTzz"      # Grace - young adult, Southern US accent
        lily_voice_id = "pFZP5JQG7iQjIQuC4Bku"      # Lily - middle-aged, British accent
        jessica_voice_id = "cgSgspJ2msm6clMCkdW9"  # Jessica - young adult, British accent

        # Generate audio
        audio_generator = client.text_to_speech.convert(
            text=message,
            voice_id=jessica_voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        
        # Convert generator to bytes
        audio_bytes = b''.join(audio_generator)
        
        # Convert audio bytes to AudioSegment and reduce volume by 50% (-6 dB)
        audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
        quieter_audio = audio_segment - 6  # Reduce volume by 6 dB (approximately 50%)
        
        # Export to temporary file and play with ffplay (suppressing output)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            quieter_audio.export(tmp_file.name, format="mp3")
            tmp_filename = tmp_file.name
        
        # Play using ffplay with suppressed output
        try:
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", tmp_filename],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        finally:
            # Clean up the temporary file
            os.unlink(tmp_filename)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()