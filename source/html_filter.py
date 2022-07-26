from typing import Tuple
from html.parser import HTMLParser


class HTMLFilter(HTMLParser):
    def __init__(self, tag_to_find: Tuple[str, str]) -> None:
        HTMLParser.__init__(self)
        self.recording = 0
        self.data = ''
        self.self_closing_tags = ("br",)
        self.tag_to_find = tag_to_find
        self.final_table = []


    def handle_starttag(self, tag, attributes) -> None:
        # Jeśli nagrywamy oraz TAG nie jest samozamykającym się to dodajmy go do wyniku
        if tag not in self.self_closing_tags and self.recording > 0:
            self.data += "<%s" % (tag,)
            if attributes:
                self.data += " " + " ".join('%s="%s"' % (k, v) for k, v in attributes)
            self.data += ">"
            if tag == self.tag_to_find[0]:
                self.recording += 1
            return

        # Jeśli TAG nie jest tym którego szukamy to wyjdź
        if tag != self.tag_to_find[0]:
            return
        
        if self.recording:
            self.recording += 1
            self.data += "<%s" % (tag,)
            if attributes:
                self.data += " " + " ".join('%s="%s"' % (k, v) for k, v in attributes)
            self.data += ">"

        # Jeśli TAG jest tym który szukamy, sprawdź atrybuty, jeśli pasuje to zacznij nagrywać
        for name, value in attributes:
            if self.tag_to_find[1] in value.split(' '):
                self.recording = 1
                return
                

    def handle_endtag(self, tag) -> None:
        if tag == self.tag_to_find[0] and self.recording:
            self.recording -= 1
            if self.recording != 0:
                self.data += "</%s>" % (tag,)
            elif self.recording == 0:
                # self.data += "</%s>" % (tag,) # zmiana 02.08.2022
                self.final_table.append(self.data)
                self.data = ''
            

        elif tag in self.self_closing_tags:
            self.data += "<%s/>" % (tag,)
        else:
            self.data += "</%s>" % (tag,)


    def handle_data(self, data) -> None:
        if self.recording:
            self.data += data


    def save_data(self):
        with open('output/output.html', 'w') as file:
            for item in self.final_table:
                file.write(item.strip().replace('\n', '').replace('\t', ''))
                file.write('\n')


    def get_data(self):
        return self.final_table