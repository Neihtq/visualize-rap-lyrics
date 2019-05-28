from lyricsDownloader import *
import timeit

if __name__ == "__main__":
    start = timeit.default_timer()
    scrape()
    stop = timeit.default_timer()
    print("done secs", stop)