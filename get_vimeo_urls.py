#!/usr/bin/env python

import re
import sys
import argparse
import requests


def get_download_urls(vimeo_url, referer):
    headers = { 'Referer': referer } if referer else {}
    r = requests.get('https://player.vimeo.com/video/%s' %
                     vimeo_url.split('/')[-1], headers=headers)
    matches = re.findall(r'"(.*?)"', r.text)
    results = [m for m in matches if '?expires=' in m]
    if len(results) == 0:
        results = [m for m in matches if '?token=' in m]
    return results


def get_content_size(download_urls):
    content_with_size = []
    for url in download_urls:
        r = requests.head(url)
        content_with_size.append(
            {'url': url, 'size': int(r.headers['content-length']) / 1024 / 1024})
    return content_with_size


def display_options(download_urls):
    quality = ['High', 'Medium', 'Low'][-1 * len(download_urls):]
    options = sorted(get_content_size(download_urls),
                     key=lambda k: k['size'], reverse=True)
    for i in xrange(len(download_urls)):
        print('%s quality (%sMB):' % (quality[i], options[i]['size']))
        print('%s\n' % options[i]['url'])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url',
                        help='link to the video page (e.g: https://vimeo.com/XXXXXXXXX)')
    parser.add_argument('-r', '--referer',
                        help='domain to specify as "Referer" (for private videos)')
    return parser.parse_args()


def main():
    args = parse_args()
    print('getting download urls...\n')
    download_urls = get_download_urls(args.url, args.referer)
    display_options(download_urls)

if __name__ == '__main__':
    main()
