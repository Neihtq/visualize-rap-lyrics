from lyricsDownloader import *
import timeit

if __name__ == "__main__":
    # Test store_lyrics(): includes get_html, scrape_ftp_page(), write_to_csv()
    start = timeit.default_timer()
    href = "anonymous/03greedo/"
    name = "03greedo"
    store_lyrics(name, href)

    stop = timeit.default_timer()
    print('Time in sec: ', stop - start) 
    print("finished store_lyrics()")
    


    # Test get_release_year_from_album():
    test_lines = ['Big Sean - Finally Famous Vol. 3: Big (Oct. 2010)', 'Tupac Shakur - The Lost Tapes (1989/2000) BUY NOW!', 'Eminem - The Marshall Mathers LP 2 (2013) BUY NOW!']
    for test in test_lines:
        print(get_release_year_from_album(test))
    
    # Test store_lyrics_of_big_artist: includes
    

