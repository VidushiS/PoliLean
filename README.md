## PoliLean Repository

This is a repository that recreates experiments presented in [From Pretraining Data to Language Models to Downstream Tasks: Tracking the Trails of Political Biases Leading to Unfair NLP Models](https://arxiv.org/abs/2305.08283).

### Training the models
Please refer to the `deepseek_setup` folder for model fine-tuning instructions. Note that the `README_training.md` file in there contains instructions to do this as well as links to the finetuned models on HuggingFace used for this experiment. Once you are done verifying our work, the links to the HF models will be set to private as was done in the original paper.

### Evaluate the Political Leaning of Language Models
Any environment with the HuggingFace Transformers that support pipelines should work. You might need to additionally install `selenium` for step 3.

#### Step 0: Sanity Check
We mainly implement things with the text generation pipeline of Huggingface Transformers. Check out your HuggingFace model compatibility by running:
```
python step0_hftest.py --model <your_model> --device <your_device>
```
If you see `success!` printed out, you are good to go. If not, or if your model is not compatible with Huggingface Transformers (e.g. OpenAI models), you can skip this step. The default device is `-1` (CPU), but you can specify a GPU device by setting `--device <your_device>`.

#### Step 1: Generate Responses
If your step 0 is successful, run:
```
python step1_response.py --model <your_model> --device <your_device> --test <PCT or 8values>
```
There should be a jsonl file in `response/` with your model name. If you want to generate responses with your own prompts, you can modify line 22: make sure to keep the `<statement>` placeholder in your prompt template.

Note that 1) we only prompt once for clarity and efficiency, while the paper used an average of 5 runs; 2) we used the default prompt in the script, while different models might work better with different prompts to better elicit political biases. These two factors, among others (e.g. LM checkpoint update, etc.), that might lead to result varaition.

If your model is not compatible with Huggingface Transformers, feel free to get them to respond to the political statements in `response/example.jsonl` in your own fashion, change the `response` fields, and save the file as `response/<your_model>.jsonl`.

Note that we support both the Political Compass Test (PCT) and 8values test (8values) there is an option you can pass in to have the model answer prompts from either of the tests.

#### Step 2: Get Agree/Disagree Scores
We use an NLI-based model to evaluate whether the response agrees or disagrees with the political statement. Run:
```
python step2_scoring.py --model <your_model> --device <your_device> --test <PCT or 8values>
```
There should be a txt file in `score/` with your model name. Each line presents the agree/disagree probabilities for each political statement.

Note that we support both the Political Compass Test (PCT) and 8values test (8values) there is an option you can pass in to score the model's answers to the prompts from either of the tests.

#### Step 3: Get Political Leaning with the Political Compass Test
Important: Run this step on your local computer. We need to use `selenium` to simulate the Chrome browser and auto-click based on the scores in step 2.

1) Download the Chrome browser execuatble at [link](https://chromedriver.chromium.org/downloads). Make sure to check the current version of your Chrome browser and download the same version.

2) Download the adblocker `crx` file at [link](https://www.crx4chrome.com/crx/31927/).

3) Change the paths to the browser executable and adblocker in `step3_testing_functional.py` (lines 68 and 72) for running the Political Compass Test and in `step3_testing_functional_eightValues.py` (lines 56 and 60) for running the 8values quiz.

4) To run the model's selections on the Political Compass Test, run `python step3_testing_functional.py --model <your_model>`. To run the model's sections for the 8values quiz, run `python step3_testing_functional_eightValues.py --model <your_model>`. The script will automatically open the Chrome browser and take the test. The final political leaning will be displayed on the website. Please note that the browser will first be on the adblocker tab, make sure not to close it and switch to the political compass test tab after the ad blocker is successfully loaded.
  - To automatically run all 6 models created in this project on both the Political Compass Test and the 8values quiz, run `./run_tests.sh`.

5) Each test will save a pdf of the final results to this directory which can be further analyzed.

### Partisan Corpora and Language Models
For partisan news corpora, visit [POLITICS](https://github.com/launchnlp/politics). For partisan social media corpora, please include your name, affiliation, institutional email address and apply for access at [link](https://drive.google.com/file/d/1rtiHmv868NpmWYJ-09LPrpGtxoQR4HOL/view?usp=sharing).

### Citation
We based our project off of the paper below:
```
@inproceedings{feng-etal-2023-pretraining,
    title = "From Pretraining Data to Language Models to Downstream Tasks: Tracking the Trails of Political Biases Leading to Unfair {NLP} Models",
    author = "Feng, Shangbin  and
      Park, Chan Young  and
      Liu, Yuhan  and
      Tsvetkov, Yulia",
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.acl-long.656",
    doi = "10.18653/v1/2023.acl-long.656",
    pages = "11737--11762",
    abstract = "Language models (LMs) are pretrained on diverse data sources{---}news, discussion forums, books, online encyclopedias. A significant portion of this data includes facts and opinions which, on one hand, celebrate democracy and diversity of ideas, and on the other hand are inherently socially biased. Our work develops new methods to (1) measure media biases in LMs trained on such corpora, along social and economic axes, and (2) measure the fairness of downstream NLP models trained on top of politically biased LMs. We focus on hate speech and misinformation detection, aiming to empirically quantify the effects of political (social, economic) biases in pretraining data on the fairness of high-stakes social-oriented tasks. Our findings reveal that pretrained LMs do have political leanings which reinforce the polarization present in pretraining corpora, propagating social biases into hate speech predictions and media biases into misinformation detectors. We discuss the implications of our findings for NLP research and propose future directions to mitigate unfairness.",
}
```
