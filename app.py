from flask import Flask, request, Response
import youtube_dl

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Welcome to youtube download api!'

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return Response(ydl.prepare_filename(ydl.extract_info(url)),
                    mimetype="audio/mpeg",
                    headers={"Content-disposition": "attachment; filename={}.mp3".format(ydl.extract_info(url)["title"])})

if __name__ == '__main__':
     app.run(debug=True)
