import os
import logging
from mysql.connector import Error
from flask import jsonify
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from models.exceptions import *
from sqlalchemy import create_engine
logger = logging.getLogger()
# DATABASE_URI = 'mysql+pymysql://root:rootpassword@mysql:3306/'
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_user = os.getenv("POSTGRES_PASSWORD")
postgres_db = os.getenv("POSTGRES_DB")

# DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@postgres:5432/YoutubeDB'
DATABASE_URI = f"postgresql://{os.getenv('DATABASE_USER', 'postgres')}:" \
               f"{os.getenv('DATABASE_PASSWORD', 'postgres')}@" \
               f"{os.getenv('DATABASE_HOST', 'db')}/" \
               f"{os.getenv('DATABASE_NAME', 'YoutubeDB')}"


class VideoInformationRepo:
    def __init__(self):
        self.engine = create_engine(DATABASE_URI)

        with self.engine.begin() as connection:
            if connection is None:
                raise ConnectionNotFoundException("Expected Connection, found None")
            try:
                # Query to fetch paginated videos sorted by PublishDateTime in descending order
                res = connection.execute(text("CREATE SCHEMA IF NOT EXISTS youtube"))
                print("yel o", res.mappings())
                query = text("""
                      CREATE TABLE IF NOT EXISTS youtube.videos(
                      ID SERIAL PRIMARY KEY,
                      VideoID VARCHAR(255) UNIQUE,
                      Title VARCHAR(255) NOT NULL,
                      Description TEXT,
                      PublishDateTime TIMESTAMP NOT NULL,
                      ThumbnailURL VARCHAR(255),
                      CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )"""
                             )
                connection.execute(query)

            except Exception as e:
                print("An error occurred:", e)
                raise e

    print("I WAS commited?")  # do select again)

    def get_paginated_videos_list_from_db(self, page, per_page) -> PaginatedReturn:
        offset = (page - 1) * per_page
        with self.engine.connect() as connection:
            if connection is None:
                raise ConnectionNotFoundException("Expected Connection, found None")

            try:
                # Query to fetch paginated videos sorted by PublishDateTime in descending order
                query = text(
                    "SELECT Title, Description, PublishDateTime, ThumbnailURL "
                    "FROM youtube.videos ORDER BY PublishDateTime DESC LIMIT :per_page OFFSET :offset"
                )
                result = connection.execute(query, {'per_page': per_page, 'offset': offset})

                # Convert result to a list of dicts
                videos_list = [dict(row) for row in result.mappings()]
                paginated_return = PaginatedReturn(video=videos_list, page=page, per_page=per_page)

                return paginated_return
            except Error as e:
                raise QueryExecutionException(e.msg)

    def search_videos_by_title_from_db(self, search_query, page, per_page) -> SearchReturn:
        words = search_query.split()
        offset = (page - 1) * per_page
        with self.engine.begin() as connection:
            if connection is None:
                raise ConnectionNotFoundException("Expected Connection, found None")

            if not words:
                raise QueryNotFoundException("Query is empty")
            try:
                #  conditions = " AND ".join(
                #      ["(Title ILIKE :word{} OR Description ILIKE :word{})".format(i, i) for i, _ in enumerate(words)]
                #  )
                #  sql_query = text("""
                #     SELECT Title, Description, PublishDateTime, ThumbnailURL
                #     FROM youtube.videos
                #     WHERE TITLE ILIKE '%{}%' OR Description ILIKE '%{}%'
                #     ORDER BY PublishDateTime DESC
                # """.format(words[-1], words[-1]))
                conditions = []
                params = {}
                for i, word in enumerate(words):
                    # For each word, create a condition that searches both Title and Description
                    condition = f"(Title ILIKE :word{i} OR Description ILIKE :word{i})"
                    conditions.append(condition)
                    # Add the word to the parameters dictionary
                    params[f'word{i}'] = f'%{word}%'

                # Join all conditions with OR or AND, depending on your search logic
                where_clause = " AND ".join(conditions)

                # Final SQL query
                sql_query = text(f"""
                       SELECT Title, Description, PublishDateTime, ThumbnailURL
                       FROM youtube.videos
                       WHERE {where_clause}
                       ORDER BY PublishDateTime DESC LIMIT :per_page OFFSET :offset
                   """)
                # Binding parameters for each word in the search query
                sql_params = {f"word{i}": f"'%{word}%'" for i, word in enumerate(words)}
                params['per_page'] = per_page
                params['offset'] = offset
                result = connection.execute(sql_query, params)
                videos_list = [
                    dict(row)  # Converts RowProxy to dict
                    for row in result.mappings().all()
                ]
                print(f"result is : {result}")
                logger.info("ASDASD")
            except SQLAlchemyError as e:
                logger.info(e)
                raise e
            except Error as e:
                raise QueryExecutionException(e.msg)

            return SearchReturn(video=videos_list)

    def insert_video(self, video_id, title, description, publishString, thumbnailURL):
        with self.engine.begin() as connection:
            if connection is None:
                return jsonify({"error": "Database connection could not be established"}), 500

            try:
                # Query to fetch paginated videos sorted by PublishDateTime in descending order
                # Convert string to datetime
                # Assuming the format 'YYYY-MM-DD HH:MM:SS'
                # Remove 'Z' and parse
                publishDateTime = datetime.fromisoformat(publishString.replace('Z', '+00:00'))

                # Check if the videoID already exists
                result = connection.execute(
                    text("SELECT VideoID FROM youtube.videos WHERE VideoID = :video_id"),
                    {'video_id': video_id}
                )
                if result.fetchone():
                    print("Video already exists in the database.")
                    return

                # Prepare and execute the insert query
                connection.execute(
                    text(
                        "INSERT INTO youtube.videos (VideoID, Title, Description, PublishDateTime, ThumbnailURL) "
                        "VALUES (:video_id, :title, :description, :publishDateTime, :thumbnailURL)"),
                    {'video_id': video_id, 'title': title, 'description': description,
                     'publishDateTime': publishDateTime,
                     'thumbnailURL': thumbnailURL}
                )
                print("Video inserted successfully")

            except Error as e:
                print(f"Error while connecting to MySQL: {e}")
# Function to insert a new video into the MySQL database
