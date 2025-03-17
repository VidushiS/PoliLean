#from huggingface_hub import notebook_login

#notebook_login()

import torch
import transformers

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--source-dir", type=str,help="source directory where model/tokenizer is stored, often a path to a model checkpoint")
parser.add_argument("--dest-dir", type=str, help="destination repo where model/processor should be stored")
args = parser.parse_args()

# test inference to see if deepseek works with huggingface
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoProcessor

model = AutoModelForCausalLM.from_pretrained(
    args.source_dir, torch_dtype="auto", device_map="auto"
)
# default: Load the model on the available device(s)
processor = AutoProcessor.from_pretrained(
    args.source_dir, torch_dtype="auto", device_map="auto"
)
print("model loaded")
model.push_to_hub(args.dest_dir)
print("pushed to hub")
print("processor loaded")
processor.push_to_hub(args.dest_dir)
print("pushed to hub")
