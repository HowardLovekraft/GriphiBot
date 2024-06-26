import os
import whisper
from other.info import BASE_DIR

model = whisper.load_model("small").cuda()


async def get_transcribe(name):
    result = model.transcribe(os.path.join(BASE_DIR, name), fp16=False)
    text = result["text"]
    return text if text else "Речи в сообщении нет"
