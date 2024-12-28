from data import read_data
from sort_sentence import get_num_text


def main():
    file = './train_viamr.txt'
    texts, amrs = read_data(file)
    text = '- chúc một ngày tốt lành , em nói .'
    text_similar, amr_similar = get_num_text(text, texts, amrs, 1)
    print(text_similar)
    print(amr_similar)


if __name__ == '__main__':
    main()
