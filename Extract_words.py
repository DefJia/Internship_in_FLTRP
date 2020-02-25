from bs4 import BeautifulSoup


if __name__ == '__main__':
    file = '.data/ldoce6_book_picrefs_cn.xml'
    fo = open(file, 'r+', encoding="utf8")
    context = fo.read()
    soup = BeautifulSoup(context, "html5lib")
    entries = soup.find_all('entry')
    middle = list()
    final = list()
    for entry in entries:
        if 'type' in entry.attrs and entry['type'] == 'encyc':
            proncodes = entry.find_all('proncodes')
            hwd = entry.find('hwd')
            if len(proncodes) > 0:
                middle.append(hwd)
            else:
                final.append(hwd)
    res = ''
    for elem in final:
        res += elem.text + ',\n'
    fo = open(".data/result.csv", "a+")
    fo.write(res)
    fo.close()
