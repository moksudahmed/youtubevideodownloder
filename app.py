from flask import Flask, request, Response
import youtube_dl
from flask import Flask, request, send_file
import os


app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Welcome to youtube download api!'

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    filename = ydl.prepare_filename(ydl.extract_info(url))
    return send_file(filename, as_attachment=True, attachment_filename='{}.mp4'.format(ydl.extract_info(url)["title"]))

if __name__ == '__main__':
    app.run(debug=True)
