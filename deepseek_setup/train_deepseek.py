from datasets import load_dataset, DatasetDict, Features, Value, Sequence
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForLanguageModeling
import argparse
from argparse import Namespace
import pyarrow as pa
# Following the guide given by Shangbin: https://huggingface.co/docs/transformers/en/tasks/language_modeling

MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize_fcn(example):
	return tokenizer(example["text"])
def tokenize_news_fcn(examples):
    string_array = examples["text"]
    return tokenizer([" ".join(x) for x in string_array])

block_size = 256


def group_texts(examples):
    # Concatenate all texts.
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
    # customize this part to your needs.
    if total_length >= block_size:
        total_length = (total_length // block_size) * block_size
    # Split by chunks of block_size.
    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }
    result["labels"] = result["input_ids"].copy()
    return result


def main(args: Namespace):
    data_file = args.data_file
    data_file_type = data_file.split(".")[-1].strip()
    output_dir= args.output_dir
    percent_train = args.percent
    ds_right = None
    print(data_file_type)
    if data_file_type == "json": 
        features = Features({'text': Sequence(feature=Value(dtype='large_string'))})
        ds_right = load_dataset("json", data_files=data_file, split=f"train[:{percent_train}%]", features=features)
    elif data_file_type == "txt":
        ds_right = load_dataset("text", data_files=data_file, split=f"train[:{percent_train}%]")

    print(ds_right)
    print(ds_right[0]['text'])
    tokenized_dataset = None
    if data_file_type == "json":
        tokenized_datasets = ds_right.map(
            tokenize_news_fcn, batched=True, num_proc=4, remove_columns=ds_right.column_names
        )
    elif data_file_type == "txt":
        tokenized_datasets = ds_right.map(
            tokenize_fcn, batched=True, num_proc=4, remove_columns=ds_right.column_names
        )
    
    print(tokenized_datasets)
    print(tokenized_datasets[0]['input_ids'])
    lm_dataset = None
    if data_file_type == "json":
        lm_dataset = tokenized_datasets.map(group_texts, batched=True, num_proc=4)
    elif data_file_type == "txt":
        lm_dataset = tokenized_datasets
    print(lm_dataset)
    print(lm_dataset[0]['input_ids'])


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
        save_steps=10000
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=lm_dataset["input_ids"],
        data_collator=data_collator,
        tokenizer=tokenizer,
    )
    print('GPU count used by trainer: ',trainer.args._n_gpu)
    trainer.train()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-file", type=str, help="The absolute path to the data file to train on")
    parser.add_argument("--percent", type=int, help="percent of data to train on")
    parser.add_argument("--output-dir",type=str,help="The absolute path to the directory where weights are stored")
    parser.add_argument('--local-rank', type=int, default=0)
    args = parser.parse_args()
    main(args)
