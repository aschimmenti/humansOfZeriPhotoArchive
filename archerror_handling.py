from requests import Session
import requests, requests_cache
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def _requests_retry_session(
    tries=3,
    status_forcelist=(403,500, 502, 504, 520, 521, 522),
    session=None
) -> Session:
    session = session or requests.Session()
    retry = Retry(
        total=tries,
        read=tries,
        connect=tries,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def handle_request(url:str, cache_path:str, error_log_dict:dict) -> None:
    requests_cache.install_cache(cache_path)
    try:
        data = _requests_retry_session().get(url, timeout=60)
        if data.status_code == 200:
            return data.json()
        else:
            error_log_dict[url] = data.status_code
    except Exception as e:
        error_log_dict[url] = str(e)