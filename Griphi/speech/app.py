import os
import whisper
from Griphi.other.info import BASE_DIR

model = whisper.load_model("small").cuda()

async def get_transcribe(name):
    result = model.transcribe(os.path.join(BASE_DIR, name), fp16=False)
    return result["text"]


