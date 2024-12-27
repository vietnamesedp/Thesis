import sys
# from unittest import result  # For command line arguments
import os
# Splits text into parts. Each part represent a single tree.
import re
import json


def make_patiton_from_lines(lines, startTag, endTag):
    text = ""
    parts = []
    count = 0
    idx = -1
    part_dict = {}

    for line in lines:
        l = line.strip()
        if l.lower().endswith("</s>"):

            if l.lower() != '</s>':
                text += l.replace("</s>", '')
            count += 1
            if len(text) > 2:
                p = partition(text, startTag, endTag)
                parts += p
                if idx >= 0:
                    part_dict[idx] = p
                    idx = -1
                # if len(p) > 1:
                #     print(p, text)
                # elif len(p) == 0:
                # print("NOTE..x",count, l, text)
            # else:
            # print("NOTE...",count, l, text)
        elif l.lower().startswith("<s "):
            text = ""
            idx = int(l[l.index('id=') + 3:l.index('>')])
            # print(idx)
            if not l.endswith('>'):
                text += re.sub('<s\s+id=\d+>', '', l)

        else:
            text += l

    # print("count = ",count)
    return parts, part_dict


def partition(text, startTag, endTag):
    partitions = []
    i = 0
    level = 0
    for c in text:
        if c == startTag:
            if level == 0:
                start = i
            level = level + 1
        if c == endTag:
            level = level - 1
            if level == 0:
                partitions.append(text[start:(i + 1)])
        i = i + 1
    return partitions


# Converts some nested text into tree.


def textToTree(text, startTag, endTag):
    node = ''
    children = []
    i = 0
    level = 0
    for c in text:

        if c == startTag:
            level = level + 1

            if level == 1:
                nodeStart = i + 1

            if level == 2 and not node:
                node = text[nodeStart:i]
                childStart = i

        if c == endTag:
            level = level - 1

            if level == 1:
                childEnd = i + 1
                children.append(textToTree(
                    text[childStart:childEnd], startTag, endTag))
                childStart = i + 1

            if level == 0 and not node:
                node = text[nodeStart:i]

        i = i + 1
    if level != 0:
        return None  # TODO: viska hoopis erind
    return node, children


# Returns the tag form a tag-word pair


def getTag(text):
    s = text.split()
    if s:
        return s[0].strip()
    return ''


# Returns the word form a tag-word pair


def getWord(text):
    s = text.split()
    if len(s) > 1:
        return ' '.join(s[1:]).strip()
    return ''


# Cleans a tree from spefic tags tags eg. NP-SBJ and -NONE-


def clean(node):
    i = 0
    cleanChildren = []
    for child in node[1]:
        cleanChild = clean(child)
        if cleanChild:
            cleanChildren.append(cleanChild)
    tag = getTag(node[0])
    # print('node ........',(node[0]), '|->word....','|%s|'%(getWord(node[0])))
    word = getWord(node[0])
    if tag == '-NONE-' or word == '*T*' or word == "*E*" or word == '*0*':
        return None
    return (tag.split('-', 1)[0] + ' ' + getWord(node[0]), cleanChildren)


# Returns a lis of tuples representing tags and their span.
# Tuples have form (tag start, tag end, tag name).


def getSegments(node, startPos):
    segments = []

    endPos = startPos

    for child in node[1]:
        childSegments = getSegments(child, endPos)
        endPos = childSegments[len(childSegments) - 1][1] + 1
        segments.extend(childSegments)

    if node[1]:
        endPos = endPos - 1

    tag = getTag(node[0])
    segments.append((startPos, endPos, tag))

    return segments


# Prints a list to screen


def printList(list):
    for l in list:
        print(l)


# Prints disagreements to screen


def printDisagreements(disagreements):
    for d in disagreements:
        if d[1]:
            strings = []
            for s in d[1]:
                strings.append(str(s[2]))
            print(str(d[0][2]) + ' <==> ' + ' & '.join(strings))
        else:
            print(str(d[0][2]) + ' <==> ?')


# Checks if two segments are equal


def equal(segment1, segment2):
    if segment1[0] == segment2[0] and segment1[1] == segment2[1] and segment1[2].upper() == segment2[2].upper() :
        return True
    return False


def is_false_tag(segment1, segment2):
    # print("=========================",segment1[0], segment1[1], segment1[2])
    if segment1[0] == segment2[0] and segment1[1] == segment2[1] and segment1[2].upper()  != segment2[2].upper() :
        # print("Lỗi: ",segment1, segment2)
        return True
    return False


def equal_soft(segment1, segment2, s1, s2):
    if segment1[0] == segment2[0] and segment1[1] == segment2[1]:
        if segment1[2].upper()  == segment2[2].upper() :
            return True
        else:
            for x in s1:
                if x != segment1 and x[0] == segment1[0] and x[1] == segment1[1] and x[2].upper()  == segment2[2].upper() :
                    return True
    return False


def clean_neted_spans(segment):
    i = 0

    while i < len(segment) - 1:

        if segment[i][:2] == segment[i + 1][:2]:
            del segment[i + 1]
            i -= 1

        i += 1


# Checks if two segments cover the same words


def equalSpan(segment1, segment2):
    if segment1[0] == segment2[0] and segment1[1] == segment2[1]:
        return True
    return False


# Evaluates segments1 based on segments2
def evaluate(segments1, segments2, idx):

    correct = 0
    crossings = 0
    errors = []
    false_map_dict = {}
    if not exactMatch:
        clean_neted_spans(segments1)
        clean_neted_spans(segments2)

    # print(segments2)
    # print(segments1)
    # print('-----------------------------------------------')
    for s2 in segments2:
        for s1 in segments1:
            # print(s2, s1)
            if is_false_tag(s1, s2):
                # print("có lỗi")
                l = s1[2] + '#' + s2[2]
                if l in false_map_dict:
                    false_map_dict[l][0] += 1
                    if idx not in false_map_dict[l][1]:
                        false_map_dict[l][1].append[idx]
                else:
                    false_map_dict[l] = [1, [idx]]
            if equal(s1, s2):
                correct = correct + 1
                break

                # print("%s vs %s" %(s1, s2))
    precision = float(correct) / len(segments1)
    recall = float(correct) / len(segments2)
    f1score = 0.0
    if precision + recall > 0:
        f1score = 2 * precision * recall / (precision + recall)

    return precision, recall, f1score, errors, false_map_dict


def eval_submission(segments1, segments2, code):
    precision = recall = crossing = 0
    false_map_dict = {}
    for i in range(len(code)):
        idx = code[i]
        if idx in segments1:
            # print("idx: ", idx ,"---------------------------------------------------")
            eval = evaluate(segments1[idx], segments2[idx], idx)
            # print(segments1[idx], '\n',segments2[idx],  '\nidx = ', idx, 'eval= ', eval)
            precision = precision + eval[0]
            recall = recall + eval[1]
            crossing = crossing + eval[2]
            # print(eval[4])
            for l in eval[4]:
                # print("vao day dc ko")
                if l in false_map_dict:
                    false_map_dict[l][0] += eval[4][l][0]
                    if idx not in false_map_dict[l][1]:
                        false_map_dict[l][1].append(idx)
                else:
                    false_map_dict[l] = eval[4][l]
        else:
            print('MISSING sentence in your submission... this sentence treat as failure')
            print(idx)

    precision = precision / len(code)
    recall = recall / len(code)
    f1score = 0
    if precision + recall > 0:
        f1score = 2 * precision * recall / (precision + recall)

    return precision, recall, f1score, false_map_dict


def check_duplicate_label(segment, part, output):
    of = open(output, 'wt', encoding='utf8')
    for i in range(len(segment)):
        s = segment[i]
        for t in range(len(s)):
            for k in range(t + 1, len(s)):

                if s[t][0] == s[k][0] and s[t][2] == s[k][2] and s[t][1] == s[k][1]:
                    print(s[t], 'vs', s[k])
                    print(part[i])
                    of.write('%s vs %s \n' % ((s[t], s[k])))
                    of.write('%s\n' % (part[i]))
                    break
    of.close()


########## Execution start here ##########
if __name__ == '__main__':
    startTag = '('
    endTag = ')'

    doCleanup = False
    showTrees = False
    showSegments = True
    showIndividualEval = False
    showDisagreements = False
    global exactMatch
    exactMatch = True
    fileNames = []
    data = []  # A List for holdin trees and segments

    # chạy lệnh: python resultanlz.py . . (hai dấu . . để cho lệnh bên dưới)
    [_, input_dir, output_dir] = sys.argv
    # print(input_dir)
    submission_dir = os.path.join(input_dir, 'res')
    truth_dir = os.path.join(input_dir, 'ref')
    # print(truth_dir)
    doCleanup = True
    # fileNames.append(os.path.join(submission_dir, 'results.csv'))
    # fileNames.append(os.path.join(truth_dir, 'ground_truth.csv'))

    fileNames.append(r'D:\Nghien_cuu\DP_VCP\DP2CP\data\output.csv')
    fileNames.append(
        r'D:\Nghien_cuu\DP_VCP\DP2CP\data\vtb2022_id.txt')
    fileNames.append(r'D:\Nghien_cuu\DP_VCP\DP2CP\data\list_id.txt')

    # Process the first file

    try:
        # print("Filenames = ",fileNames)
        # print(fileNames[0])
        file1 = open(fileNames[0], 'r', encoding='utf-8')

        text1 = file1.readlines()
        file1.close()
    except:
        print('Invalid results file.', fileNames[0])
        with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file:
            output_file.write(
                "F1: {:f}\nInvalid submission file name. To submit the results, the user is required to submit a zip file that contains a results.csv.".format(
                    -1))
        sys.exit()
    try:
        trees1 = []
        segments1 = {}
        _, parts1 = make_patiton_from_lines(text1, startTag, endTag)
        # print(parts1)
        for part in parts1:
            tree = textToTree(parts1[part][0], startTag, endTag)
            if doCleanup:
                tree = clean(tree)
            trees1.append(tree)
            segments1[part] = getSegments(tree, 1)
    except:
        print("In your result contains a invalid tree ...")
        with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file:
            output_file.write(
                "F1: {:f}\nThe tree structure is incorrect, please check your results and try again, ".format(-1))
        sys.exit()

    # Process the second file

    try:
        file2 = open(fileNames[1], 'rt', encoding='utf-8')
        # print(fileNames[1])
        text2 = file2.readlines()
        file2.close()
        # lit = text2[0]
        # litIDX = [int(i) for i in lit[4:].strip().split(', ')]
        vtb = text2[0]
        vtbIDX = [int(i) for i in vtb[4:].strip().split(', ')]
        # lit = text2[2]
        # litIDX = [int(i) for i in lit[4:].strip().split(', ')]
        text2 = text2[1:]
        # print(text2)


        # print(yteIDX, nerIDX)
    except Exception as e:
        print('Invalid file gold file.', fileNames[1])
        print(e)
        sys.exit()

    try:
        file3 = open(fileNames[2], 'rt', encoding='utf-8')
        text3 = file3.readlines()
        file3.close()
        output = text3[0]
        IDX_sum = [int(i) for i in output[len("output.csv: "):].strip().split(', ')]
    except Exception as e:
        print('Invalid file gold file.', fileNames[2])
        print(e)
        sys.exit()

    trees2 = []
    segments2 = {}
    _, parts2 = make_patiton_from_lines(text2, startTag, endTag)
    for part in parts2:
        tree = textToTree(parts2[part][0], startTag, endTag)
        if doCleanup:
            tree = clean(tree)
        trees2.append(tree)
        segments2[part] = getSegments(tree, 1)

    # Evaluate and print the output

    # print('')

    total = vtbIDX
    # print(total)

    segments1 = {k: segments1[k] for k in total if k in segments1}

    ccheck = True

    if len(segments1) != len(segments2):
        print(
            "The number of trees in yours result is different from the number of trees in the reference.\nNotice that the trees are scoped by round brackets, please check your results!")
        ccheck = False

    eprecision, erecall, ef1score, fmap = eval_submission(segments1, segments2, total)
    # print("fmap: ", fmap)
    print('exactMatch')
    # print(fmap)
    # json.dump(fmap, open(
    #     r'D:\\Nghien_cuu\\DP2VCP\\data\\test.json',
    #     'wt', encoding='utf8'), ensure_ascii=False)
    # mp, mr, mf, fmap = eval_submission(segments1, segments2, litIDX)
    # print("Medical")
    # print(fmap)
    # gp, gr, gf, fmap = eval_submission(segments1, segments2, nerIDX)
    # print('News')
    # print(fmap)
    exactMatch = False
    precision, recall, f1score, fmap = eval_submission(segments1, segments2, total)
    json.dump(fmap, open(
        r'D:\Nghien_cuu\DP_VCP\DP2CP\data\test_soft.json',
        'wt', encoding='utf8'), ensure_ascii=False)

    print('Soft match')
    # print(fmap)
    print('########## TOTAL soft ##########')
    print('')
    print('Average precision, recall and f1 score:')
    print((precision, recall, f1score))

    print('\n########## TOTAL exactly ##########')
    print('')
    print('Average precision, recall and f1 score:')
    print((eprecision, erecall, ef1score))

    # with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file:
    #     output_file.write(
    #         "F1: {:f}\nP: {:F}\nR: {:f}\nF1s: {:f}\nP_new: {:F}\nR_new: {:f}\nP_med: {:F}\nR_med: {:f}".format(ef1score,
    #                                                                                                            eprecision,
    #                                                                                                            erecall,
    #                                                                                                            f1score,
    #                                                                                                            gp, gr,
    #                                                                                                            mp, mr))
    #     if not ccheck:
    #         output_file.write(
    #             "\nThe number of trees in yours result is different from the number of trees in the reference.\nNotice that the trees are scoped by round brackets, please check your results!")
