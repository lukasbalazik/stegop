# stegop

stegop is python tool for creating steganographic patterns in data so we can hide our message. stegop is more of the obfuscation then steganography itself, becouse we are not editing file we only create pattern which define our data.

## Instalation

```bash
git clone https://github.com/lukasbalazik123/stegop.git
cd stegop
pip3 install -r requirements.txt
```

## How it works?
Flow is simple, first you have to define path to file or link which will serve as our pattern making, then you define data you want to encode.

At very first step, the charset is created, its just range of ascii characters which will purpose as table of used characters from file. Then stegop create map which is created from charset and position of character in the file, this map is then used for replacing hexadecimal format of data to positions of charset characters, this is how our pattern is made. Then we gzip our pattern so it will take less space and encoded it in base64.

## Usage

```bash
$ ./stegop.py -h
usage: stegop.py [-h] [--minchar MINCHAR] [--maxchar MAXCHAR] [-g] [-e] [-d] -f PATH -i INPUT

optional arguments:
  -h, --help            			  show this help message and exit
  --minchar MINCHAR      Lower limit for charset default 97
  --maxchar MAXCHAR     Upper limit for charset defualt 123
  -g, --generate				  Generate js injector
  -e, --encode						Encode Data
  -d, --decode						Decode Data
  -f PATH, --file PATH			Path to file or link
  -i INPUT, --input INPUT	Input Data

```

## Example

For example if we want to upload some sort of javascript and we dont want to show our code to everyone we can generate javascript injector and use pattern decoder for evaluating our javascript code:

```bash
$ ./stegop.py -f http://localhost -i "alert('Hello world')" -g -e

Encoded data:
eJxFjMkNADAIwxbKh0Bh/82q0IOPBciYBXOwECky4QsWIqOHnNWf8/3D7BejNJl9OZ0px+2ItQFfjBbt

Javascript payload:
function loadXMLDoc(t){(xmlhttp=window.XMLHttpRequest?new XMLHttpRequest:new ActiveXObject("Microsoft.XMLHTTP")).open("GET",t,!1),xmlhttp.send()}var base_chars=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'],charset=[97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123],file="http://localhost",b="eJxFjMkNADAIwxbKh0Bh/82q0IOPBciYBXOwECky4QsWIqOHnNWf8/3D7BejNJl9OZ0px+2ItQFfjBbt",decodedStr=atob(b),unziped=pako.ungzip(decodedStr,{to:"string"}),pattern=unziped.split(","),xmlhttp=!1;if(loadXMLDoc(file),1!=xmlhttp){var i=1,map={},filedata=xmlhttp.responseText,filedata=filedata.replace(/[^\x00-\x7F]/g,"");base_chars.forEach(t=>{for(;i<filedata.length;i++){var a=filedata.charAt(i).charCodeAt(0);if(!(charset.indexOf(a)<0)){map[t]=i,charset.splice(charset.indexOf(a),1);break}}i++});var data_hex="";pattern.forEach(a=>{Object.keys(map).forEach(function(t){map[t]==a&&(data_hex+=t)})});for(var data="",n=0;n<data_hex.length;n+=2)data+=String.fromCharCode(parseInt(data_hex.substr(n,2),16));eval(data)}
```

Then we copy our javascript payload and use:

```bash
<html>
<head>
</head>
<body>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pako/1.0.11/pako.min.js"></script>
    <script type="text/javascript">
function loadXMLDoc(t){(xmlhttp=window.XMLHttpRequest?new XMLHttpRequest:new ActiveXObject("Microsoft.XMLHTTP")).open("GET",t,!1),xmlhttp.send()}var base_chars=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'],charset=[97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123],file="http://localhost",b="eJxFjMkNADAIwxbKh0Bh/82q0IOPBciYBXOwECky4QsWIqOHnNWf8/3D7BejNJl9OZ0px+2ItQFfjBbt",decodedStr=atob(b),unziped=pako.ungzip(decodedStr,{to:"string"}),pattern=unziped.split(","),xmlhttp=!1;if(loadXMLDoc(file),1!=xmlhttp){var i=1,map={},filedata=xmlhttp.responseText,filedata=filedata.replace(/[^\x00-\x7F]/g,"");base_chars.forEach(t=>{for(;i<filedata.length;i++){var a=filedata.charAt(i).charCodeAt(0);if(!(charset.indexOf(a)<0)){map[t]=i,charset.splice(charset.indexOf(a),1);break}}i++});var data_hex="";pattern.forEach(a=>{Object.keys(map).forEach(function(t){map[t]==a&&(data_hex+=t)})});for(var data="",n=0;n<data_hex.length;n+=2)data+=String.fromCharCode(parseInt(data_hex.substr(n,2),16));eval(data)}
    </script>
</body>
</html>
```
When we enter the site the code will be decoded and executed.

For decompression we are using pako.js so we need to import that.

Be carefull when encoding data, when you plan to deploy it as javascript you have to check allow-origin header (if its not allowed for everything, use url only from that domain for example index file)