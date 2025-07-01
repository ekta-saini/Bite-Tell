from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
from urllib.parse import parse_qs
from datetime import datetime
import uuid
import base64
import re

class BlogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('templates/index.html', 'r') as f:
                content = f.read()
                
            # Read posts
            posts = []
            if os.path.exists('posts'):
                for filename in os.listdir('posts'):
                    if filename.endswith('.json'):
                        post_id = filename[:-5]  # Remove .json extension
                        with open(f'posts/{filename}', 'r') as f:
                            post = json.load(f)
                            post['id'] = post_id
                            posts.append(post)
            
            # Sort posts by date (newest first)
            posts.sort(key=lambda x: x['date'], reverse=True)
            
            # Insert posts into HTML
            posts_html = ''
            for post in posts:
                image_html = ''
                if 'image' in post and post['image']:
                    image_html = f'<img src="data:image/jpeg;base64,{post["image"]}" alt="" class="post-image">'
                
                posts_html += f'''
                <article class="post">
                    <div class="post-header">
                        <h2>{post['title']}</h2>
                        <button onclick="deletePost('{post['id']}')" class="delete-btn" title="Delete this post">×</button>
                    </div>
                    <div class="date">{post['date']}</div>
                    {image_html}
                    <div class="content">{post['content']}</div>
                </article>
                '''
            
            content = content.replace('{{posts}}', posts_html)
            self.wfile.write(content.encode())
            
        elif self.path == '/create':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('templates/create.html', 'r') as f:
                content = f.read()
            self.wfile.write(content.encode())
            
        elif self.path.startswith('/static/'):
            file_path = self.path[1:]
            if os.path.exists(file_path):
                self.send_response(200)
                if file_path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'File not found')

    def do_DELETE(self):
        delete_match = re.match(r'/delete/([^/]+)', self.path)
        if delete_match:
            post_id = delete_match.group(1)
            file_path = f'posts/{post_id}.json'
            
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True}).encode())
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': str(e)}).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Post not found'}).encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Invalid delete request'}).encode())

    def do_POST(self):
        if self.path == '/create':
            # Get the boundary from Content-Type header
            content_type = self.headers['Content-Type']
            boundary = content_type.split('=')[1].encode()
            
            # Read the form data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse multipart form data
            parts = post_data.split(boundary)
            form_data = {}
            
            for part in parts:
                if b'Content-Disposition' in part:
                    # Extract field name
                    field_name = part.split(b'name="')[1].split(b'"')[0].decode()
                    
                    if b'filename=' in part:
                        # This is a file upload
                        if b'image' in part:
                            # Find the start of image data
                            img_start = part.find(b'\r\n\r\n') + 4
                            img_data = part[img_start:-2]  # -2 to remove final \r\n
                            if img_data:
                                form_data['image'] = base64.b64encode(img_data).decode()
                    else:
                        # Regular form field
                        value_start = part.find(b'\r\n\r\n') + 4
                        value = part[value_start:-2].decode()  # -2 to remove final \r\n
                        form_data[field_name] = value
            
            post = {
                'title': form_data.get('title', ''),
                'content': form_data.get('content', ''),
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'image': form_data.get('image', '')
            }
            
            if not os.path.exists('posts'):
                os.makedirs('posts')
                
            filename = f"posts/{str(uuid.uuid4())}.json"
            with open(filename, 'w') as f:
                json.dump(post, f)
            
            # Redirect to home page
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()

def run(server_class=HTTPServer, handler_class=BlogHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run() 