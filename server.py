#  coding: utf-8 
import socketserver

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
        # self.data = self.request.recv(1024).strip()
        self.data = self.request.recv(1024).decode('utf-8')
        req = self.data.split(' ')
        print("method:", req[0])
        print("file:", req[1])

        method = req[0]
        file_requested = req[1]

        if method == "GET":
            if file_requested == "/":
                file_requested = "/index.html"

            # print(req[1].lstrip("/"))
            # raise Exception

            # file = open(req[1].lstrip("/"), "rb")

            try:
                file_name = "www" + file_requested
                file = open(file_name, "rb")
                response = file.read()
                file.close()

                header = "HTTP/1.1 200 OK\n"

                if file_name.endswith(".css"):
                    mimetype = "text/css"
                else:
                    mimetype = "text/html"

                header += 'Content-Type: '+str(mimetype)+'\n\n'
            except Exception as e:
                header = "HTTP/1.1 404 Not Found\n\n"
                response = 'HTTP/1.1 404 Not Found'.encode('utf-8')

            final_response = header.encode("utf-8")
            # print(type(final_response))
            # print(type(response))
            # raise Exception
            final_response += response

            # print(header)
            # print(response)
            # raise Exception

            print(final_response)

            # final_response = final_response.encode("utf-8")

            self.request.sendall(final_response)

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
