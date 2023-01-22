from flask import Flask, request, Response
import youtube_dl
import qrcode
from io import BytesIO
from flask import Flask, request, send_file
import os
import PIL

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

@app.route("/qr")
def qr():
    url = request.args.get('url')
    img = qrcode.make(url)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return Response(img_io.getvalue(), mimetype='image/png', headers={'Content-Disposition':'attachment;filename=qrcode.png'})

if __name__ == '__main__':
    app.run(debug=True)
