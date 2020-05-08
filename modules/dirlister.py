import os

#**argで可変長引数をとれる。
def run(**args):
    print('[*] In dirlister module.')
    files = os.listdir('.')

    return str(files)
