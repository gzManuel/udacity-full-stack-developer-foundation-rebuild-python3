from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Restaurant, MenuItem, Address, Employee
import cgi, cgitb
import sys

cgitb.enable()
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
DBSession = sessionmaker(bind = engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        
        # if self.path.endswith("/hello"):
        #     self.send_response(200)
        #     self.send_header('Content-type','text/html')
        #     self.end_headers()

        #     output = ""
        #     output += "<html><body>"
        #     output += "<h1>Hello!</h1>"
        #     output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
        #     output += "</body></html>"

        #     self.wfile.write( output.encode('utf-8'))#We need to encode our message before send
        #     print(output)
        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            restaurants = session.query(Restaurant).all()
            
            out = "<a href='restaurants/new'>Make a New Restaurant Here</a><br><br>"
            for restaurant in restaurants:
                out += restaurant.name+'<br><a href="/restaurants/'+str(restaurant.id)+'/edit">Edit</a>'
                out +='<br><a href="/restaurants/'+str(restaurant.id)+'/delete">Delete</a><br><br><br>'
            self.wfile.write(out.encode('utf-8'))
        elif self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            out = '<h1>Make a new Restaurant</h1>'
            out += '<form method="POST" enctype="multipart/form-data" action="/restaurants/new"> <input name ="name" type ="text"> <input type="submit" value="Create"></form>'
            self.wfile.write(out.encode('utf-8'))
        elif self.path.endswith("/edit"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            path =  self.path.rsplit("/")
            id = int(path[2])

            restaurant = session.query(Restaurant).filter_by(id = id).one()
            out = ''
            out += restaurant.name
            out += '<form method ="POST" enctype = "multipart/form-data" action="'+str(restaurant.id)+'/edit"> <input name ="name" type ="text" placeholder="'+restaurant.name+'"><input type="submit" value="Rename"></form>'

            self.wfile.write(out.encode('utf-8'))
        elif self.path.endswith('/delete'):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            path =  self.path.rsplit("/")
            id = int(path[2])
            print(path)
            restaurant = session.query(Restaurant).filter_by(id=id).one()
            out = '<h1>Are you sure you want to delete restaurant '+restaurant.name+'?</h1>'
            out += '<form method = "POST" enctype = "multipart/form-data" action="'+str(restaurant.id)+'/delete"><input type="submit" value="Delete"></form>'
            self.wfile.write(out.encode('utf-8'))
        else:
        
            self.send_error(404,'File Not Found: '+self.path)
    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                content_len =int(self.headers.get('Content-length'))
                pdict['CONTENT-LENGTH'] = content_len
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                
                name = fields.get("name")[0]
                name = str(name)
                restaurant = Restaurant(name = name)
                session.add(restaurant)
                session.commit()
            if self.path.endswith('/edit'):
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                content_len =int(self.headers.get('Content-length'))
                pdict['CONTENT-LENGTH'] = content_len
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)

                name = fields.get("name")[0]
                if name !="":
                    path =  self.path.rsplit("/")
                    id = int(path[2])
                    restaurant = session.query(Restaurant).filter_by(id=id).one()
                    restaurant.name=name
                    session.add(restaurant)
                    session.commit()
            if self.path.endswith('/delete'):
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                path =  self.path.rsplit("/")
                id = int(path[2])
                print(id)
                restaurant = session.query(Restaurant).filter_by(id=id).one()
                session.delete(restaurant)
                session.commit()

            # if self.path.endswith('resta')

            # self.send_response(301)
            # self.send_header('content-type', 'text/html')
            # self.end_headers()

            # ctype, pdict = cgi.parse_header(self.headers['content-type'])
            # pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            # content_len =int(self.headers.get('Content-length'))
            # pdict['CONTENT-LENGTH'] = content_len
            # if ctype == 'multipart/form-data':
            #     fields = cgi.parse_multipart(self.rfile, pdict)

            # message = fields.get("message")[0]
            # message = str(message).lower()
            # if message == "no body loves you":
            #     message = "God's love's me"

            # output = ""
            # output += "<html><body>"
            # output += " <h2> Okay, how about this: </h2>"
            # output += "<h1> "+message+"</h2>"
            # output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            # output += "</body></html>"
            # self.wfile.write(output.encode('utf-8'))
            # print(output)
        except:
            self.send_error(404, "{}".format(sys.exc_info()[0]))
            print(sys.exc_info()    )
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