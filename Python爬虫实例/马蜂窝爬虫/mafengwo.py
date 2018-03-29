import requests
from multiprocessing import Process
import multiprocessing
from lxml import etree
from collections import defaultdict
import re
import time
from Static import city
from Static1 import city_prov
import psycopg2


class Task:
    def __init__(self):
        self.Base = "https://m.mafengwo.cn/gl/catalog/index?catalog_id="
        self.sess = requests.Session()
        self.rule = defaultdict(dict)
        self.mg = multiprocessing.Manager()
        self.set = multiprocessing.Manager().list()
        self._citys = city
        self.prov = city_prov
        self.rule['子页面'] = {
            "标题": "//div[@class='hd']/div[@class='title']/text()",
            "子集": "//div[@class='bd']/div[@class='list']/ul[@class='clearfix']//a/@href",
            "页面子标题": "",
            "页面子内容": "",
            "总内容": "//div[@class='wrapper']"}
        self.filters = ['<', '>', 'p', 'b', '/']
        self.sql = "insert into tourism(area,title,content) values(%s,%s,%s)"
        self.conn = psycopg2.connect(database="postgres", user="linhanqiu", password="linhanqiu", host="127.0.0.1", port="5432")
        self.cursor = self.conn.cursor()


    # 替换Url

    def _Init(self, code):
        return self.Base + str(code)
    # 判重

    def _is_exist(self, code):
        if code in self.set:
            return True
        else:
            return False
    # 基本请求

    def task(self, c):
        if self._is_exist(c):
            pass
        else:
            con = self.sess.get(self._Init(code=c))
            try:
                contents = self._Script(con.text)
                if contents[0] in self._citys:
                    sub_url = [
                        urls for urls in contents if isinstance(
                            urls, list)][0]

                    ret = list(map(self.sub_task, sub_url))
                    # print(ret)
                    params = [(contents[0],title,sub[0].get(title)) for sub in ret for title in sub[0]]
                    print(params)
                    # 批量插入
                    # print(params)
                    self.cursor.executemany(self.sql, params)
                    try:
                        self.conn.commit()
                    except Exception as e:
                        pass
                else:
                    print("国外城市")

            except Exception as e:
                pass

    # 子链接请求
    def sub_task(self, url):
        con = self.sess.get(url)
        try:
            contents = self._Script(con.text, sub=False)
            return contents
        except Exception as e:
            pass
    # 解析

    def _Script(self, content, sub=True):
        con = etree.HTML(content)
        data = []
        for i in self.rule.get('子页面'):
            if sub:
                if i in ('子集', '标题'):
                    data.append(
                        self._Script_Help(
                            con, self.rule.get('子页面').get(i)))
                else:
                    pass
            else:
                if i in ('总内容', ):
                    data.append(
                        self._Script_Help(
                            con, self.rule.get('子页面').get(i)))
                else:
                    pass
        return data

    def _add(self, code):
        """
        添加代码，判重
        :param code:
        :return:
        """
        if code in self.set:
            pass
        else:
            try:
                self.set.append(code)
            except Exception as e:
                pass

    def _filter(self, content):
        patterns = '|'.join(self.filters)
        content = re.sub(patterns, '', ''.join(content))
        return content

    def _Script_Help(self, content, xpath_rule):
        """
        提取帮助
        :param content:
        :param xpath_rule:
        :return:
        """
        if xpath_rule == "//div[@class='hd']/div[@class='title']/text()":
            data = content.xpath(xpath_rule) if isinstance(
                content.xpath(xpath_rule), str) else ''.join(
                content.xpath(xpath_rule))
        elif xpath_rule == "//div[@class='bd']/div[@class='list']/ul[@class='clearfix']//a/@href":
            data = [i.strip()
                    for i in content.xpath(xpath_rule) if i.endswith('#1')]
            codes = [''.join(re.findall(r'catalog_id=(\d+)', i)) for i in data]
            for i in codes:
                self._add(i)
        elif xpath_rule == "//div[@class='wrapper']":
            data = etree.tostring(
                content.xpath(xpath_rule)[0],
                xml_declaration=True,
                encoding='utf-8').decode('utf-8')
            data = re.sub(r'section[\s\S]*?</section>', '', data)
            data = re.findall(r'id="\d[\s\S]*?div', data)
            data = [re.sub(r'\n', '', i) for i in data]
            data = {
                ''.join(
                    re.findall(
                        r'h3>([\s\S]*?)</h3>',
                        i)): re.findall(
                    r'<p>([\s\S]*)</p>',
                    i) for i in data}
            data = {k: self._filter(v) for k, v in data.items()}
        else:
            data = etree.tostring(
                content.xpath(xpath_rule)[0],
                xml_declaration=True,
                encoding='utf-8').decode('utf-8')

        return data

    # 执行方法

    def __call__(self, *args, **kwargs):
        for i in range(100, 4500):
            p = Process(target=self.task, args=(str(i),))
            p.start()
            p.join()


if __name__ == "__main__":
    test = Task()
    test()
