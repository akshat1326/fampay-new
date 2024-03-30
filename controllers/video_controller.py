from flask import Flask, request
from flask_cors import CORS
import logging
import sys
from services.service import VideoInfoService, DatabaseException, SearchException
from flask import jsonify

app = Flask(__name__)
# Configure handler for stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)  # Set the logging level
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)

# Configure the Flask app's logger
app.logger.addHandler(stdout_handler)
app.logger.setLevel(logging.INFO)
cors = CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8080"])

service = VideoInfoService()


@app.route('/videos', methods=['GET'])
def fetch_videos():
    # Default values for pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    try:
        paginated_return = service.fetch_paginated_videos_from_db(page, per_page)
    except DatabaseException as e:
        return jsonify({"error": "Internal Server Error, "}), 500
    return paginated_return.dict(), 200


@app.route('/search', methods=['GET'])
def search_videos():
    # Get search query from URL parameter
    search_query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    try:
        search_return = service.search_video_by_title(search_query, page, per_page)
    except SearchException as e:
        app.logger.info('INFO message: The home page was accessed.', e.message)
        return jsonify({"error": "Internal Server Error, "}), 500
    return search_return.dict(), 200

