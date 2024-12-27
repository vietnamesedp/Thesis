import csv

import re


def get_raw(file):
    data = []
    idx = []
    data_chunk = []
    with open(file, 'r', encoding='utf-8') as f:
        dt = f.readlines()
        for d in dt:
            if not d.startswith('<') and d.strip() != '':
                data.append(d.replace('*E*', '').replace('*e*', '').strip().lower())
            if d.startswith('<s'):
                idx.append(d.replace("<s id=", "").replace(">\n", "").replace("<s id = ", "").replace("> ", ""))

    for d in data:
        data_chunk.append(change_punct(d))

    return data, idx, data_chunk


def get_sentence(data):
    result = []
    for dt in data:
        sentence = ''
        for row in dt:
            sentence += ' ' + row[1]
        result.append(sentence.strip())
    return result


def change_punct(sentence):
    return xoa_khoang_trang_thua(re.sub(r'[^\w\s]', ' ', sentence))


def xoa_khoang_trang_thua(s):
    s = s.strip()
    while "  " in s:
        s = s.replace("  ", " ")
    return s


def get_data(path, delimiter):
    sentences = []
    data = open(path, "r", encoding="utf-8")
    data_csv = csv.reader(data, delimiter=delimiter)
    sentence = []
    for d in data_csv:
        if len(d) > 0 and d[0].strip() != '':
            if '\ufeff' in d[0]:
                d[0] = d[0].replace('\ufeff', '')
            if len(d) == 9:
                d[1] = "\""
                d.insert(1, "\"")
            d[1] = d[1].replace(' ', '_')
            sentence.append(d)
        elif len(d) <= 0 or d[0].strip() == '':
            sentences.append(sentence)
            sentence = []

    if sentence:
        sentences.append(sentence)
    return sentences


def format_data(data):
    word = []
    dp = []
    head = []
    label = []
    idx = []
    for sentence in data:
        w = []
        d = []
        h = []
        l = []
        i = []
        for row in sentence:
            w.append(row[1])
            d.append(row[4])
            h.append(row[6])
    pass


def get_idx(data, e):
    indexes = []
    for index, value in enumerate(data):
        if change_punct(value) == e:
            indexes.append(index)
    return indexes


def get_senten_compare(data_ground, data_raw_dp, data, idx, data_punct):
    result = []
    id_compare = []

    for i in range(len(data_raw_dp)):
        if data_raw_dp[i].lower() in data_ground:
            result.append(data[i])
            j = data_ground.index(data_raw_dp[i].lower())
            id_compare.append(idx[j])
        elif change_punct(data_raw_dp[i].lower()) in data_ground:
            result.append(data[i])
            j = data_ground.index(change_punct(data_raw_dp[i].lower()))
            id_compare.append(idx[j])
        elif change_punct(data_raw_dp[i].lower()) in data_punct:
            result.append(data[i])
            j = data_punct.index(change_punct(data_raw_dp[i].lower()))
            id_compare.append(idx[j])
        # elif 'nhưng ông hoàng bé nhỏ lấy làm kinh ngạc .' == data_raw_dp[i]:
        #     result.append(data[i])
        #     id_compare.append(988)

    return result, id_compare


def get_rule():
    rule_vcp = {'nsubj': 'NP-SUB', 'root_V': 'VP', 'root_N': 'NP', 'obj': 'NP', 'obl': 'NP-SUB',
                'amod': 'AP', 'nmod': 'NP', 'conj_V': 'VP', 'appos:nmod': 'VP', 'aux': 'VP',
                'acl:subj': 'VP', 'obl:comp': 'NP', 'expl': 'NP-TPC', 'aux:pass': 'VP',
                'case': 'PP', 'parataxis': 'VP', 'ccomp': 'VP', 'cop': 'VP', 'conj_Nc': 'NP',
                'xcomp': 'VP', 'PRE_case': 'PP'}
    # 'clf': 'NP-PRD',
    rule_head = {'acl:subj': '-H', 'nsubj': '-H', 'root_N': '-H', 'root_V': '-H', 'expl': '-H', 'clf': '-H',
                 'cop': '-H', 'conj': '-H', 'obl:comp': '-H', 'advcl': '-H',
                 'aux': '-H', 'case': '-H', 'aux:pass': '-H'}

    rule_s = {'nsubj': 'S'}
    return rule_vcp, rule_head, rule_s


def get_id_root(sentence):
    for row in sentence:
        idx = int(row[0])
        head = int(row[6])
        if head == 0:
            return idx
    return -1


def get_id_head_equal_root(sentence, id_root):
    id_head_equal_root = []
    for row in sentence:
        idx = int(row[0])
        head = int(row[6])
        if head == id_root:
            id_head_equal_root.append(idx)
    return id_head_equal_root


def get_cluster_by_id(sentence, id_root):
    id_list = []
    for row in sentence:
        idx = int(row[0])
        head = int(row[6])
        if head == id_root:
            id_list.append(idx)
            id_sub = get_cluster_by_id(sentence, idx)
            id_list += id_sub
    return id_list


def transform_word(sentence):
    pass


def convertDP2VCP(sentence, rule_vcp, rule_head, rule_s):
    str_vcp = ''
    vcp = ''
    id_root = get_id_root(sentence)
    id_head_root = get_id_head_equal_root(sentence, id_root)
    id_head_root.append(id_root)
    check = [0] * len(sentence)
    # print(check)
    word_ = 0
    count = 0
    # print(sentence)
    for row in sentence:
        idx = int(row[0])
        # print(idx)
        if check[idx - 1] == 1:
            continue

        if row[1] == '(':
            row[1] = 'LBKT'
            word_ += 1

        if row[1] == ')':
            row[1] = 'RBKT'

        if idx in id_head_root:
            if idx == id_root:
                vcp += convert(sentence, idx, rule_vcp, rule_head, rule_s, count)
                check[idx - 1] = 1
            else:
                id_list = get_cluster_by_id(sentence, idx)
                id_list.append(idx)
                id_sort = list(set(id_list))
                id_sort.sort()
                for i in id_sort:
                    if isinstance(i, list):
                        vcp += convert_list_id(sentence, i, rule_vcp, rule_head, rule_s, check, count)
                    else:
                        vcp += convert(sentence, i, rule_vcp, rule_head, rule_s, count)
                        check[i - 1] = 1

        if (vcp.count('(') - word_) > vcp.count(')'):
            lech = ') ' * ((vcp.count('(') - word_) - vcp.count(')'))
            vcp += lech
        # if vcp.startswith('(NP-SUB'):
        #     vcp = '(S ' + vcp +')'
        # elif vcp.startswith('NP-SUB'):
        #     vcp = '(S (' + vcp + ')'
        str_vcp += vcp
        vcp = ''
        count += 1

    str_vcp = str_vcp.replace('\\s+', ' ')
    if str_vcp.strip().startswith('S '):
        str_vcp = '(' + str_vcp + ' )'
    elif str_vcp.strip().startswith('(S '):
        str_vcp = str_vcp + ' )'
    else:
        str_vcp = '(S ' + str_vcp + ' )'

    if str_vcp.count('(') > str_vcp.count(')'):
        lech = ') ' * (str_vcp.count('(') - str_vcp.count(')'))
        str_vcp += lech
    return str_vcp


def convert_list_id(sentence, idx, rule_vcp, rule_head, rule_s, check, count):
    vcp = ''
    for i in idx:
        vcp += convert(sentence, i, rule_vcp, rule_head, rule_s, count)
        check[i - 1] = 1
    vcp = '(' + vcp + ' )'

    return vcp


def convert(sentence, idx, rule_vcp, rule_head, rule_s, check):
    row = sentence[idx - 1]
    if row[1] == '(':
        row[1] = 'LBKT'

    if row[1] == ')':
        row[1] = 'RBKT'

    word = row[1].replace(' ', '_')
    if word != "-":
        word = word.replace("-", "_")
    dp = row[4]
    label = row[7].strip()
    if label == 'root' and dp == 'V':
        label = 'root_V'
    elif label == 'root' and dp == 'N':
        label = 'root_N'
    elif label == 'conj' and dp == 'V':
        label = 'conj_V'
    elif label == 'conj' and dp.lower() == 'nc':
        label = 'conj_Nc'
    elif label == 'case' and dp.upper() == 'PRE':
        label = 'case_PRE'

    elif 'compound' in label and row[3].lower() == 'sconj' and dp == 'C':
        dp = 'CC'
    elif label == 'mark' and row[3].lower() == 'sconj':
        dp = 'SC'
    # elif label == 'cop' and row[3].lower() == 'aux':
    #     dp = 'V:cop'
    # elif label == 'aux:pass' and dp.lower() == 'aux':
    #     dp = 'V'
    elif label == 'cc' and dp.lower() == 'c':
        dp = 'CC'
    elif label == 'cc' and dp.lower() == 'prt':
        dp = 'SC'
    # elif label == 'aux' and dp.lower() == 'aux':
    #     dp = 'V:mod'
    elif label == 'case' and dp.lower() == 'c' and word.lower() == 'như':
        dp = 'PRE'
    elif label == 'case' and dp.lower() == 'c':
        dp = 'PRE'
    # elif (label == 'nsubj' or label == 'obj' or label == 'nmod:poss') and dp.lower() == 'pro':
    #     dp = 'PRO:per'
    # elif label == 'nsubj' and dp.lower() == 'det':
    #     dp = 'PRO:det'
    # elif (label == 'det:pmod' or label == 'compound') and dp.lower() == 'pro':
    #     dp = 'PRO:dem'
    # elif label == 'obl:comp' and dp.lower() == 'pro':
    #     dp = 'PRO:per'

    # if label == 'aux:pass':
    #     dp = 'V:pass'
    # if dp == 'NU':
    #     dp = 'NUX'
    # elif dp == 'N' and label =='conj':
    #     dp = 'V'
    # elif label == 'discourse' and dp.lower() == 'prt' and word != "đâu":
    #     dp = 'PRO:det'
    # elif label == 'advmod:adj' and dp.lower() == 'adj':
    #     dp = 'ADV'

    # elif label == 'amod' and dp.upper() == 'ADJ':
    #     dp =  "ADJ:det"
    if dp.strip().upper().endswith(':G') or dp == 'SC:G':
        dp = dp.replace(':G', 'G')

    # if ':' not in dp and dp != 'Nb' and dp != 'Ny':
    #     dp = dp.upper()
    # if 'NY' in dp or 'PY' in dp:
    #     dp = dp.replace('Y', 'y')
    # if 'NB' in dp or 'VB' in dp:
    #     dp = dp.replace('B', 'b')

    # if len(word.split("_")) > 1 and dp.lower() == 'nnp':
    #     vcp = '(NP-PN '
    #     for w in word.split("_"):
    #         vcp += '(' + dp.upper() + ' ' + w + ') '
    #     vcp += ')'
    # else:
    if label in rule_vcp.keys():
        if label in rule_head.keys():
            vcp = '(' + rule_vcp[label] + ' (' + dp + rule_head[label] + ' ' + word + ' )'
        else:
            vcp = '(' + rule_vcp[label] + ' (' + dp + ' ' + word + ' )'
    else:
        vcp = '(' + dp + ' ' + word + ' )'

    return vcp


def convert_to_three_levels(input_string):
    stack = []
    output_string = ""
    level = 0
    for char in input_string:
        if char == '(':
            stack.append(char)
            level = min(len(stack), 3)
            output_string += '\n' + '\t' * level + char
        elif char == ')' and stack != []:
            stack.pop()
            output_string += char
            level = min(len(stack), 3)
        else:
            output_string += char
    return output_string


def write_output(file, data, idx):
    with open(file, 'w', encoding='utf-8') as f:
        for i, dt in enumerate(data, 1):
            f.write(f'<s id={i}>\n')
            f.write(convert_to_three_levels(dt) + '\n')
            f.write('</s>\n\n')


def compare_data(dp, raw, delimiter):
    sentences = get_data(dp, delimiter)

    data_ground, idx, data_punct = get_raw(raw)
    data_raw_dp = get_sentence(sentences)
    with open("data_raw.txt", 'a+', encoding='utf=8') as f:
        for dt in data_raw_dp:
            f.write(dt + '\n')
    with open("data_ground_raw.txt", 'a+', encoding='utf=8') as f:
        for dt in data_ground:
            f.write(dt + '\n')

    senten, idx_compare = get_senten_compare(data_ground, data_raw_dp, sentences, idx, data_punct)
    print(len(senten), len(idx_compare))
    return senten, idx_compare


def main():
    rule_vcp, rule_head, rule_s = get_rule()
    # sentences_htb_dp_ground, id_htb = compare_data('data/dp.csv', 'data/htb_raw.txt', ',')
    # sentences_vtb_dp_ground, id_vtb = compare_data('data/VTB_DP.csv', 'data/vtb_raw.txt', '\t')
    dp = get_data('data/dp2022.txt', '\t')
    # sentences_dp_ground = sentences_htb_dp_ground + sentences_vtb_dp_ground
    # print(len(sentences_dp_ground))
    # id_compare = id_htb + id_vtb

    data = [convertDP2VCP(sentence, rule_vcp, rule_head, rule_s) for sentence in dp]

    write_output('data/output.csv', data, [])


main()
