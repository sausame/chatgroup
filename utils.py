# Utils

import os
import re
import sys
import subprocess
import threading
import time
import traceback

def getchar():
    sys.stdin.read(1)

def toVisibleAscll(src):

    if None == src or 0 == len(src):
        return src

    if unicode != type(src):
        try:
            src = unicode(src, errors='ignore')
        except TypeError, e: 
            print 'Unable to translate {!r} of type {}'.format(src, type(src)), ':', e

    dest = ''

    for char in src:
        if char < unichr(32): continue
        dest += char

    return dest

def runProcess(cmd, onlyFirstLine=True):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    if onlyFirstLine:
        ret = p.wait()
        if 0 != ret: raise IndexError, 'Unable to run "{}"'.format(cmd)
        for line in p.stdout.readlines():
            return line.rstrip('\r').rstrip('\n')
    else:
        return p.stdout.read()

# update property of name to value
def updateProperty(path, name, value):
    fp = None
    targetLine = None
    newLine = None
    try:
        fp = open(path)
        minlen = len(name) + 1
        for line in fp:
            if len(line) < minlen or '#' == line[0]:
                continue
            group = line.strip().split('=')
            if 2 != len(group) or group[0].strip() != name:
                continue
            if group[1] == value:
                return None
            else:
                targetLine = line
                newLine = '{}={}\r\n'.format(name,value)
                break
    except IOError:
        pass
    finally:
        if fp != None: fp.close()

    if targetLine != None and newLine != None:
        with open(path) as fp:
            content = fp.read()

        content = content.replace(targetLine, newLine)

        with open(path, 'w') as fp:
            fp.write(content)

    return None

def getProperty(path, name):

    fp = None

    try:
        fp = open(path)

        minlen = len(name) + 1

        for line in fp:
            if len(line) < minlen or '#' == line[0]:
                continue

            line = line.strip()
            pos = line.find('=')

            if pos < 0:
                continue

            if line[:pos] != name:
                continue

            return line[pos+1:].strip()

    except IOError:
        pass

    finally:
        if fp != None: fp.close()

    return None

def safePop(obj, name, defaultValue=None):

    try:
        return obj.pop(name)
    except KeyError:
        pass

    return defaultValue

def getMatchString(content, pattern):

    matches = re.findall(pattern, content)

    if matches is None or 0 == len(matches):
        return None

    return matches[0]

def dump(obj):

    def dumpObj(obj):

        fields = ['    {}={}'.format(k, v)
            for k, v in obj.__dict__.items() if not k.startswith('_')]

        return ' {}:\n{}'.format(obj.__class__.__name__, '\n'.join(fields))

    if obj is None: return None

    if type(obj) is list:

        for subObj in obj:
            dump(subObj)
    else:
        print dumpObj(obj)

class AutoReleaseThread(threading.Thread):

    def __init__(self):

        self.isInitialized = False

        self.running = True
        threading.Thread.__init__(self)

        self.mutex = threading.Lock()

    def initialize(self):

        try:
            self.mutex.acquire()

            if not self.isInitialized:

                self.isInitialized = True

                self.onInitialized()

            self.accessTime = time.time()

        except KeyboardInterrupt:
            raise KeyboardInterrupt

        finally:
            self.mutex.release()

    def release(self):

        self.isInitialized = False

        self.onReleased()

    def run(self):

        threadname = threading.currentThread().getName()

        while self.running:

            self.mutex.acquire()

            if self.isInitialized:

                diff = time.time() - self.accessTime

                if diff > 30: # 30 seconds
                    self.release()

            self.mutex.release()

            time.sleep(1)

        else:
            self.release()

        print 'Quit'

    def quit(self):

        print 'Stopping ...'
        self.running = False

class ThreadWritableObject(threading.Thread):

    def __init__(self, configFile, clientVersion='', build=''):

        threading.Thread.__init__(self)

        self.running = True

        outputPath = getProperty(configFile, 'output-path')

        if '' != clientVersion:

            if '' != build:
                outputPath = os.path.join(outputPath, '{}-{}'.format(clientVersion, build))
            else:
                outputPath = os.path.join(outputPath, '{}'.format(clientVersion))

            if not os.path.exists(outputPath):
                os.mkdir(outputPath, 0755)

        self.path = os.path.join(outputPath, 'sys.log')
        self.contents = []

        self.mutex = threading.Lock()

    def write(self, content):

        self.mutex.acquire()

        self.contents.append(content)

        self.mutex.release()

    def run(self):

        def output(path, contents):

            with open(path, 'a') as fp:

                for content in contents:
                    fp.write(content)

        threadname = threading.currentThread().getName()

        while self.running:

            self.mutex.acquire()

            if 0 != len(self.contents):

                MAX_SIZE = 2*1024*1024

                if os.path.exists(self.path) and os.stat(self.path).st_size > MAX_SIZE:

                    os.rename(self.path, '{}.old'.format(self.path))

                output(self.path, self.contents)

                del self.contents[:]

            self.mutex.release()

            time.sleep(10)

        else:
            output(self.path, self.contents)

    def quit(self):

        print 'Quit ...'
        self.running = False


