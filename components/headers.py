from fake_useragent import UserAgent



def get_headers(ua):

    headers = {
        "accept-encoding": "gzip",  # gzip压缩编码  能提高传输文件速率
        "user-agent": ua.random
    }

    return headers


