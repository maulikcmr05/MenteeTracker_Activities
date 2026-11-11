from transformers import pipeline
from http.server import BaseHTTPRequestHandler,HTTPServer
import json,os
model=pipeline("text-classification",model=os.getenv("MODEL_NAME","distilbert-base-uncased-finetuned-sst-2-english"))
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b'{"status":"ok"}')
    def do_POST(self):
        n=int(self.headers.get("Content-Length",0)); x=json.loads(self.rfile.read(n)); b=json.dumps(model(x["text"][:2000])).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(b)
HTTPServer(("0.0.0.0",8080),H).serve_forever()
