def get_file(path, outpath):
    wf = open(outpath, 'w', encoding="utf-8")
    with open(path, 'r', encoding="utf-8") as f:
        dt = f.readlines()
        for data in dt:
            if str(data).strip() != '':
                wf.write(convert_to_three_levels(data))

def convert_to_three_levels(input_string):
    stack = []
    output_string = ""
    level = 0
    for char in input_string:
        if char == '(':
            if stack:
                if len(stack) < 10:
                    output_string += '\n' + '\t' * len(stack)
                if level < 9:
                    level += 1
            stack.append(char)
            if len(stack) == level:
                output_string += '\n' + '\t' * len(stack) + char
            else:
                output_string += char
        elif char == ')':
            stack.pop()
            output_string += char
            if len(stack) <10:
                level-=1
        else:
            output_string += char
    return output_string

get_file("./data/vtb2022_id.txt", './data/vtb2022_id_format.txt')