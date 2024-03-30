import threading
from controllers.video_controller import app, service
import time

from services.service import VideoInfoService



def run_periodically(interval, func, *args):
    """Run a function in a separate thread at given intervals."""

    def func_wrapper():
        while True:
            print(" i'm running")
            func(*args)
            time.sleep(interval)

    thread = threading.Thread(target=func_wrapper)
    #thread.daemon = True  # Daemonize thread
    thread.start()
    print("yoyoyoyooyoyo")
    print("ASdASDSA")


if __name__ == '__main__':
    run_periodically(60, service.fetch_youtube_videos_by_query, "Cricket")
    app.run(host='0.0.0.0', debug=True, port=5020)
