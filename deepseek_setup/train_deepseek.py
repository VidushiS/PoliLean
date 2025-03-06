from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
from transformers import TrainingArguments, Trainer
# Following the guide given by Shangbin: https://huggingface.co/docs/transformers/en/tasks/language_modeling

def tokenize_fcn(example):
	return tokenizer(example["text"])
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

data_file = "./partisan_media/reddit_left.txt"
output_dir="./reddit_left_deepseek"
ds_right = load_dataset("text", data_files=data_file, split="train[:10%]")

print(ds_right)
#print(ds_right['train'][0])
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

tokenized_datasets = ds_right.map(
    tokenize_fcn, batched=True, num_proc=4,remove_columns=ds_right.column_names
)
print(tokenized_datasets)
#print(tokenized_datasets['train'][0])

from transformers import DataCollatorForLanguageModeling

tokenizer.pad_token = tokenizer.eos_token
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)


model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype="auto"
)

training_args = TrainingArguments(
    output_dir=output_dir,
    eval_strategy="no",
    learning_rate=1e-4,
    weight_decay=1e-5,
	per_device_train_batch_size=2,
	num_train_epochs=5,
    push_to_hub=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["input_ids"],
    data_collator=data_collator,
    tokenizer=tokenizer,
)
print('GPU count used by trainer: ',trainer.args._n_gpu)
trainer.train()
