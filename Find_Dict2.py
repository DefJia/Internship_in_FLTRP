from bs4 import BeautifulSoup


def del_space(line1):
    lst = line1.split('\n')
    new_line = ''
    for i in lst:
        new_line += i
    return new_line


class Dict:
    def __init__(self, order):
        file_name = 'batch_%02d_LARGEENGLISHCHINESE2.xml' % order
        self.fo = open("Docu/Dict/" + file_name, "r+")
        line = self.fo.read()
        self.fo.close()
        self.soup = BeautifulSoup(line, "lxml")
        self.data = dict()
        # self.content = ['Sentences', 'Phrases-ex', 'Phrases-hw', 'Names', 'Places', 'Brands']
        for i in self.data:
            self.data[i] = '1st-Category,2nd-Category,3rd-Category,Word_en,Word_ch,Example_en,Example_ch,\n'

    def find_label(self):
        entries = self.soup.find_all('entry')
        for entry in entries:
            sensecats = entry.find_all('sensecat')
            if sensecats:
                class_a = ''
                if sensecats[0].previous_sibling and sensecats[0].previous_sibling.name == 'ulsubjfld':
                    class_a = sensecats[0].previous_sibling['value']
                for sensecat in sensecats:
                    classes = sensecat.find_all('lbsubjfld')
                    if classes or class_a:
                        eng = entry.find('hw').text
                        print(eng)
                        chs_pre = sensecat.find('tran')
                        if chs_pre: chs = chs_pre.text
                        else: chs = ''
                        # exmplgrps = sensecat.find_all('exmplgrp')
                        if class_a:
                            classes = [{'value': class_a}]
                        for class_ in classes:
                            class_name = class_['value']
                            expls = sensecat.find_all('exmplgrp')
                            expl_chs = ''
                            expl_eng = ''
                            '''
                            if expls:
                                expl_eng = expls[0].find('exmpl').text
                                expl_chs_pre = expls[0].find('tran')
                                if expl_chs_pre: expl_chs = expl_chs_pre.text
                                del expls[0]
                            self.generate(eng, chs, class_name, expl_eng, expl_chs)
                            for expl in expls:
                                expl_eng = expl.find('exmpl').text
                                expl_chs_pre = expl.find('tran')
                                if expl_chs_pre: expl_chs = expl_chs_pre.text
                                self.generate('', '', class_name, expl_eng, expl_chs)
                            '''
                            for expl in expls:
                                expl_eng = expl.find('exmpl').text
                                expl_chs_pre = expl.find('tran')
                                if expl_chs_pre: expl_chs = expl_chs_pre.text
                                self.generate(eng, chs, class_name, expl_eng, expl_chs)

    def classify(self):
        entries = self.soup.find_all('entry')
        for entry in entries:
            hw = entry.find('hw')
            eng = hw.text
            chs = entry.find('tran')
            print(eng)
            if not chs:
                pass
            elif 'firstname' in hw.attrs:  # Names
                class_ = 'Names'
                self.generate(eng + ', ' + hw['firstname'], chs.text, class_)
            elif hw.find('biography'):
                class_ = 'Names'
                self.generate(eng, chs.text, class_)
            elif hw.next_sibling and hw.next_sibling.name == 'lbtm':  # Brands
                class_ = 'Brands'
                self.generate(eng, chs.text, class_)
            elif entry.find('ulsubjfld') and entry.find('ulsubjfld')['value'][:12] == 'Geographical':
                class_ = 'Places'
                self.generate(eng, chs.text, class_)
            elif entry.find('expan'):
                class_ = 'Phrases-hw'
                self.generate(eng + ' = ' + entry.find('expan').text, chs.text, class_)
            elif ' ' in eng or ',' in eng or '-' in eng[1:-1]:
                class_ = 'Phrases-hw'
                senses = entry.find_all('sensecat')
                if senses[0].find('tran'):
                    self.generate(eng, senses[0].find('tran').text, class_)
                del senses[0]
                for sense in senses:
                    if sense.find('tran'):
                        self.generate('', sense.find('tran').text, class_)
            else:
                examples = entry.find_all('exmplgrp')
                for example in examples:
                    eng = example.find('exmpl').text.strip()
                    pre_chs = example.find('tran')
                    if pre_chs:
                        chs = pre_chs.text.strip()
                        if chs[-1] in '。？”！':
                            class_ = 'Sentences'
                        else:
                            class_ = 'Phrases-ex'
                        # print(chs)
                        self.generate(eng, chs, class_)

    def generate(self, eng, chs, class_, expl_eng, expl_chs):
        # string = format('"%s","%s",\n' % (del_space(eng), del_space(chs)))
        class_split = class_.split(':')
        if len(class_split) > 2: class3 = class_split[2]
        else: class3 = ''
        if eng:
            string = format('"%s","%s","%s","%s","%s","%s","%s",\n' % (del_space(class_split[0]), del_space(class_split[1]), class3, del_space(eng), del_space(chs), del_space(expl_eng), del_space(expl_chs)))
        else:
            string = format(',,,,,"%s","%s",\n' % (del_space(expl_eng), del_space(expl_chs)))
        if not class_ in self.data:
            self.data[class_] = ''
        self.data[class_] += string

    def write(self):
        content = ['Sentences', 'Phrases-ex', 'Phrases-hw', 'Names', 'Places', 'Brands']
        # for file_name in content:
        for file_name in self.data:
            fo = open("Docu/Dict/Tag/" + file_name + ".csv", "a+")
            fo.write(self.data[file_name])
            fo.close()
        self.fo.close()

    def advanced_write(self):
        for file_name in self.data:
            file_name_ = file_name.split(':')[0]
            fo = open("Docu/Dict/Tag/" + file_name_ + ".csv", "a+")
            fo.write(self.data[file_name])
            fo.close()
        self.fo.close()


if __name__ == '__main__':
    for i in range(1, 11):
        cur = Dict(i)
        # cur.classify()
        cur.find_label()
        cur.advanced_write()


'''
file_name: batch_xx_LARGEENGLISHCHINESE2.xml

例句-Sentences exmplgrp(exmpl, tran) exmpl以。？”！结尾
例词-Phrases-ex exmplgrp(exmpl, tran) phrgrp(phr, tran) 
例词2-Phrases-hw entry(hw, sensecat(tran)) hw中有space或,或- sensecat有多个, 取第一个tran
人名-Names hw[firstname]
地名-Places ulsubjfld[Geographical_entry.....]
商标名-Brands lbtm的上一条hw
重定向 groupintro
'''
