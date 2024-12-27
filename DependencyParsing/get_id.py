import os


def read_file(id_path):
    ids = []
    with open(os.path.join(id_path), 'r', encoding='UTF-8') as f:
        dt = f.readlines()
        for data in dt:
            if "<s id" in data:
                ids.append(data.replace("<s id=", "").replace(">\n", "").replace("<s id = ", "").replace("> ", ""))

    # htb = ids[:176]
    # vtb = ids[176:]
    with open('D:/Nghien_cuu/DP_VCP/DP2VCP/data/list_id.txt', 'w', encoding='UTF-8') as id_f:
        id_f.write(', '.join(ids))
        # id_f.write('htb: ')
        # id_f.write(", ".join(htb))
        # id_f.write("\n")
        # id_f.write('vtb: ')
        # id_f.write(", ".join(vtb))
        # id_f.write("\n")


read_file('D:/Nghien_cuu/DP2VCP/data/output.csv')
