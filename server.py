#  coding: utf-8 
import socketserver
from os import error, listdir, path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

def detectType(content_type, self):
    if content_type == "css":
        self.request.sendall(bytearray("Content-Type: text/css\r\n",'utf-8'))
    else:
        self.request.sendall(bytearray("Content-Type: text/html\r\n",'utf-8'))



def constructResponse(self):
    content_type = ""
    path, content_type= parseRequest(self,content_type)
    self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
    detectType(content_type, self)
    #to do detect which file to send
    self.request.sendall(bytearray("\r\n",'utf-8'))
    sendFile(self,path)

def parseRequest(self,content_type):
    path = ""
    content = ""
    request = self.data.decode("utf-8")
    split_request = request.split()
    file_path = split_request[1]
    split_path = file_path.split("/")

    if ((split_path[-1][-4:] == "html") or (split_path[-1][-4:] == ".css")):
        content = split_path.pop()
        if content[-4:] == "html":
            content_type = "html"
        elif content[-4:] == ".css":
            content_type = "css"

    print(file_path)
    print(split_path)

    for i in split_path:
        if i != "":
            path = path+ "/"+ i
            if path[0] == "/":
                path = path[1:]
                path = "www/" + path
            try:
                files_in_dir = listdir(path)
                print(files_in_dir)
            except error as e:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
        elif file_path =="/" or file_path =="/index.html" or file_path =="/base.css":
            path = "www"
            files_in_dir = listdir(path)
            break
    if content in files_in_dir:
        return path+"/"+content, content_type
    else: return path, content


def sendFile(self, file_to_send):
    if ((file_to_send[-4:] == "html") or (file_to_send[-4:] == ".css")):
        file_to_send = file_to_send
    else:
        file_to_send = file_to_send + "/index.html"
    f = open(file_to_send, "r")
    self.request.sendall(bytearray(f.read(),'utf-8'))

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        constructResponse(self)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
