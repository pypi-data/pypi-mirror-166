import json
import requests
import pandas as pd

class Trend:
    """
    트렌드 API 클래스
    """
    def __init__(self):
        pass

    def tisword(self):
        """
        티스워드 실시간 검색어 API
        """
        url = "https://tisword.com/realtime/realtimeKeyword.php"
        res = requests.get(url)
        if res.status_code == 200:
            return pd.DataFrame(res.json())
        else:
            return res
        
    def blackkiwi(self):
        """
        블랙키위 실시간 급상승 검색어 API
        """
        headers = {
            'referer': 'https://blackkiwi.net/service/trend',
        }
        url = "https://blackkiwi.net/api/service/keyword/issue-keywords"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return pd.DataFrame(res.json())
        else:
            return res