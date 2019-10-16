# _*_ encoding:utf-8 _*_
__author__ = 'zhl'
__date__ = '2019/10/16 10:30'

from redis import Redis


class Paging:
    """ 用 Redis List 实现分页 """

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def add(self, item):
        """
        将给定元素添加到分页列表中。
        """
        self.client.lpush(self.key, item)

    def get_page(self, page_number, item_per_page):
        """
        从指定页数中取出指定数量的元素。
        """
        # 根据给定的 page_number （页数）和 item_per_page （每页包含的元素数量）
        # 计算出指定分页元素在列表中所处的索引范围
        # 例子：如果 page_number = 1 ， item_per_page = 10
        # 那么程序计算得出的起始索引就是 0 ，而结束索引则是 9
        start_index = (page_number - 1) * item_per_page
        end_index = page_number * item_per_page - 1
        # 根据索引范围从列表中获取分页元素
        return self.client.lrange(self.key, start_index, end_index)

    def size(self):
        """
        返回列表目前包含的分页元素数量。
        """
        return self.client.llen(self.key)


if __name__ == "__main__":
    client = Redis(host="192.168.120.201", password="123456", decode_responses=True)
    topics = Paging(client, "user-topics")
    for i in range(1, 20):
        topics.add(i)

    print(topics.get_page(1, 5))
    print(topics.get_page(2, 5))
    print(topics.get_page(1, 10))
    print(topics.size())