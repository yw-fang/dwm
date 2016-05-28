#! /usr/bin/python
# -*- coding: utf8 -*-

import os
import sys
import shutil
from subprocess import Popen, PIPE, CalledProcessError

from comm import echo


def run1(name, cnt):
    cmd = ["avconv"]
    for i in range(1, cnt + 1):
        cmd.append("-i")
        cmd.append("%s[%02d].mp4"% (name, i))
    cmd.append("-y")
    cmd.append("-c")
    cmd.append("copy")
    cmd.append("%s.mp4" % name)
    p = Popen(cmd)
    p.wait()


def merge1(name, ext, cnt):
    cmd = ['cat']
    for i in range(cnt):
        #cmd.append("tmp/欢乐颂42[%02d].mp4.ts"% i)
        cmd.append("%s[%02d].%s.ts"% (name, i, ext))
    cmd.append(">")
    tmpfn = "%s.%s.ts" % (name, ext)
    cmd.append(tmpfn)
    p = Popen(" ".join(cmd), shell=True)
    p.wait()
    p = Popen(["avconv", "-i", tmpfn, "-strict", "experimental",
               "-y", "-c", "copy", "%s.%s" % (name, ext)])
    p.wait()


def merge(name, ext, cnt, clean=False):
    # avconv -i tmp/嘻哈帝国第一季12[99].mp4 -c copy -f mpegts -bsf h264_mp4toannexb - > aa.ts
    outfn = "%s.%s" % (name, ext)
    mrgfn = "%s.mrg.%s" % (name, ext)
    if os.path.exists(outfn):
        echo(outfn, "exists")
        return
    fs = []
    for i in range(cnt):
        fs.append("%s[%02d].%s"% (name, i, ext))

    cmd = ["avconv",
           "-v", "error",
           "-i", "-",
           "-y",
           "-c", "copy",
           mrgfn]
    p = Popen(cmd, stdin=PIPE)
    for f in fs:
        echo("merge", f, "/", cnt)
        try:
            s = None
            fobj = open(f + ".ts", "r+b")
        except IOError:
            smd = ["avconv", 
                   #'-loglevel', #'quiet', "error",
                   "-v", "error",
                   "-i", f,
                   "-c", "copy",
                   "-f", "mpegts",
                   "-bsf", "h264_mp4toannexb",
                   "-"]
            s = Popen(smd, stdout=PIPE)
            fobj = s.stdout
        shutil.copyfileobj(fobj, p.stdin)
        if s:
            s.wait()
            s.stdout.close()
            if s.returncode != 0:
                #echo("s.returncode =", s.returncode)
                raise CalledProcessError(s.returncode, smd)
    p.stdin.close()
    p.wait()
    if p.returncode != 0:
        raise CalledProcessError(p.returncode, cmd)
    os.rename(mrgfn, outfn)

    if clean:
        for f in fs:
            os.remove(f)
            os.remove(f + ".ts")


def usage():
    echo('Usage:', sys.argv[0], "name ext url_num")
    sys.exit(1)


def main():
    if len(sys.argv) != 4:
        usage()
    try:
        i = int(sys.argv[3])
    except:
        usage()
    #merge(sys.argv[1], "mp4", i)
    merge(sys.argv[1], sys.argv[2], i)


if __name__ == '__main__':
    main()
        
    
