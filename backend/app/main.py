import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import supabase_client
from app.pipeline import run_voice_ai_pipeline

app = FastAPI(
    title="Sauti-AI Core Engine",
    description="Backend processing framework for data scaling and accent-mimicking models",
    version="1.0.0"
)

# Enable Cross-Origin Resource Sharing (CORS)
# This allows your Vercel-deployed frontend website to hit your backend API securely.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to your specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def check_health():
    """Simple status check route to verify the server is live."""
    return {"status": "online", "system": "Sauti-AI Engine Running"}


@app.post("/api/upload-dataset")
async def upload_dataset_voice(
    accent: str = Form(...),
    transcript: str = Form(...),
    audio_file: UploadFile = File(...)
):
    """
    Pillar 1 Endpoint: Automated Global Data Collection Track.
    Takes voice drive recordings from anyone in the world and pipes them to Supabase.
    """
    try:
        # Generate a distinct random filename to prevent overwriting existing dataset entries
        file_extension = audio_file.filename.split(".")[-1] if "." in audio_file.filename else "wav"
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Read the binary data from the incoming multipart form file
        file_bytes = await audio_file.read()
        
        # 1. Stream the raw audio file block up into your Supabase Storage Bucket
        bucket_name = "sauti-voice-dataset"
        supabase_client.storage.from_(bucket_name).upload(
            path=unique_filename,
            file=file_bytes,
            file_options={"content-type": audio_file.content_type or "audio/wav"}
        )
        
        # Resolve the persistent public URL of the freshly saved audio asset
        public_file_url = supabase_client.storage.from_(bucket_name).get_public_url(unique_filename)
        
        # 2. Insert an index mapping log metadata row directly into your Database Table
        db_payload = {
            "accent_label": accent,
            "transcription": transcript,
            "audio_url": public_file_url
        }
        supabase_client.table("voice_contributions").insert(db_payload).execute()
        
        return {
            "status": "success",
            "message": "Data contribution successfully recorded",
            "stored_url": public_file_url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data storage pipeline failure: {str(e)}")


@app.post("/api/interact")
async def interact_with_prototype(
    target_accent: str = Form(...),
    user_audio: UploadFile = File(...)
):
    """
    Pillar 2 Endpoint: Live Interactive Prototype Playground.
    Runs speech recognition and responses matching localized phonetic soundscapes.
    """
    try:
        # Pull raw recording bytes from form payload
        user_audio_bytes = await user_audio.read()
        
        # Run audio assets directly through the machine learning execution loop
        ai_audio_url, ai_text_response = run_voice_ai_pipeline(user_audio_bytes, target_accent)
        
        return {
            "status": "success",
            "detected_transcript": "Processed User Input Stream",
            "ai_text_log": ai_text_response,
            "ai_audio_reply_url": ai_audio_url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interactive playback pipeline failure: {str(e)}")