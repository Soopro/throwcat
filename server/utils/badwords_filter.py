#coding=utf-8
from __future__ import absolute_import

class DFAFilter():

    """Filter Messages from keywords
    Use DFA to keep algorithm perform constantly
    >>> f = DFAFilter()
    >>> f.add("sexy")
    >>> f.filter("hello sexy baby")
    hello **** baby
    """

    def __init__(self):
        self.keyword_chains = {}
        self.delimit = '\x00'

    def add(self, keyword):
        if not isinstance(keyword, unicode):
            keyword = keyword.decode('utf-8')
        chars = keyword.lower().strip()
        if not chars:
            return
        level = self.keyword_chains
        for i in xrange(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in xrange(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def is_in_english_word(self, message, start, step_ins):
        start_char = message[start]
        if 0x4e00 <= ord(start_char) < 0x9fa6:      # is chinese
            return False
        if start > 0 and (ord(message[start-1]) < 0x4e00 \
        or ord(message[start-1]) >= 0x9fa6) \
        and message[start-1].isalnum():
            return True
        if start + step_ins < len(message) \
        and message[start+step_ins].isalnum() \
        and (ord(message[start+step_ins]) < 0x4e00 \
        or ord(message[start+step_ins]) >= 0x9fa6):
            return True
        return False

    def parse(self, path):
        with open(path) as f:
            for line in f:
                self.add(line.strip())

    def filter(self, message, repl="*"):
        if not isinstance(message, str) and not isinstance(message, unicode):
            return message

        if isinstance(message, str):
            message = message.decode('utf-8')
        content_list = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        if self.is_in_english_word(message, start, step_ins):
                            content_list.append(message[start:start+step_ins])
                            start += step_ins - 1
                            break
                        else:
                            content_list.append(repl * step_ins)
                            start += step_ins - 1
                            break
                else:
                    content_list.append(message[start])
                    break
            else:
                content_list.append(message[start])
            start += 1
        result = ''.join(content_list)

        return unicode(result)

    # def check_legal(self, message, user_id):
    #     if not isinstance(message, unicode):
    #         message = message.decode('utf-8')
    #     message = message.lower()
    #     start = 0
    #     while start < len(message):
    #         level = self.keyword_chains
    #         step_ins = 0
    #         for char in message[start:]:
    #             if char in level:
    #                 step_ins += 1
    #                 if self.delimit not in level[char]:
    #                     level = level[char]
    #                 else:
    #                     return False
    #         start += 1
    #     return True


class BadWordsFilter(object):
    """
    Use Singleton Pattern
    >>> f = BadWordsFilter()
    >>> f.filter("sexy girl")
    *** girl
    >>> f.check_legal("sexy girl")
    False
    """
    
    BADWORDS_FILE = 'badwords.txt'
    
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(BadWordsFilter, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            cls._instance.f = DFAFilter()
            cls._instance.f.parse(cls.BADWORDS_FILE)
        return cls._instance

    def __init__(self, repl='*'):
        self.repl = repl

    def filter(self, content):
        if isinstance(content, dict):
            res = {}
            for k, v in content.iteritems():
                res[k] = self.f.filter(v, self.repl)
            return res
        elif isinstance(content, list):
            res = []
            for item in content:
                res.append(self.f.filter(item, self.repl))
            return res
        else:
            return self.f.filter(content, self.repl)
    #
    # def check_legal(self, content, user_id):
    #     return self.f.check_legal(content, user_id)

