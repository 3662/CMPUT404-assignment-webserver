#  coding: utf-8 
import socketserver
from urllib import request

import os

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


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        redirected = False
        redirected_url = ""
        # self.data = self.request.recv(1024).strip()
        self.data = self.request.recv(1024).decode('utf-8')
        req = self.data.split(' ')
        print("method:", req[0])
        print("file:", req[1])

        method = req[0]
        file_requested = req[1]

        if method == "GET":
            if not file_requested.endswith(".html") and not \
            file_requested.endswith(".css") and not file_requested.endswith("/"):
                for root, dirs, files in os.walk("www"):
                    print(dirs)
                    if file_requested[1:] in dirs:
                        file_requested += "/"
                        redirected = True 
                        redirected_url = file_requested
                        break

            if file_requested[-1] == "/":
                file_requested += "index.html"

            try:
                # print("DIRECTORY:", os.getcwd())
                # all_files = set()

                # for root, dirs, files in os.walk("www"):
                #     print(root)
                #     print(dirs)
                #     print(files)
                #     # for f in files:
                #     #     all_files.add("/" + f)
                print(file_requested)
                print("--------------")
                # print(all_files)

                # if file_requested not in all_files:
                #     print("FILE NOT FOUND")
                #     raise request.HTTPError("http://127.0.0.1:8080/", 404, "", 1, 4)
                    
                # file_name = "D:\\" + os.getcwd() + "www" + file_requested
                file_name = "www" + file_requested

                print(file_name)
                file = open(file_name, "rb")
                response = file.read()
                file.close()

                print(response)

                if file_name.endswith(".css"):
                    mimetype = "text/css"
                else:
                    mimetype = "text/html"

                if redirected:
                    header = "HTTP/1.1 301 REDIRECTED\n"
                    header += 'Location: '+ redirected_url +'\n\n'
                else:
                    header = "HTTP/1.1 200 OK\n"
                    header += 'Content-Type: '+str(mimetype)+'\n\n'

                # if redirected:
                #     header += 'Location: '+ str("http://www.google.com/") +'\n\n'

            except Exception as e:
                print("EXCEPT")
                header = "HTTP/1.1 404 Not Found\n\n"
                response = "HTTP/1.1 404 Not Found".encode('utf-8')

            final_response = header.encode("utf-8")
            final_response += response

            # print ("Got a request of: %s\n" % self.data)
            # self.request.sendall(bytearray("OK la concha",'utf-8'))

        else:
            header = "HTTP/1.1 405 Method Not Allowed\n\n"
            final_response = header.encode("utf-8")

        print(final_response)
        self.request.sendall(final_response)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
