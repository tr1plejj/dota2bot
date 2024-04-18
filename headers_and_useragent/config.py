from fake_useragent import UserAgent

ua = UserAgent()

headers_for_stratz = {
    'User-Agent': f'{ua.random}',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiNzVmODYxYzktMWFlZi00NmRmLTliZDYtYzY0NWFiOGE5NDQwIiwiU3RlYW1JZCI6IjExNTEwNjcxODYiLCJuYmYiOjE3MTAwNTkxMTIsImV4cCI6MTc0MTU5NTExMiwiaWF0IjoxNzEwMDU5MTEyLCJpc3MiOiJodHRwczovL2FwaS5zdHJhdHouY29tIn0.84meNwXgF6YuVOIVKLo7v3GhlK4uvmnZqYM7zfNa_s4'
}
headers_for_opendota = {
    'User-Agent': f'{ua.random}'
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': f'{ua.random}'
}
