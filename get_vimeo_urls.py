#!/usr/bin/env python

import re
import sys
import argparse
import requests
from urlparse import urlparse


def get_vimeo_links_from_page(url):
    r = requests.get(url)
    return re.findall('http[s]?://player.vimeo.com/video/\d+', r.content)


def get_referer(url, referer):
    if referer:
        return referer
    else:
        uri = urlparse(url)
        return '%s://%s' % (uri.scheme, uri.netloc)


def get_download_urls(vimeo_url, referer):
    headers = {'Referer': referer} if referer else {}
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


def display_options(download_urls, gui=False):
    quality = ['High', 'Medium', 'Low'][-1 * len(download_urls):]
    options = sorted(get_content_size(download_urls),
                     key=lambda k: k['size'], reverse=True)
    l = len(download_urls) if len(download_urls) < 3 else 3
    if gui:
        links = []
        for i in xrange(l):
            links.append({
                'quality': quality[i],
                'size': options[i]['size'],
                'url': options[i]['url']
            })
        return links
    for i in xrange(l):
        print('%s quality (%sMB):' % (quality[i], options[i]['size']))
        print('%s\n' % options[i]['url'])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url',
                        help='link to the video page (e.g: https://vimeo.com/XXXXXXXXX),'
                        ' or to a page containing vimeo links')
    parser.add_argument('-r', '--referer',
                        help='domain to specify as "Referer" (for private videos)')
    return parser.parse_args()

def gui_flow(url):
    results = {}
    if 'vimeo' in url:
        urls = [url]
    else:
        print('getting vimeo urls from page...\n')
        urls = get_vimeo_links_from_page(url)
        print('found %d vimeo videos' % len(urls))
    referer = get_referer(url, None)
    for url in urls:
        print('getting download urls for %s\n' % url)
        current_results = display_options(get_download_urls(url, referer), gui=True)
        if len(current_results) > 0:
            results[url] = current_results
    return results

def main():
    args = parse_args()
    if 'vimeo' in args.url:
        urls = [args.url]
    else:
        print('getting vimeo urls from page...\n')
        urls = get_vimeo_links_from_page(args.url)
        print('found %d vimeo videos' % len(urls))
    referer = get_referer(args.url, args.referer)
    print referer
    for url in urls:
        print('getting download urls for %s\n' % url)
        download_urls = get_download_urls(url, referer)
        display_options(download_urls)

if __name__ == '__main__':
    main()
