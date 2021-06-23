#!/usr/bin/env python3
import codecs
import base64
import zlib
import os.path
import requests
import argparse

class StegoP:
    def __init__(self):
        self.dictionary = {
                "0": [ 97, 98 ],
                "1": [ 99, 100 ],
                "2": [ 101, 102 ],
                "3": [ 103, 104 ],
                "4": [ 105, 106 ],
                "5": [ 107, 108 ],
                "6": [ 109, 110 ],
                "7": [ 111, 112 ],
                "8": [ 113, 114 ],
                "9": [ 115, 116 ],
                "a": [ 117, 118 ],
                "b": [ 119, 120 ],
                "c": [ 121, 122 ],
                "d": [ 65, 66 ],
                "e": [ 67, 68 ],
                "f": [ 69, 70 ]
        }
        self.map = {}

    def read(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.filedata = f.read()
        elif "http" in path:
            r = requests.get(path)
            self.filedata = r.text
        else:
            print("Website or file not found")

    def generate_map(self):
        for key in self.dictionary.keys():
            for v in self.dictionary[key]:
                pos = self.filedata.find(chr(v))
                if pos > 0:
                    self.map[key] = pos
                    break

    def encrypt(self, data):
        pass

    def encode(self, data):
        output = []
        data_hex = codecs.encode(bytes(data, 'ascii'), "hex").decode()
        for c in data_hex:
            output.append(str(self.map[c]))

        compress = zlib.compress(bytes(','.join(output), 'ascii'))
        b64_compress = base64.b64encode(compress)
        return b64_compress

    def decrypt(self, data):
        pass

    def decode(self, b64_compress):
        data_hex = ""
        compress = base64.b64decode(b64_compress)
        output = zlib.decompress(compress).decode()
        output = output.split(",")

        for c in output:
            data_hex += list(self.map.keys())[list(self.map.values()).index(int(c))]
        data = codecs.decode(data_hex, "hex").decode()
        return data

    def generate_injector(self, _type):
        pass


stegop = StegoP()
stegop.read("./test.html")
stegop.generate_map()

ret = stegop.encode("""testtest asdasds""")
print(ret)

ret = stegop.decode(ret)
print(ret)
