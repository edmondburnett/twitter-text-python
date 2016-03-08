#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unwind short-links e.g. bit.ly, t.co etc to their canonical links"""
from __future__ import unicode_literals, print_function
import requests


def follow_shortlinks(shortlinks):
    """Follow redirects in list of shortlinks, return dict of resulting URLs"""
    links_followed = {}
    for shortlink in shortlinks:
        url = shortlink
        request_result = requests.get(url)
        redirect_history = request_result.history
        # history might look like:
        # (<Response [301]>, <Response [301]>)
        # where each response object has a URL
        all_urls = []
        for redirect in redirect_history:
            all_urls.append(redirect.url)
        # append the final URL that we finish with
        all_urls.append(request_result.url)
        links_followed[shortlink] = all_urls
    return links_followed


if __name__ == "__main__":
    shortlinks = ['http://t.co/8o0z9BbEMu', 'http://bbc.in/16dClPF']
    print (follow_shortlinks(shortlinks))
