from sqlalchemy.exc import SQLAlchemyError

from dao.video_sql_queries import VideoInformationRepo, PaginatedReturn, QueryExecutionException, ConnectionNotFoundException, \
    QueryNotFoundException, SearchReturn
from googleapiclient.discovery import build
from isodate import parse_duration
from googleapiclient.errors import HttpError
from config.api_keys import api_keys
class DatabaseException(Exception):
    def __init__(self, message, e):
        super().__init__(e)
        self.message = message

    def __repr__(self):
        return f"{self.message}"


class SearchException(Exception):
    def __init__(self, message, e):
        super().__init__(e)
        self.message = message

    def __repr__(self):
        return f"{self.message}"


class VideoInfoService:
    def __init__(self):
        self.videoInfoRepo = VideoInformationRepo()

    def fetch_paginated_videos_from_db(self,page, per_page) -> PaginatedReturn:
        try:
            paginated_return = self.videoInfoRepo.get_paginated_videos_list_from_db(page, per_page)
        except QueryExecutionException as e:
            raise DatabaseException("Query Failure Exception", e)
        except ConnectionNotFoundException as e:
            raise DatabaseException("Connection Not Found Exception", e)
        except Exception as e:
            raise DatabaseException("Something Went Wrong", e)
        return paginated_return

    def search_video_by_title(self, search_query, page, per_page) -> SearchReturn:
        try:
            search_return = self.videoInfoRepo.search_videos_by_title_from_db(search_query, page, per_page)
        except ConnectionNotFoundException as e:
            raise SearchException("Connection Not Found Exception", e)
        except QueryNotFoundException as e:
            raise SearchException("Query Not Found Exception", e)
        except QueryExecutionException as e:
            raise SearchException("Execution Failed Exception", e)
        except SQLAlchemyError as e:
            raise SearchException("Connection Not Found Exception", e)
        except Exception as e:
            raise SearchException("Something Went Wrong", e)
        return search_return

    def fetch_youtube_videos_by_query(self, search_query):
        success = False
        for api_key in api_keys:
            try:
                # Get the search query from user input
                print("Fetching the urls from youtube api.")
                youtube = build('youtube', 'v3', developerKey=api_key)

                # Step 1: Initial search
                request = youtube.search().list(
                    q=search_query,
                    part='snippet',
                    order='date',
                    type='video',
                    maxResults=100
                )
                response = request.execute()

                video_ids = [item['id']['videoId'] for item in response['items']]
                print(f"Video Ids fetched: {video_ids}")

                # Step 2: Fetch video details and filter out Shorts
                details_request = youtube.videos().list(
                    part='contentDetails',
                    id=','.join(video_ids)
                )
                details_response = details_request.execute()

                for item in details_response['items']:
                    video_id = item['id']
                    duration = parse_duration(item['contentDetails']['duration']).total_seconds()

                    # Assuming you want to exclude videos shorter than 60 seconds
                    if duration > 60:
                        # Find the snippet from the initial response
                        snippet = next((x['snippet'] for x in response['items'] if x['id']['videoId'] == item['id']),
                                       None)
                        if snippet:
                            title = snippet['title']
                            description = snippet['description']
                            publishTime = snippet['publishedAt']
                            thumbnailsUrls = snippet['thumbnails']['default']['url']  # Adjust as needed

                            # Print the extracted information
                            print(f"Title: {title}")
                            print(f"Description: {description}")
                            print(f"Publish Time: {publishTime}")
                            print(f"Thumbnail URL: {thumbnailsUrls}")
                            print(f"Video Id:  {video_id}")

                            # Insert into database as needed
                            self.videoInfoRepo.insert_video(video_id, title, description, publishTime, thumbnailsUrls)
                            print("-" * 40)

                success = True
                break
            except HttpError as e:
                if e.resp.status in [403, 429]:
                    print(f"Quota exceeded for API key: {api_key}")
                    continue  # Try the next API key
                else:
                    print(f"An error occurred: {e}")
                    break  # Break the loop on other errors

        if not success:
            print("Failed to fetch and process videos due to API quota limitations or other errors.")