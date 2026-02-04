def run_gui():
    """Minimal web GUI for selecting ROM / boot / payload"""
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    import webbrowser
    import threading

    def open_browser():
        webbrowser.open("http://localhost:8080")

    server = HTTPServer(("localhost", 8080), SimpleHTTPRequestHandler)
    threading.Thread(target=open_browser).start()
    print("GUI running on http://localhost:8080")
    server.serve_forever()
