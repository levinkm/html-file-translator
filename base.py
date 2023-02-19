import os
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
from googletrans import Translator
import requests
import asyncio
translator = Translator()


class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v


files_from_folder = "./"

use_translate_folder = False

destination_language = 'hi'

extension_file = ".html"

elements = ['p', 'title', 'h1', 'h2', 'h3', 'h4', 'h5',
            'h6', 'span', 'a', 'strong', 'small', 'button',]

directory = os.fsencode(files_from_folder)


def recursively_translate(node):
    for x in range(len(node.contents)):
        if isinstance(node.contents[x], str):
            if node.contents[x].strip() != '':
                try:
                    node.contents[x].replaceWith(translator.translate(
                        node.contents[x], dest=destination_language).text)
                except:
                    pass
        elif node.contents[x] != None:
            recursively_translate(node.contents[x])


async def translate_file(filename):
    print(filename)
    if filename == 'y_key_e479323ce281e459.html' or filename == 'TS_4fg4_tr78.html':  # ignore this 2 files
        pass
    if filename.endswith(extension_file):
        soup = None
        with open(os.path.join(files_from_folder, filename), encoding='utf-8') as html:
            soup = BeautifulSoup('<pre>' + html.read() +
                                 '</pre>', 'html.parser')
            for title in soup.findAll(elements):
                recursively_translate(title)

            for meta in soup.findAll('meta', {'name': 'description'}):
                try:
                    meta['content'] = translator.translate(
                        meta['content'], dest=destination_language).text
                except:
                    pass

        print(f'{filename} translated')
        soup = soup.encode(formatter=UnsortedAttributes()).decode('utf-8')
        new_filename = f'{filename.split(".")[0]}.html'
        if use_translate_folder:
            try:
                with open(os.path.join(files_from_folder+r'\translated', new_filename), 'w', encoding='utf-8') as new_html:
                    new_html.write(soup[5:-6])
            except:
                os.mkdir(files_from_folder+r'\translated')
                with open(os.path.join(files_from_folder+r'\translated', new_filename), 'w', encoding='utf-8') as new_html:
                    new_html.write(soup[5:-6])
        else:
            with open(filename, 'w', encoding='utf-8') as html:
                html.write(soup[5:-6])
