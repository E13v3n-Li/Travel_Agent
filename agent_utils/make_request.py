import requests

def make_req(url, method="GET", params=None, headers=None, timeout=10):
    try:
        if method.upper() == "GET":
            res = requests.get(url, params=params, headers=headers, timeout=timeout)
        elif method.upper() == "POST":
            res = requests.post(url, params=params, headers=headers, timeout=timeout)
        else:
            print(f"不支持的 method: {method}")
            return None
        return res
    except Exception as e:
        print(f"请求异常: {e}")
        return None