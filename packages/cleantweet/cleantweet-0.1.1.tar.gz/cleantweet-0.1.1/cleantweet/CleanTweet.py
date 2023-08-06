import re
from nltk.tokenize import word_tokenize


class CleanTweet:
    def __init__(self, text):
        self.text = text

    def clean(self):
        with open(self.text, "r", encoding='utf8', errors='ignore') as read_object:
            lines = read_object.read()
            # remove special characters and punctuations
            # lines = re.sub('[\n]', '', lines)
            lines = re.sub('#', '', lines)
            lines = re.sub('\\n\\n', '', lines)
            lines = re.sub('[\\n\\n]', '', lines)
            lines = re.sub('(\n\n)', '', lines)
            lines = re.sub('[{}:_@\[\]0-9,%&*""?!/-]', '', lines)
            # remove the id and text tag
            lines = re.sub('(id)', '', lines)
            lines = re.sub('(text)', '', lines)
            lines = re.sub('(RT)', '', lines)
            # remove paragraph space/indentation
            lines = re.sub('  ', '', lines)
            lines = word_tokenize(lines)
            lines = [line for line in lines if line.isalpha()]
            lines = ' '.join(lines)
        return lines
