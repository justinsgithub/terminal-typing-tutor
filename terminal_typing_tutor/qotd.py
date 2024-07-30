from pathlib import Path
from blessed import Terminal
import wikiquote
import yaml
import os
import unicodedata

# ord('\u2014') = 8212
# ord('\u2019') = 8217
# ord('\u2026') = 8230

term=Terminal()
WIDTH=term.width-10

qotd_file = Path(__file__).parent.joinpath("series/D/1/data.yaml")
rand_file = Path(__file__).parent.joinpath("series/D/2/data.yaml")
edison_file = Path(__file__).parent.joinpath("series/D/3/data.yaml")

template = {'total_segments':0,
             'segments': {
                 0: {
                     'type':'info',
                     'intro':None,
                     'content':None
                 }
             }}

def export_yaml(template, data, segs, intro, content, fp):
    template['total_segments'] = segs
    template['segments'][0]['intro'] = intro
    template['segments'][0]['content'] = content

    for i in range(1,segs):
        template['segments'][i] = {}
        template['segments'][i]['type'] = 'drill'
        template['segments'][i]['intro'] = intro
        # cleanse text data from wikiquote
        # examples, inlcude ellipses, hyphens, and other 
        data[i-1] = ''.join([x if ord(x) != 8217 else '\'' for x in data[i-1]])
        data[i-1] = ''.join([x if ord(x) != 8212 else '-' for x in data[i-1]])
        data[i-1] = ''.join([x if ord(x) != 8230 else '...' for x in data[i-1]])
        data[i-1] = ''.join([x if ord(x) < 128 else '***' for x in data[i-1]])
        template['segments'][i]['content'] = data[i-1]

    # yaml not very reliable/versatile, so also need to 'cleanse' yaml output
    yaml_data = yaml.dump(template, sort_keys=False, width=WIDTH)
    yaml_data = yaml_data.replace("content:","content: |\n     ")
    
    # write to file
    with open(fp, "w") as f:
        f.write(yaml_data)

def qotd():
    quote = wikiquote.qotd()
    data = [quote[0] + ' --' + quote[1]]
    intro="Today's Quote of the Day from Wikiquote"
    content="The quote of the day changes every day. Check back tomorrow for a different quote! It's possible that non-ascii characters were fetched from wikiquote, in which case they were either substituted with the closest ascii equivalent or replaced with '***'. Also, some quotes may be excessively long and may not display properly. Feel free to skip them, for now."
    export_yaml(template, data, 2, intro, content, qotd_file)

def rand_quote():
    titles = wikiquote.random_titles(max_titles=1)
    quotes = wikiquote.quotes(titles[0])
    title = titles[0]
    content = "A selection of quotes from a randomly selected topic (above). It's possible that non-ascii characters were fetched from wikiquote, in which case they were either substituted with the closest ascii equivalent or replaced with '***'. Also, some quotes may be excessively long and may not display properly. Feel free to skip them, for now."
    export_yaml(template, quotes, len(quotes)+1, title, content, rand_file)

def edison():
    quotes = wikiquote.quotes('Thomas Edison', max_quotes=30)
    title = "Quotes from Thomas A. Edison"
    content = "A slection of quotes from Thomas Edison"
    export_yaml(template, quotes, len(quotes)+1, title, content, edison_file)

# for testing
if __name__ == '__main__':
    qotd()
    rand_quote()
    edison()