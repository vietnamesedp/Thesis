import numpy as np


def calculate_uas(predicted_heads, gold_heads):
    correct = sum(1 for pred, gold in zip(predicted_heads, gold_heads) if pred == gold)
    return correct / len(gold_heads) if gold_heads else 0


def calculate_las(predicted_heads, gold_heads, predicted_deprels, gold_deprels):
    correct = sum(
        1 for pred, gold, pred_label, gold_label in zip(predicted_heads, gold_heads, predicted_deprels, gold_deprels)
        if pred == gold and pred_label == gold_label)
    return correct / len(gold_heads) if gold_heads else 0
