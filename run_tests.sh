#! /usr/bin/bash
echo "Political Compass tests"
echo "Running Politics left:"
python step3_testing_functional.py --model politics_left_deepseek --threshold 0.3

echo "Running Politics right:"
python step3_testing_functional.py --model politics_right_deepseek --threshold 0.3

echo "Running Politics center:"
python step3_testing_functional.py --model politics_center_deepseek --threshold 0.3

echo "Running Reddit left:"
python step3_testing_functional.py --model deepseek_1.5_reddit_left --threshold 0.3

echo "Running Reddit right:"
python step3_testing_functional.py --model deepseek_1.5_reddit_right --threshold 0.3

echo "Running Reddit center:"
python step3_testing_functional.py --model deepseek_1.5_reddit_center --threshold 0.3

echo "8Values Quiz tests"

echo "Running Politics left:"
python step3_testing_functional_eightValues.py --model politics_left_deepseek_eight_values --threshold 0.3

echo "Running Politics right:"
python step3_testing_functional_eightValues.py --model politics_right_deepseek_eight_values --threshold 0.3

echo "Running Politics center:"
python step3_testing_functional_eightValues.py --model politics_center_deepseek_eight_values --threshold 0.3

echo "Running Reddit left:"
python step3_testing_functional_eightValues.py --model deepseek_1.5_reddit_left_eight_values --threshold 0.3

echo "Running Reddit right:"
python step3_testing_functional_eightValues.py --model deepseek_1.5_reddit_right_eight_values --threshold 0.3

echo "Running Reddit center:"
python step3_testing_functional_eightValues.py --model deepseek_1.5_reddit_center_eight_values --threshold 0.3
