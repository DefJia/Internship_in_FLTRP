class Count:
    def __init__(self, path, mode='01'):
        self.fo = open(path, 'r+')
        self.path = path
        self.mode = mode
        self.eng = 0
        self.chs = 0
        self.cnt_field = len(mode)

    def main(self):
        line = self.fo.readline()
        while line:
            if line[0] == '"':
                tmp = line.split('"')
                line_lst = []
                for elem_ in tmp:
                    if not (elem_ == ',' or elem_ == ''):
                        line_lst.append(elem_)
            else:
                line_lst = line.split(',')
            for i in range(self.cnt_field):
                if self.mode[i] == '1':
                    self.cnt_chs(self.pre(line_lst[i]))
                else:
                    self.cnt_eng(self.pre(line_lst[i]))
            line = self.fo.readline()
        print('%s,%d,%d,' % (self.path, self.eng, self.chs))

    def pre(self, line):
        if line[0] == '"':
            return line[1:-1]
        return line

    def cnt_eng(self, line):
        delta = len(line.split(' '))
        self.eng += delta
        return delta

    def cnt_chs(self, line):
        cnt = 0
        for character in line:
            if character >= u'\u4e00' and character <= u'\u9fa5':
                cnt += 1
        self.chs += cnt
        return cnt

if __name__ == '__main__':
    # lst = ['Brands', 'Names', 'Phrases-ex', 'Phrases-hw', 'Places', 'Sentences']
    lst = ['sentences', 'words']
    for elem in lst:
        cur = Count('Docu/Dict2/'+elem+'.csv', '01')
        cur.main()
