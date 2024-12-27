def read_conllu_file(file_path):
    sentences = []
    current_heads = []
    current_deprels = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Bỏ qua các dòng chú thích và dòng trống
            if line.startswith('#') or line.strip() == "":
                if current_heads:  # Nếu có đầu vào trong câu hiện tại
                    sentences.append((current_heads, current_deprels))
                    current_heads = []
                    current_deprels = []
                continue

            # Tách các trường trong dòng
            columns = line.strip().split('\t')

            # Kiểm tra xem có đủ cột
            if len(columns) >= 10:  # 10 là số cột trong định dạng CoNLL-U
                head = columns[6]  # Cột head nằm ở vị trí thứ 7 (index 6)
                deprel = columns[7]  # Cột deprel nằm ở vị trí thứ 8 (index 7)

                current_heads.append(head)
                current_deprels.append(deprel)

        # Thêm câu cuối nếu có
        if current_heads:
            sentences.append((current_heads, current_deprels))

    return sentences

