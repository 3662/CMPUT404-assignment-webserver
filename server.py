#  coding: utf-8 
import socketserver
from urllib import request

import os

# Copyright 2022 Abram Hindle, Eddie Antonio Santos, Felipe Rodriguez Atuesta
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
        self.data = self.request.recv(1024).decode('utf-8')
        data_request = self.data.split(' ')

        method = data_request[0]
        file_requested = data_request[1]

        if method == "GET":
            final_response = self.handle_get(file_requested)
        else:
            header = "HTTP/1.1 405 Method Not Allowed\n\n"
            final_response = header.encode("utf-8")

        # print(final_response)

        self.request.sendall(final_response)

    """
    handles get requests and return an encoded final response to be sent back 
    to the client
    """
    def handle_get(self, file_requested):
        redirected = False
        redirected_url = ""

        file_name = "www" + file_requested

        # print(file_name)

        valid_paths = set()
        valid_paths.add("www")
        valid_paths.add("www/")

        for root, dirs, files in os.walk("www"):
            for d in dirs:
                valid_paths.add("{}/{}/".format(root, d))
                valid_paths.add("{}/{}".format(root, d))
            for f in files:
                valid_paths.add("{}/{}".format(root, f))

        if file_name not in valid_paths:
            # print(file_name)
            # print(valid_paths)

            header = "HTTP/1.1 404 Not Found\n\n"
            response = "HTTP/1.1 404 Not Found".encode('utf-8')
        else:
            # correct directory paths not ending with /
            if not file_requested.endswith(".html") and not \
                file_requested.endswith(".css") and not file_requested.endswith("/"):
                    for root, dirs, files in os.walk("www"):
                        if file_requested[1:] in dirs:
                            file_name += "/"
                            redirected = True 
                            redirected_url = file_requested
                            break

            # return index.html for directories (paths ending with /)
            if file_name[-1] == "/":
                file_name += "index.html"

            # read the requested file
            try:
                file = open(file_name, "rb")
                response = file.read()
                file.close()

                # currently supporting mime-types HTML and CSS
                if file_name.endswith(".css"):
                    mimetype = "text/css"
                elif file_name.endswith(".html"):
                    mimetype = "text/html"
                else:
                    mimetype = ""

                # returns a status code of 301 if path redirected
                if redirected:
                    header = "HTTP/1.1 301 Redirected\n"
                    header += "Location: " + redirected_url + "\n\n"
                else:
                    header = "HTTP/1.1 200 OK\n"
                    header += "Content-Type: " + mimetype + "\n\n"

            except Exception as e:
                # if failed to read the requested file
                header = "HTTP/1.1 404 Not Found\n\n"
                response = "HTTP/1.1 404 Not Found".encode('utf-8')

        final_response = header.encode("utf-8") + response 

        return final_response

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
