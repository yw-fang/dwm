# -*- coding: utf8 -*-

import re
import sys
import json
from subprocess import Popen, PIPE

from mybs import SelStr
from comm import DWM, echo, start, debug


class KANTV6(DWM):
    handle_list = ['//kantv6\.com/', '//www\.kantv6\.com/']

    def query_info(self, url):
        # https://www.kantv6.com/tvdrama/301948271219001-161948271219033
        # https://www.kantv6.com/index.php/video/play?tvid=301948271219001&part_id=161948271219033&line=1&seo=tvdrama
        sect, tvid, ptid = self.get_stp(url)
        if not ptid:
            echo("no ptid")
            return
        title = self.get_title(tvid, ptid, sect)
        du = "https://www.kantv6.com/index.php/video/play"
        du = "%s?tvid=%s&part_id=%s&line=1&seo=%s" % (du, tvid, ptid, sect)
        dat = self.get_hutf(du)
        dat = json.loads(dat)
        title = title + "_" + dat['data']['part_title']
        debug(json.dumps(dat, indent=2))
        echo("title", title)
        #return
        us = self.try_m3u8('https:' + dat['data']['url'])
        return title, None, us, None

    def get_playlist(self, url):
        sect, tvid, ptid = self.get_stp(url)
        u = 'https://www.kantv6.com/index.php/video/part'
        u = '%s?tvid=%s' % (u, tvid)
        dat = self.get_hutf(u)
        dat = json.loads(dat)
        debug(json.dumps(dat, indent=2))
        bu = 'https://www.kantv6.com/%s/%s-' % (sect, tvid)
        return [(a['part_title'], bu + a['part_id']) for a in dat['data']['partList']]

    def get_title(self, tvid, ptid, sect):
        u = "https://www.kantv6.com/index.php/video/info"
        u = "%s?tvid=%s&seo=%s" % (u, tvid, sect)
        dat = self.get_hutf(u)
        dat = json.loads(dat)
        debug(json.dumps(dat, indent=2))
        return dat['data']['title']

    def get_stp(self, url):
        m = re.search("/(tvdrama)/(\d+)-(\d+)", url)
        if m:
            sect, tvid, ptid = m.groups()
            return sect, tvid, ptid
        m = re.search("/(tvdrama)/(\d+)", url)
        sect, tvid = m.groups()
        return sect, tvid, ""

    def test(self, argv):
        url = 'https://www.kantv6.com/tvdrama/301948271219001-161948271219033'
        url = 'https://www.kantv6.com/index.php/video/part?tvid=301948271219001'
        url = 'https://www.kantv6.com/index.php/video/info?tvid=301948271219001&seo=tvdrama'
        url = 'https://www.kantv6.com/tvdrama/301948271219001'
        #self.get_title(url)
        self.get_playlist(url)


if __name__ == '__main__':
    start(KANTV6)