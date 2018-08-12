class Main:
    def __init__(self, path, old):
        self.old = old
        self.fo = open(path + old + '.xml', 'r+')
        self.fo2 = open(path + old + '_.xml', 'w+')
        self.fo3 = open(path + old + '_log.csv', 'w+')
        self.log = ''
        self.new = ''

    def main(self):
        lines = self.fo.read().split('\n')
        count = 0
        for line in lines:
            count += 1
            print(self.old + str(count))
            if line != '':
                space = ''
                while line[0] in (' ', '\t'):
                    space += line[0]
                    line = line[1:]
                tmp = line.find('.')
                if (line[tmp+1].isdigit() and line[tmp-1].isdigit()) or line[tmp+1] == '.':
                    tmp = -1
                if line[:5] == '<DEF>' and tmp > 0 and line[-7] != '.':
                    string = space + line[:-6] + '.' + line[-6:]
                    self.new += string + '\n'
                    log = '"%s","%s",\n,"%s",\n' % (count, line, string[len(space):])
                    self.log += log
                else:
                    self.new += space + line + '\n'
        self.fo2.write(self.new)
        self.fo3.write(self.log)


if __name__ == '__main__':
    for i in range(65, 91):
        cur = Main('Docu/Others/', chr(i))
        cur.main()