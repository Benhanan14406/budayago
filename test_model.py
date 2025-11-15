import scipy
from modules.ai_conversation.const import JAWA_PRE_PROMPT, SUNDA_PRE_PROMPT

from transformers import VitsModel, AutoTokenizer
import torch

model = VitsModel.from_pretrained("facebook/mms-tts-ind")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-ind")

text = JAWA_PRE_PROMPT
inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    output = model(**inputs).waveform

scipy.io.wavfile.write("techno.wav", rate=model.config.sampling_rate, data=output.squeeze().cpu().numpy())
