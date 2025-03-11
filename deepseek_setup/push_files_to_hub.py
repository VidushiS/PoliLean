#from huggingface_hub import notebook_login

#notebook_login()

import torch
import transformers

# test inference to see if deepseek works with huggingface
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoProcessor

# default: Load the model on the available device(s)
model = AutoModelForCausalLM.from_pretrained(
    "/work1/sadasivan/student18/PoliLean/deepseek_setup/news_center_deepseek/checkpoint-50910", torch_dtype="auto", device_map="auto"
)
print("model_loaded")
model.push_to_hub("politics_center_deepseek")
print("pushed to hub")
