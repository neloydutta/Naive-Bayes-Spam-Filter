import os
import json
import email
from nltk.tokenize import word_tokenize
import filter as sfilter

traindata = {}


def create():
    cwd = os.getcwd()
    print cwd
    idx = 0
    with open('SPAMTrain.label', 'r') as label:
        lwords = word_tokenize(label.read(), language='english')
        folderlocation = os.path.join(cwd, 'TRAINING')
        if not os.path.isfile(folderlocation):
            for i in os.listdir(folderlocation):
                filename = os.path.join(folderlocation, i)
                f = open(filename, 'r')
                a = email.message_from_file(f)
                f.close()
                message = "empty"
                if not a.is_multipart() and a.get_content_type() == 'text/plain':
                    continue
                    message = a.get_payload()
                    try:
                        message.encode('utf8')
                    except Exception:
                        continue
                else:
                    message = ""
                    for i in a.walk():
                        if i.get_content_type() == 'text/plain':
                            message += i.get_payload() + " "
                            try:
                                message.encode('utf8')
                            except Exception:
                                continue
                if lwords[idx] == '1' and message != 'empty':
                    sfilter.train(message, 'not_spam')
                else:
                    sfilter.train(message, 'spam')
                idx += 2


if __name__ == "__main__":
    create()
