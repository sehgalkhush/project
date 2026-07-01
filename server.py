from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse

class MyServer(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/login.html")
            self.end_headers()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path != "/login":
            return

        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length).decode('utf-8')
        form = urllib.parse.parse_qs(data)

        username = form.get('username', [''])[0]
        password = form.get('password', [''])[0]

        users = {
            "raghvendra mishra": ("admin123", "/admin.html"),
            "manager": ("manager123", "/manager.html"),
            "khush": ("khush123", "/khush.html"),
        }

        if username in users and users[username][0] == password:
            redirect_to = users[username][1]
        else:
            redirect_to = "/login.html?error=1"

        self.send_response(302)
        self.send_header("Location", redirect_to)
        self.end_headers()


def run_server(port=5000):
    httpd = HTTPServer(('127.0.0.1', port), MyServer)
    print(f"Server running at http://127.0.0.1:{port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()