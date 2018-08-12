import os, shutil


class Match:
    def __init__(self, source):
        self.s = source
        self.source = open('Docu/Match_audios/%s.csv' % source, 'r+').read().split()
        self.target = dict()
        for root, dirs, files in os.walk('Docu/Match_audios/Audios'):
            self.target[root[-1]] = files

    def copy(self, line, file, letter):
        srcFile = os.path.join('Docu/Match_audios/Audios/' + letter, 'en_gb_%s.mp3' % file)
        targetFile = os.path.join('Docu/Match_audios/Results/' + self.s, str(line) + '_' + file + '.mp3')
        shutil.copyfile(srcFile, targetFile)

    def main(self):
        line = 0
        for elem in self.source:
            line += 1
            s = 'en_gb_%s.mp3' % elem
            if elem[0].islower():
                a = chr(ord(elem[0])-22)
                if s in self.target[elem[0].upper()]:
                    self.copy(line, elem, elem[0].upper())
                    print(s)


if __name__ == '__main__':
    cur = Match('1')
    cur.main()
    cur = Match('2')
    cur.main()