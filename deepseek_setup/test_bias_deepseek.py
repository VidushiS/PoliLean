import torch
import transformers

# test inference to see if deepseek works with huggingface
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoProcessor

# default: Load the model on the available device(s)
model = AutoModelForCausalLM.from_pretrained(
    "/work1/sadasivan/student18/PoliLean/deepseek_setup/reddit_right_deepseek/checkpoint-45000", torch_dtype="auto", device_map="auto"
)

# We recommend enabling flash_attention_2 for better acceleration and memory saving, especially in multi-image and video scenarios.
# model = Qwen2VLForConditionalGeneration.from_pretrained(
#     "Qwen/Qwen2-VL-72B-Instruct-GPTQ-Int4",
#     torch_dtype=torch.bfloat16,
#     attn_implementation="flash_attention_2",
#     device_map="auto",
# )

# default processer
processor = AutoProcessor.from_pretrained("/work1/sadasivan/student18/PoliLean/deepseek_setup/reddit_right_deepseek/checkpoint-45000")

# The default range for the number of visual tokens per image in the model is 4-16384. You can set min_pixels and max_pixels according to your needs, such as a token count range of 256-1280, to balance speed and memory usage.
# min_pixels = 256*28*28
# max_pixels = 1280*28*28
# processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-72B-Instruct-GPTQ-Int4", min_pixels=min_pixels, max_pixels=max_pixels)
messages = [{"role": "user", "content": "Do you think illegal immigrants should be given sanctuary in the US?"}]
'''
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What are you?"},
        ],
    }
]
'''
# Preparation for inference
text = processor.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
inputs = processor(
    text=[text],
    padding=True,
    return_tensors="pt",
)
inputs = inputs.to("cuda")

# Inference: Generation of the output
generated_ids = model.generate(**inputs, max_new_tokens=128)
generated_ids_trimmed = [
    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
]
output_text = processor.batch_decode(
    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
)
print(output_text)

