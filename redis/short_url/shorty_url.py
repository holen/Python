# _*_ encoding:utf-8 _*_
__author__ = 'zhl'
__date__ = '2019/10/15 18:04'


from short_url import base36
from redis import Redis

ID_COUNTER = "ShortyUrl::id_counter"
URL_HASH = "ShortyUrl::url_hash"


class ShortyUrl:

    def __init__(self, client):
        self.client = client

    def shorten(self, target_url):
        """
        为目标网址创建并储存相应的短网址 ID 。
        """
        # 为目标网址创建新的数字 ID
        new_id = self.client.incr(ID_COUNTER)
        # 通过将 10 进制数字转换为 36 进制数字来创建短网址 ID
        # 比如说，10 进制数字 10086 将被转换为 36 进制数字 7S6
        short_id = base36.base10_to_base36(new_id)
        # 把短网址 ID 用作字段，目标网址用作值，
        # 将它们之间的映射关系储存到散列里面
        self.client.hset(URL_HASH, short_id, target_url)
        return short_id

    def restore(self, short_id):
        """
        根据给定的短网址 ID ，返回与之对应的目标网址。
        """
        return self.client.hget(URL_HASH, short_id)


if __name__ == '__main__':
    client = Redis(host="192.168.120.201", password="123456", decode_responses=True)
    shorty_url = ShortyUrl(client)
    short_id = shorty_url.shorten("www.hechuangyi.com")
    print(short_id)
    print(shorty_url.restore(short_id))
