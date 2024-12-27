from data import read_conllu_file
from evaluate import calculate_uas, calculate_las


def score_dp(file_path_gold, file_path_predicted):
    gold_sentences = read_conllu_file(file_path_gold)
    predicted_sentences = read_conllu_file(file_path_predicted)

    total_uas = 0
    total_las = 0
    sentence_count = 0

    for (gold_heads, gold_deprels), (predicted_heads, predicted_deprels) in zip(gold_sentences, predicted_sentences):
        uas = calculate_uas(predicted_heads, gold_heads)
        las = calculate_las(predicted_heads, gold_heads, predicted_deprels, gold_deprels)

        total_uas += uas
        total_las += las
        sentence_count += 1

    # Tính điểm trung bình
    average_uas = total_uas / sentence_count if sentence_count > 0 else 0
    average_las = total_las / sentence_count if sentence_count > 0 else 0
    return average_uas, average_las


def main():
    file_path_gold = './data/gold_file.txt'  # File chứa kết quả đúng
    file_path_predicted = './data/system_file.txt'  # File chứa kết quả dự đoán
    average_uas, average_las = score_dp(file_path_gold, file_path_predicted)
    print("Average UAS:", average_uas)
    print("Average LAS:", average_las)


if __name__ == '__main__':
    main()