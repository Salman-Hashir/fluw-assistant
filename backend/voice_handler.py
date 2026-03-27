import whisper, edge_tts, asyncio, os, requests, logging
logger = logging.getLogger(__name__)

try:
    model = whisper.load_model("base")
    logger.info("Whisper loaded")
except Exception as e:
    logger.error(f"Whisper error: {e}"); model = None

VOICES = {
    'malayalam_female': 'ml-IN-SobhanaNeural',
    'malayalam_male':   'ml-IN-MidhunNeural',
    'english_female':   'en-IN-NeerjaNeural',
    'english_male':     'en-IN-PrabhatNeural',
}

def voice_note_to_text(audio_file_path: str) -> str:
    if not model: return "Voice message received"
    try:
        result = model.transcribe(audio_file_path, language=None)
        return result['text'].strip()
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return "Voice message received."

async def text_to_voice_note(text: str, output_path: str = 'reply.mp3') -> str:
    try:
        communicate = edge_tts.Communicate(text, voice=VOICES['english_female'])
        await communicate.save(output_path)
        return output_path
    except Exception as e:
        logger.error(f"TTS error: {e}"); return None

def download_whatsapp_media(media_id: str, token: str) -> str:
    try:
        headers    = {'Authorization': f'Bearer {token}'}
        media_info = requests.get(f"https://graph.facebook.com/v18.0/{media_id}", headers=headers).json()
        media_url  = media_info.get('url')
        if not media_url: raise Exception("No media URL")
        data = requests.get(media_url, headers=headers)
        os.makedirs('downloads', exist_ok=True)
        path = f"downloads/voice_{media_id}.ogg"
        with open(path, 'wb') as f: f.write(data.content)
        return path
    except Exception as e:
        logger.error(f"Media download error: {e}"); return None
