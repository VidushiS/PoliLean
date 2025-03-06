#from huggingface_hub import notebook_login

#notebook_login()

import torch
import transformers

# test inference to see if deepseek works with huggingface
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoProcessor

# default: Load the model on the available device(s)
model = AutoModelForCausalLM.from_pretrained(
    "/work1/sadasivan/student18/PoliLean/deepseek_setup/reddit_center_deepseek/checkpoint-59500", torch_dtype="auto", device_map="auto"
)
print("model_loaded")
model.push_to_hub("deepseek_1.5_reddit_center")
print("pushed to hub")
