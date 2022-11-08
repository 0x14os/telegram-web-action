from duckduckgo_search import ddg
import re


# def ddg(keywords, region='wt-wt', safesearch='Moderate', time=None, max_results=28, save_csv=False):
#     ''' DuckDuckGo search
#     keywords: keywords for query;
#     safesearch: On (kp = 1), Moderate (kp = -1), Off (kp = -2);
#     region: country of results - wt-wt (Global), us-en, uk-en, ru-ru, etc.;
#     time: 'd' (day), 'w' (week), 'm' (month), 'y' (year), or 'year-month-date..year-month-date';
#     max_results = 28 gives a number of results not less than 28,
#                   maximum DDG gives out about 200 results,
#     save_csv: if True, save results to csv file.
#     '''

def so(key=None):
    uri = []
    results = ddg(keywords="site:t.me " + key, max_results=80)
    if len(results) > 0:
        for v in results:
            # print(v)
            href = v["href"]
            matchObj = re.search(r'https://t.me/s/', href, re.M | re.I)
            if matchObj is None:
                uri.append(href)
    return uri


# if __name__ == '__main__':

    # uri = so("chuỗi khối")
    # print(uri)
    # for vv in uri:
    #     html = pq(url=vv)
    # req = requests.get(url=target)
    # req.encoding = 'utf-8'
    # print(req.text)
