def read_data(file):
    texts = []
    amrs = []
    with open(file, 'r', encoding='utf-8') as f:
        datas = f.readlines()
        sentence_amr = ''
        for data in datas:
            if data.startswith('::snt'):
                texts.append(data.replace('::snt','').strip())
            elif not data.startswith('::'):
                sentence_amr += data
            elif data.startswith('::id') and sentence_amr:
                amrs.append(sentence_amr.strip())
                sentence_amr = ''
        if sentence_amr:
            amrs.append(sentence_amr.strip())

        return texts, amrs