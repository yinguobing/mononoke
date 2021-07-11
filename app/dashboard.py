from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort

from app.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    video_count = db.videos.count_documents({})
    image_count = db.images.count_documents({})
    summary = {'video_count': video_count,
               'image_count': image_count}
    return render_template('index.html', summary=summary)
