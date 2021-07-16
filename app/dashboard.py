from bson.objectid import ObjectId
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for)
from werkzeug.exceptions import abort

from app.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    video_count = db.videos.count_documents({})
    image_count = db.images.count_documents({})
    summary = {'video_count': "{:,}".format(video_count),
               'image_count': "{:,}".format(image_count)}
    videos = [v for v in db.videos.find().sort("index_time", -1).limit(5)]
    images = [i for i in db.images.find().sort("index_time", -1).limit(5)]
    return render_template('index.html', summary=summary, videos=videos, images=images)


@bp.route('/<name>/')
def show_collection(name):
    db = get_db()
    collection = db.get_collection(name)
    samples = [s for s in collection.find({}).limit(50)]
    return render_template('list.html', name=name, samples=samples)

@bp.route('/<name>/<string:id>')
def preview(name, id):
    db = get_db()
    collection = db.get_collection(name)
    sample = collection.find_one({'_id': ObjectId(id)})
    return render_template('preview.html', id=id, name=name, sample=sample)
