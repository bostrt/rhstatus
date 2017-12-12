#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import click
import sys
from terminaltables import AsciiTable
from colored import stylize, fg

def applystyle(status, style):
    color = style.split('-')[1]
    return stylize(status, fg(color))

def go():
    result = requests.get('https://status.redhat.com')
    table = [['Name', 'Status']]
    if result.status_code != 200:
        print(stylize('It broke :(', fg('red')))
        sys.exit(1)
    else:
        soup = BeautifulSoup(result.content, 'html.parser')
        components = soup.find_all('div', {'class': 'component-inner-container'})
        for comp in components:
            style = comp.get('class')[1]
            keyval = comp.find_all('span')
            name = keyval[0].get_text().strip()
            status = keyval[1].get_text().strip()
            # hack out the embedded "Insights" section header.
            if status is not None and status is not '':
                table.append([name, applystyle(status, style)])
        output = AsciiTable(table)
        print(output.table)
    
if __name__=='__main__':
    go()
