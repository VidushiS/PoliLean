from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer

def tokenize(element):
    outputs = tokenizer(
        element["text"],
        truncation=True,
        return_overflowing_tokens=True,
        return_length=True,
    )
    input_batch = []
    for length, input_ids in zip(outputs["length"], outputs["input_ids"]):
        if length == context_length:
            input_batch.append(input_ids)
    return {"input_ids": input_batch}






ds_right = load_dataset("text", data_files="./partisan_media/test_data.txt")
#load_dataset("text", data_files={"train": ["my_text_1.txt", "my_text_2.txt"], "test": "my_test_file.txt"})
#dataset_dict = DatasetDict(
#    {
#        "train": ds_right,  # .shuffle().select(range(50000)),
#    }
#)

print(ds_right)
print(ds_right['train'][0])
#print(dataset_dict["train"]['train'][0])
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")

outputs = tokenizer(
    ds_right['train']["text"],
    truncation=True,
    return_overflowing_tokens=True,
    return_length=True,
)

print(outputs)

tokenized_datasets = ds_right.map(
    tokenize, batched=True, remove_columns=ds_right["train"].column_names
)
print(tokenized_datasets)
