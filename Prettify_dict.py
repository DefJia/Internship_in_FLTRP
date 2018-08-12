import re


class Elem:
    """
        the structure of element.
    """
    def __init__(self, keyword, level, parent):
        self.level = level
        self.keyword = keyword
        self.senses = list()
        self.sons = list()
        self.parent = parent

    def add_sense(self, sense):
        """
        :param sense: string
        :return: length of senses
        """
        self.senses.append(sense)
        return len(self.senses)

    def add_son(self, son):
        """
        :param son: Elem
        :return: length of sons
        """
        self.sons.append(son)
        return len(self.sons)


class Extract:
    def __init__(self, path, file):
        self.ancestor = Elem(file, 0, None)
        self.cur = self.ancestor
        fo = open(path + file + '.txt', 'r+')
        self.path = path
        self.file = file
        self.context = re.split('\n|;', fo.read())
        self.line = 0
        self.results = list()

    def execute(self):
        """
        :return: 0 -> no
        """
        line = self.context[self.line]
        while line and line[0] in ('\t', ' '):
            line = line[1:]
        print(line)
        if line == '' or line.isupper():
            # Others
            return 0
        elif self.is_chinese(line[0]):
            # 词头词
            self.cur = Elem(line[0], 1, self.ancestor)
            self.ancestor.sons.append(self.cur)
            self.context[self.line] = self.context[self.line][1:]
            return 1
        elif line[0] == '【':
            # 二级词头
            while self.cur.level > 1:
                self.cur = self.cur.parent
            tmp = line[1:].split('】')[0]
            self.context[self.line] = self.context[self.line][(len(tmp) + 3):]
            tmp_elem = Elem(tmp, 2, self.cur)
            self.cur.sons.append(tmp_elem)
            self.cur = tmp_elem
            return 2
        elif line[0] == '◇':
            while self.cur.level > 1:
                self.cur = self.cur.parent
            tmp = line[2:].split()[0]
            self.context[self.line] = self.context[self.line][(len(tmp) + 5):]
            # print(self.context[self.line])
            tmp_elem = Elem(tmp, 2, self.cur)
            self.cur.sons.append(tmp_elem)
            self.cur = tmp_elem
            return 2
        elif line[0] == '〖':
            tmp = line[1:].split('〗')[0]
            self.context[self.line] = self.context[self.line][(len(tmp) + 3):]
            tmp_elem = Elem(tmp, 3, self.cur)
            self.cur.sons.append(tmp_elem)
            self.cur = tmp_elem
            return 3
        elif line[-1] == ')' and not line[-2].islower():
            # meanings with chinese
            i = -3
            while not line[i] in ('(', '（'):
                i -= 1
            eng = line[:(i - 1)]
            chs = line[(i + 1): -1]
            string = "%s|%s" % (eng, chs)
            self.cur.senses.append(string)
            return self.cur.level + 5
        else:
            # meanings without chinese
            self.cur.senses.append(line)
            return self.cur.level + 5

    def main(self):
        while self.line < len(self.context):
            flag = self.execute()
            if flag == 0 or flag >= 5:
                self.line += 1
            elif 1 <= flag <= 3:
                pass
        return 0

    def generate(self):
        fo2 = open(self.path + self.file + '.csv', 'w+')
        string = ''
        for elem in self.ancestor.sons:
            string += self.base_gene(elem)
            for elem2 in elem.sons:
                string += self.base_gene(elem2)
                for elem3 in elem2.sons:
                    string += self.base_gene(elem3)
        fo2.write(string)

    @staticmethod
    def base_gene(elem):
        keyword = elem.keyword
        level = elem.level
        # string = ',' * (level*3-3) + '"%s' % keyword + ',' * (12-3*level) + '\n'
        string = '%s"%s"%s\n' % (',' * (level*3-3), keyword, ',' * (12-3*level))
        for sense in elem.senses:
            senses = sense.split('|')
            if len(senses) == 1:
                # string += ',' * (level*3-2) + '"%s"' % senses[0] + ',' * ()
                string += '%s"%s"%s\n' % (',' * (level*3-2), senses[0], ',' * (11-3*level))
            else:
                string += '%s"%s","%s",%s\n' % (',' * (level * 3 - 2), senses[0], senses[1].replace('~', keyword), ',' * (10 - 3 * level))
        return string

    @staticmethod
    def is_chinese(character):
        return (character >= u'\u4e00') and (character <= u'\u9fa5')


if __name__ == '__main__':
    letters = 'BCDFGHJKZ'
    for letter in letters:
        cur = Extract('Docu/Dict_word/', letter)
        cur.main()
        cur.generate()