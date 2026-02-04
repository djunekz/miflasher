def run_gui():
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    import threading, webbrowser

    def open_browser():
        webbrowser.open("http://localhost:8080")

    server = HTTPServer(("localhost", 8080), SimpleHTTPRequestHandler)
    threading.Thread(target=open_browser).start()
    print("GUI running at http://localhost:8080")
    server.serve_forever()
