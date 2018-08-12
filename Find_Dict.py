from bs4 import BeautifulSoup


def del_space(line):
    lst = line.split('\n')
    new_line = ''
    for i in lst:
        new_line += i
    return new_line


def main(file, parent, son, sibling):
    print(file)
    fo = open("Docu/Dict2/5XD0" + file + ".xml", "r+")
    fo2 = open("Docu/Dict2/words.csv", "a+")
    fo3 = open("Docu/Dict2/sentences.csv", "a+")
    line = fo.read()
    soup = BeautifulSoup(line, "lxml")
    un = soup.find_all(parent)
    for elem in un:
        eng = elem.find(sibling)
        chs = elem.find(son)
        if eng and chs:
            if sibling == 'description' and elem.find('synonym'):
                eng = eng[len(elem.find('synonym').text):]
            if sibling == 'description' and eng and not 96 < ord(eng[-1]) < 123:
                eng = ''
            else:
                chs = chs.text.strip().replace(' ', '')
                eng = eng.text.strip().replace('"', "'")
                if chs and eng:
                    string = format('"%s","%s",\n' % (del_space(eng), del_space(chs)))
                    if chs[-1] in "。？”！!.?'’": fo3.write(string)
                    else: fo2.write(string)
    fo.close()
    fo2.close()
    fo3.close()


if __name__ == '__main__':

    for i in range(65, 91):
        if not chr(i) in 'OIUV':
        # if True:
            main(chr(i), 'example', 'source', 'target')
            # main(chr(i), 'subentry', 'word', 'description')

    # main('Dict3', 'example', 'source', 'target')
# <Thesbox>[\s]*?<Collocate>[^.]+?</Collocate>[^.]+?</Thesbox>