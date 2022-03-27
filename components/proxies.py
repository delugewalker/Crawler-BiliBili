def getProxies(proxy, http=True, https=True):

    if http and https:
        proxies = {
            "http": "socks5h://%(proxy)s" % {'proxy': proxy},
            "https": "socks5h://%(proxy)s" % {'proxy': proxy}
        }
    elif http:
        proxies = {
            "http": "socks5h://%(proxy)s" % {'proxy': proxy},
        }
    elif https:
        proxies = {
            "https": "socks5h://%(proxy)s" % {'proxy': proxy}
        }
    else:
        raise EOFError('Http or https must be opened!')

    return proxies