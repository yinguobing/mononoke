import os

from bson.objectid import ObjectId
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   url_for, send_from_directory, safe_join)
from werkzeug.exceptions import abort

from app.db import get_db

bp = Blueprint('dashboard', __name__,
               static_folder='/Users/Robin/data/warehouse/originals')


def sizeof_file(num, suffix='B'):
    """Convert the file size into human readable format.

    Author: http://blogmag.net/blog/read/38/Print_human_readable_file_size
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def format_record(collection_name, record):
    """Format the record to make it suitable for html output.

    This function will:
        1. convert the array items in the record into a comma seperated string.
        2. convert the index time into Year-Month-Day string.
        3. convert the raw file size into human readable string.
        3. add a preview_link item that contains the hyperlink for previewing.
    """
    record.update({'manual_tags': ', '.join((record['manual_tags']))})
    record.update({'authors': ', '.join((record['authors']))})
    record.update({'index_time': record['index_time'].strftime("%Y-%m-%d")})
    record.update({'file_size': sizeof_file(record['file_size'])})
    record.update({'href': url_for('dashboard.preview', name=collection_name,
                                   id=record['_id'])})


def format_records(collection_name, records):
    for s in records:
        format_record(collection_name, s)


def generate_static_link(record):
    """Generate a href link for the static file."""
    file_path = record['path'].split(os.path.sep)[-2:]
    file_path = "{}/{}".format(file_path[0], file_path[1])
    
    return url_for('dashboard.static', filename=file_path)

@bp.route('/')
def index():
    db = get_db()
    video_count = db.videos.count_documents({})
    image_count = db.images.count_documents({})
    summary = {'video_count': "{:,}".format(video_count),
               'image_count': "{:,}".format(image_count)}

    videos = [v for v in db.videos.find().sort("index_time", -1).limit(5)]
    for v in videos:
        v.update({'href': generate_static_link(v)})
    format_records('videos', videos)

    images = [i for i in db.images.find().sort("index_time", -1).limit(5)]
    for i in images:
        i.update({'href': generate_static_link(i)})
    format_records('images', images)

    return render_template('index.html', summary=summary, videos=videos, images=images)


@bp.route('/<name>/')
def show_collection(name):
    db = get_db()
    collection = db.get_collection(name)
    samples = [s for s in collection.find({}).limit(50)]
    format_records(name, samples)
    return render_template('list.html', name=name, samples=samples)


@bp.route('/<name>/<string:id>')
def preview(name, id):
    db = get_db()
    collection = db.get_collection(name)
    sample = collection.find_one({'_id': ObjectId(id)})
    download_link = generate_static_link(sample)
    format_record(name, sample)
    return render_template('preview.html', name=name, sample=sample, download_link=download_link)


@bp.route('/originals/<path:filename>')
def originals(filename):
    return send_from_directory(bp.static_folder, filename)
