def url_Splicing(url_resp,href:str):
    """
    :param url_resp: #链接或响应对象
    :param href: 需要拼接的链接
    :return: 拼接完成的链接
    """
    start_url=url_resp

    if href.startswith('http'):
        return href

    if type(url_resp)!=str:
        start_url=url_resp.url

    if href.startswith('/'):
        href=href.lstrip('/')
        href_sp=href.split('/')[0]
        start_url_rsplit=start_url.rsplit('/'+href_sp,1)
        if len(start_url_rsplit)==2:
            start_url=start_url_rsplit[0]
        elif len(start_url_rsplit)==1:
            start_url = start_url.rsplit('/',1)[0]
    elif href.startswith('./'):
        href=href.lstrip('./')
        href_sp=href.split('/')[0]
        start_url_rsplit=start_url.rsplit('/'+href_sp,1)
        if len(start_url_rsplit)==2:
            start_url=start_url_rsplit[0]
        elif len(start_url_rsplit)==1:
            start_url = start_url.rsplit('/',1)[0]
    else:
        href_sp=href.split('/')[0]
        start_url_rsplit = start_url.rsplit('/' + href_sp,1)
        if len(start_url_rsplit) == 2:
            start_url = start_url_rsplit[0]
        elif len(start_url_rsplit) == 1:
            start_url = start_url.rsplit('/',1)[0]
    return start_url + '/' + href

def headers_dict(headers_raw):
    if headers_raw is None:
        return None
    if headers_raw.startswith(':'):
        print('requests请求头中键名前的冒号需要删除！！！')
    headers = headers_raw.splitlines()
    headers_tuples = [header.lstrip(':').split(":", 1) for header in headers]

    result_dict = {}
    for header_item in headers_tuples:
        if not len(header_item) == 2:
            continue

        item_key = header_item[0].strip()
        item_value = header_item[1].strip()
        result_dict[item_key] = item_value

    return result_dict

def param_dict(param_raw):
    if param_raw is None:
        return None
    params = param_raw.splitlines()
    param_tuples = [param.split(":", 1) for param in params]

    result_dict = {}
    for param_item in param_tuples:
        if not len(param_item) == 2:
            continue

        item_key = param_item[0].strip()
        item_value = param_item[1].strip()
        result_dict[item_key] = item_value

    return result_dict