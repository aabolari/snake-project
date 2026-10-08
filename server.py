# server.py - the "glue" between the browser and your snake.py functions.
# Your game rules stay in snake.py. This file only passes messages back and forth.
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from snake import create_new_game, step_game, change_direction, toggle_pause

PORT = 8000
VALID_DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

# The one and only game, kept in memory while the server runs.
game = create_new_game()


class SnakeHandler(BaseHTTPRequestHandler):

    def send_json(self, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/state":
            self.send_json(game)
        elif self.path == "/" or self.path == "/index.html":
            try:
                with open("index.html", "rb") as f:
                    page = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(page)))
                self.end_headers()
                self.wfile.write(page)
            except FileNotFoundError:
                self.send_error(404, "index.html not found next to server.py")
        else:
            self.send_error(404)

    def do_POST(self):
        global game

        if self.path == "/tick":
            step_game(game)
        elif self.path == "/direction":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or b"{}")
            direction = data.get("direction")
            if direction in VALID_DIRECTIONS:
                change_direction(game, direction)
        elif self.path == "/pause":
            toggle_pause(game)
        elif self.path == "/reset":
            game = create_new_game(game["high_score"])
        else:
            self.send_error(404)
            return

        self.send_json(game)

    def log_message(self, format, *args):
        pass  # keeps the terminal quiet


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), SnakeHandler)
    print(f"Snake running at http://localhost:{PORT}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")