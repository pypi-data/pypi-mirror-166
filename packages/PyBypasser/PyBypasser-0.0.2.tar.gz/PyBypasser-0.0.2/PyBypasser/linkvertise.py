import json
import time
from urllib.parse import urlparse
from .utils import utils


class linkvertise:
    def __init__(self, debug=False):
        self.path = None
        self.urlparse = None
        self.debug = debug

    def is_own(self, url):
        self.urlparse = urlparse(url)
        utils.print_debug(self.debug, f"urlparse : {self.urlparse}")
        return self.urlparse.netloc == "linkvertise.com"

    def path_split(self, index=0):
        self.path = self.urlparse.path.split("/")
        return self.path

    def __get_api_redirect_link(self):
        self.path_split()
        utils.print_debug(self.debug, f"path split : {self.path}")
        if len(self.path) < 3:
            raise SyntaxError("url is miss format")
        self.base_path = '/'.join(self.path[0:3])
        response = utils.request(self.debug, 200, {
            "method": "GET",
            "url": f"https://publisher.linkvertise.com/api/v1/redirect/link/static{self.base_path}?origin=&resolution=1920x1080",
            "headers": {'user-agent': utils.getUserAgent(), "Accept": "application/json"}
        })
        data = response.json()
        target_type = data["data"]["link"]["target_type"].lower()
        if target_type == "url":
            target_type = "target"
        return response.cookies, data["data"]["link"]["id"], target_type, data["user_token"]

    def __get_paper_ostrichesica(self):
        response = utils.request(self.debug, 200, {
            "method": "GET",
            "url": "https://paper.ostrichesica.com/ct?id=14473",
            "headers": {"referer": "https://linkvertise.com/"}
        })
        data = response.text
        cq_token = data[data.find("jsonp") + 8: data.find("req") - 3]
        return cq_token

    def __post_traffic_validation(self, cookies, cq_token, linkvertise_id, user_token):
        response = utils.request(self.debug, 200, {
            "method": "POST",
            "url": f"https://publisher.linkvertise.com/api/v1/redirect/link{self.base_path}/traffic-validation?X-Linkvertise-UT={user_token}",
            "headers": {
                "host": 'publisher.linkvertise.com',
                "connection": 'keep-alive',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                "accept": 'application/json',
                'content-type': 'application/json',
                'sec-ch-ua-mobile': '?0',
                'user-agent': utils.getUserAgent(),
                'sec-ch-ua-platform': '"Windows"',
                'origin': 'https://linkvertise.com',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://linkvertise.com/',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
            },
            "json": {"type": "cq", "token": cq_token},
            "cookies": cookies
        })
        data = response.json()
        if "TARGET" not in data["data"]["tokens"]:
            raise Exception("recaptched")
        base64 = utils.encode_base64(json.dumps({
            "timestamp": int(time.time() * 1000),
            "random": "6548307",
            "link_id": linkvertise_id
        }, separators=(',', ':')))
        return base64, response.cookies, data["data"]["tokens"]["TARGET"]

    def __post_redirect_link(self, base64, cookies, target_type, token_target, user_token):
        response = utils.request(self.debug, 200, {
            "method": "POST",
            "url": f"https://publisher.linkvertise.com/api/v1/redirect/link{self.base_path}/{target_type}?X-Linkvertise-UT={user_token}",
            "headers": {
                'host': 'publisher.linkvertise.com',
                'connection': 'keep-alive',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
                'accept': 'application/json',
                'content-type': 'application/json',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
                'sec-ch-ua-platform': '"Windows"',
                'origin': 'https://linkvertise.com',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://linkvertise.com/',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
            },
            "json": {
                "serial": base64,
                "token": token_target
            },
            "cookies": cookies
        })
        return response.json()["data"][target_type]

    def bypass(self, url):
        if not self.is_own(url):
            utils.raise_not_own()
        cookies, linkvertise_id, target_type, user_token = self.__get_api_redirect_link()
        utils.print_debug(self.debug,
                          f"cookies : {cookies}\nlinkvertise_id : {linkvertise_id}\ntype : {target_type}\nuser_token : {user_token}")
        cq_token = self.__get_paper_ostrichesica()
        utils.print_debug(self.debug, f"cq_token : {cq_token}")
        base64, cookies, token_target = self.__post_traffic_validation(cookies, cq_token, linkvertise_id, user_token)
        utils.print_debug(self.debug, f"base64 : {base64}\ncookies : {cookies}\ntoken_target : {token_target}")
        response_url = self.__post_redirect_link(base64, cookies, target_type, token_target, user_token)
        utils.print_debug(self.debug, f"response url : {response_url}")
        return response_url
