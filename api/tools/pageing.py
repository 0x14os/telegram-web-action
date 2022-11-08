# !/usr/bin/env python
# -*- coding:utf-8 -*-

class Pageing:
    """
    has_next 如果下一页存在，返回 True
    has_prev 如果上一页存在，返回 True
    items 当前页的数据列表
    next_num 下一页的页码
    page 当前页码
    pages 总页数
    per_page 每页的条数
    prev_num 上一页的页码
    query 用于创建此分页对象的无限查询对象。
    total 总条数
    iter_pages(left_edge=2, left_current=2, right_current=5, right_edge=2)
    迭代分页中的页码，四个参数，分别控制了省略号左右两侧各显示多少页码，在模板中可以这样渲染"""

    next_num = None
    prev_num = None
    page = 1
    pages = None
    per_page = None
    total = None
    data = {}
    items = None

    def __init__(self, next_num=0, prev_num=0, page=1, pages=1, per_page=10, total=0, items=None):
        self.next_num = next_num
        self.prev_num = prev_num
        self.page = page
        self.pages = pages
        self.per_page = per_page
        self.total = total
        self.items = items

    def initDataList(self):
        list = {}
        list["page"] = self.page
        # list["pages"] = self.pages
        list["per_page"] = self.per_page
        list["total"] = self.total
        # list["next_num"] = self.next_num
        # list["prev_num"] = self.prev_num
        list["items"] = {}
        if self.items != None:
            list["items"] = self.items
        self.data = list

    def results(self):
        self.initDataList()
        return self.data
