import argparse
import requests
import os
import time
from urllib.request import urlretrieve
from pathlib import Path


# Parser
parser = argparse.ArgumentParser()
parser.add_argument('sub', help="Name of the Subreddit (without r/)")
parser.add_argument('-s', default='top',  help="Sort based on Hot or Top")
parser.add_argument('-d', default='n',
                    help="duplicate flag for posts with same caption")

params = parser.parse_args()

subreddit = params.sub
sort = params.s
duplicatecaption = params.d

# Defining URLS
if params.s == 'top':
    url = f'https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=all'
    print(f'\nSubreddit: r/{subreddit} \nSort: {sort} posts of all time')
    time.sleep(2.5)

else:
    url = f'https://www.reddit.com/r/{subreddit}/.json?'
    print(f'\nSubreddit: r/{subreddit} \nSort: {sort} posts')
    time.sleep(2.5)


def download(imageurl, filename, source, foldername):
    try:
        filepath = foldername
        if not os.path.exists(filepath):
            print(f'Created Directory {filepath}{os.sep}')
            os.makedirs(filepath)
            time.sleep(2)

        elif source == 'i.imgur.com':
            imageurl = imageurl.replace('.gifv', '.mp4')
            fileurl = os.path.splitext(imageurl)[1]
            filename = f'{filepath}{os.sep}{filename}{fileurl}'
            if os.path.exists(filename):
                if params.d == 'y':
                    x = filename.rsplit(".", 1)
                    i = 1
                    x[0] = x[0]+"("+str(i)+")"
                    x[1] = "."+x[1]
                    dupfilename = ''.join(map(str, x))
                    urlretrieve(imageurl, dupfilename)
                    i += 1
                    return False
                else:
                    print(f'File {filename} already exists')
                return False

            print(f'\nDownloading {filename}')
            urlretrieve(imageurl, filename)

        elif source == 'i.redd.it':
            fileurl = os.path.splitext(imageurl)[1]
            filename = f'{filepath}{os.sep}{filename}{fileurl}'

            if os.path.exists(filename):
                if params.d == 'y':
                    x = filename.rsplit(".", 1)
                    i = 1
                    x[0] = x[0]+"("+str(i)+")"
                    x[1] = "."+x[1]
                    dupfilename = ''.join(map(str, x))
                    urlretrieve(imageurl, dupfilename)
                    i += 1
                    return False
                else:
                    print(f'File {filename} already exists')
                return False

            print(f'\nDownloading {filename}')
            urlretrieve(imageurl, filename)

    except Exception as e:
        print(e)


def connection(url):

    # User Agent to prevent Response 429
    userAgent = {
        'User-agent': 'Python Reddit Media Downloader Bot : 0.1 (by Aman0819)'
    }

    response = requests.get(url, headers=userAgent)
    if response.status_code == 200:
        print("\nConnection Successful!")
        time.sleep(2)
        print(f"Starting Download...")
        time.sleep(1)

        responsejson = response.json()
        nextpage = responsejson['data']['after']
        posts = responsejson['data']['children']
        for post in posts:
            source = post['data']['domain']
            mediaurl = post['data']['url']
            filename = post['data']['title']
            # Works on Windows, Linux and Mac!
            downloadfolder = str(os.path.join(Path.home(), "Downloads"))
            download(mediaurl, filename.replace('/', '_'), source, downloadfolder +
                     os.sep + 'Reddit' + os.sep + subreddit)

        if nextpage is not None:
            print("\nLoading Next Page")
            url = url + '&after=' + nextpage
            connection(url)
    else:
        print(response)


connection(url)
