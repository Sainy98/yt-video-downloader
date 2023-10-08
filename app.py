from flask import Flask, render_template, request, send_file, session, url_for, redirect
from pytube import YouTube
from io import BytesIO

app = Flask(__name__, template_folder="Template")
app.config['SECRET_KEY'] = "sainy"


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == 'POST':
        session['url'] = request.form.get('url')
        yt = YouTube(session['url'])
        print(yt)

        if 'videoDetails' in yt.vid_info:
            TITLE = yt.vid_info['videoDetails']['title']
            image = yt.thumbnail_url
            session["title"] = TITLE
            return render_template('download.html', TITLE=TITLE, image=image, yt=yt)
        else:
            TITLE = "Title not found"
            image = ""
            return render_template("download.html", TITLE=TITLE, image=image, yt=yt)
    return redirect(url_for("home"))


@app.route("/downloaded", methods=["GET", "POST"])
def downloaded():
    buffer = BytesIO()
    yt = YouTube(session['url'])
    itag = request.form.get("itag")
    video = yt.streams.get_by_itag(itag)
    video.stream_to_buffer(buffer)
    buffer.seek(0)
    TITLE = session.get('title', 'title Not Found')

    return send_file(buffer, as_attachment=True, download_name=f"{TITLE} video.mp4", mimetype="video/mp4")


app.run(debug=True)
