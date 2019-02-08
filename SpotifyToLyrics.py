from bs4 import BeautifulSoup
import requests
import csv
# imports

typee= input("what kind of link are you giving me?")
link=input("Put a spotify link with no spaces")
source = requests.get(link).text # gets the html for beautiful soup

soup = BeautifulSoup(source, 'lxml')
soup.prettify()
csv_file = open('cms_scrape.csv', 'w')
file = open('SongLyrics','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['num','name', 'artist', 'album', "lyrics website"])# creates .CSV type file

def findLyrics(link):   # tries to find the song lyrics
    try:
        source = requests.get(link).text
        so = BeautifulSoup(source, 'lxml')
        file.write("\n\n" + songName + "\n\t-" + artist + '\n\n' + so.p.text)

    except:
        print('no lyrics')


if typee=='playlist': #works out info for the playlist
    tracklist = soup.ol
    tracklist.prettify()
    i = 1
    for track in tracklist:
        name = track.find_all('span')

        featuring = name[1].text.split('•')[0].replace(name[2].text,' ')
        album= ' '
        try:
            if name[4].text[0].isalpha():
                album = name[4].text
                if name[5].text[0].isalpha():
                    album = name[5].text
            else:
                album = name[3].text
        except:
            print("oops")
        print()
        artist= str(name[2].text).replace('&amp;', 'and').replace('&', 'and')
        songName = (str(name[0].text).split(' - ')[0].split(' (')[0]).replace('&amp;', 'and').replace('&', 'and')
        linkPart = artist.replace(' ', '-')+'-'+songName.replace(' ', '-')
        lyricsLink = "https://genius.com/"+linkPart+"-lyrics"
        findLyrics(lyricsLink)

        csv_writer.writerow([i, songName, artist+', '+featuring, album, lyricsLink]) #writes info into the CSV
        i += 1


if typee=='album':
    lol = soup.h1.text+" "+soup.h2.text
    albumArtist= lol.split(" By ")
    album = albumArtist[0]
    artist = albumArtist[1]
    for Am in soup.ol:
        songName = Am.text.split("\n")[2].strip()[:-8]


        artist = artist.replace('&amp;', 'and').replace('&', 'and')
        songName = songName.replace('&amp;', 'and').replace('&', 'and').replace("","").replace("\'","")
        linkPart = artist.replace(' ', '-') + '-' + songName.replace(' ', '-')
        lyricsLink = "https://genius.com/" + linkPart + "-lyrics"
        findLyrics(lyricsLink)

        csv_writer.writerow([1, songName, artist, album, lyricsLink])#writes info into the CSV

csv_file.close()
