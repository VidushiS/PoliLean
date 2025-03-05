from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
from transformers import TrainingArguments, Trainer
# Following the guide given by Shangbin: https://huggingface.co/docs/transformers/en/tasks/language_modeling

def tokenize_fcn(example):
	return tokenizer(example["text"])
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
ds_right = load_dataset("text", data_files="./partisan_media/reddit_right.txt")

print(ds_right)
print(ds_right['train'][0])
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

tokenized_datasets = ds_right.map(
    tokenize_fcn, batched=True, num_proc=4,remove_columns=ds_right["train"].column_names
)
print(tokenized_datasets)
print(tokenized_datasets['train'][0])

from transformers import DataCollatorForLanguageModeling

tokenizer.pad_token = tokenizer.eos_token
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)


model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype="auto", device_map="auto"
)

training_args = TrainingArguments(
    output_dir="reddit_right_deepseek",
    eval_strategy="no",
    learning_rate=1e-4,
    weight_decay=1e-5,
	per_device_train_batch_size=1,
	optim='schedule_free_radam',
	num_train_epochs=1,
    push_to_hub=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    data_collator=data_collator,
    tokenizer=tokenizer,
)

trainer.train()
