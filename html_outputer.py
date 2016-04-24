#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self, content):
        with open('output.html', 'w') as fout:
            fout.write('<html>')
            fout.write('<body>')
            for data in self.datas:
                fout.write('<tr>')
                fout.write('<td>%s</td>'.format(data))
                fout.write('</tr>')
            fout.write('</body>')

            fout.write('</html>')
