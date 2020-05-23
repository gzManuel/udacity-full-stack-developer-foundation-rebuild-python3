from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Hello!</h1>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"

            self.wfile.write( output.encode('utf-8'))#We need to encode our message before send
            print(output)
        
        else:
            self.send_error(404,'File Not Found: '+self.path)
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # ctype, pdifct = cgi.parse_header(self.headers.keys['content-type'])
            # if ctype == "multipart/form-data":
            #     fields = cgi.parse_multipart(self.rfile,pdifct)
            #     messageContent = fields.get('message')
            output = ""
            output += "<html><body>sdfsdfsd"
            # output += " <h2> Okay, how about this: </h2>"
            # output += "<h1> {} </h1>".format(messageContent[0])
            # output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            
            output += "</body></html>"
            self.wfile.write(output.encode('utf-8'))
            print(output)
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port),WebServerHandler)
        print("Web Server running on port "+str(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print("Web server running on port")
        server.socket.close()

if __name__ == "__main__":
    main()