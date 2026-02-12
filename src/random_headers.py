import random

headers = [
{
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",  # Unique: Linux FF
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "none",
"Sec-Fetch-User": "?1",
"Connection": "keep-alive",
"Referer": "",
"sec-ch-ua": '"Not_A Brand";v="8", "Gecko";v="147"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": '"Linux"',
},
{
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",  # Unique: Older desktop Chrome (updated version)
"sec-ch-ua": '"Not:A Brand";v="8", "Chromium";v="145", "Google Chrome";v="145"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": '"Windows"',
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Upgrade-Insecure-Requests": "1",
"Referer": "",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "none",
"Sec-Fetch-User": "?1",
"Connection": "keep-alive",
},
{
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0",  # Deduped FF Windows (kept fullest version)
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "none",
"Sec-Fetch-User": "?1",
"Connection": "keep-alive",
"Referer": "",
"sec-ch-ua": '"Not_A Brand";v="8", "Gecko";v="147"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": '"Windows"',
},
{
"User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-A146P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36",  # Deduped Samsung Android (kept fullest, updated version)
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "none",
"Sec-Fetch-User": "?1",
"Connection": "keep-alive",
"Referer": "",
"sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="145", "Google Chrome";v="145"',
"sec-ch-ua-mobile": "?1",
"sec-ch-ua-platform": '"Android"',
},
{
"User-Agent": "Mozilla/5.0 (Linux; Android 14; 23021RAAEG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36",  # Deduped Redmi Android (kept fullest, updated version)
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "none",
"Sec-Fetch-User": "?1",
"Connection": "keep-alive",
"Referer": "",
"sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="145", "Google Chrome";v="145"',
"sec-ch-ua-mobile": "?1",
"sec-ch-ua-platform": '"Android"',
},
{
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",  # Unique: Newer desktop Chrome (updated version)
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
"Accept-Encoding": "gzip, deflate, br, zstd",
"Upgrade-Insecure-Requests": "1",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "none",
"Sec-Fetch-User": "?1",
"Connection": "keep-alive",
"Referer": "",
"sec-ch-ua": '"Google Chrome";v="145", "Chromium";v="145", "Not_A Brand";v="24"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": '"Windows"',
},
]

def get_random_headers(link):
    template = random.choice(headers).copy()
    if random.random() < 0.15:
        template["Accept-Language"] = "en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7"
    template["Referer"] = link
    return template

def headers_len():
    return len(headers)