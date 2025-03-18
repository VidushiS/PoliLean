## PoliLean Repository - DeepSeek Training Instructions

This README contains instructions for training the DeepSeek Distilled Model mentioned in the paper for full reproducibility of results. If you want to skip the model training and instead go straight to inference, the models used for this project are publicly available on HuggingFace and links to them are provided in the [Model Checkpoints](#model-checkpoints) Section

### Environment Setup
Virtual Environment was used to setup a space in order to run these experiments. The python version was 3.9.14. Once the environment was activated the requirements outlined in the `requirements_training.py` were pip installed

### Preprocessing the Data
Please refer to the README in the main directory for information on how to receive access to the partisan media and BIGNEWSBLN datasets. These instructions assume that you already have access to both datasets.

The partisan media dataset requires no further preprocessing, and can be used to directly train the model after unzipping it.

The BIGNEWSBLN dataset requires further preprocessing due to all of the data being on a single line (makes most text editors and data loaders crash when trying to load it) and it contains unencoded unicode characters that cause data loaders to crash. To fix this a command line JSON parser called [jq](https://jqlang.org/) was used. Follow the instructions on the linked website to download the appropriate version of jq for your machine.

Once you have done that run the command below to pretty-print the data onto multiple lines (yet retain the array list format) and to re-encode unencoded characters:
```
cat (path_to_raw_dataset).json | jq '.[] | {text: .text}' | jq -s > (output_file).json
```

Use the json file containing the processed data for any model training.

### Training the Model
In order to train the model run the following command:
```
python -m torch.distributed.launch --nproc-per-node=(num_gpus) --nnodes=(num_clusters) train_deepseek.py --data-file (path_to_json_or_txt_data_file) --output-dir (path_to_where_models_are_saved) --percent (percent_of_training_data_to_use)
```

For the purposes of recreating the project, the `--nproc-per-node` was set to 4 and `--nnodes` was set to 1 since the models were trained on a cluster of 4 MI210 GPUs. The `--percent` was set to 10 and 4 when training on the partisan media and BIGNEWSBLN datasets respectively.

Note that the above command requires the data to be in a json or txt format, and expects for there to be a text field in the data that it processes and reads from

The checkpoints will be saved to the `--output-dir` specified

### Pushing to Huggingface
Optionally, for convenience you may want to push your models to Huggingface. In order to do so, first create your own repository on Huggingface, and then run the following command:
```
python push_to_hub.py --source-dir (path_to_where_model_is_stored) --output_dir (username/name_of_repo)
``` 
This will push the model and processor up to Huggingface.

### Model Checkpoints
- [reddit right model](https://huggingface.co/vsingh1221/deepseek_1.5_reddit_right)
- [reddit center model](https://huggingface.co/vsingh1221/deepseek_1.5_reddit_center)
- [reddit left model](https://huggingface.co/vsingh1221/deepseek_1.5_reddit_left)
- [news right model](https://huggingface.co/vsingh1221/politics_right_deepseek)
- [news center model](https://huggingface.co/vsingh1221/politics_center_deepseek)
- [news left model](https://huggingface.co/vsingh1221/politics_left_deepseek)

