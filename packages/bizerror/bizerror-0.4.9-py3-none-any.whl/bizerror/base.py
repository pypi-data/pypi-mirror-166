# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
import json

LANGUAGE = "zh-hans"

ERROR_INFO = {
    "en": {},
    "zh-hans": {}
}

def clean_language_name(language):
    if language is None:
        return LANGUAGE
    else:
        return language.lower().strip().replace("_", "-")

def set_language(language):
    global LANGUAGE
    language = clean_language_name(language)
    LANGUAGE = language

def get_language():
    return LANGUAGE

def set_error_info(language, class_name, code, message):
    language = clean_language_name(language)
    if not language in ERROR_INFO:
        ERROR_INFO[language] = {}
    ERROR_INFO[language][class_name] = {
        "code": code,
        "message": message,
    }

def get_error_info(class_name, language=None):
    language = clean_language_name(language)
    return ERROR_INFO[language][class_name]

class classproperty(property):
    """Subclass property to make classmethod properties possible"""
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

class BizErrorBase(RuntimeError):
    """Base class of all errors.
    """

    def __init__(self, message=None, code=None, **kwargs):
        if isinstance(message, BizErrorBase): # 从BizErrorBase构造新的BizError，直接复制其code和message
            code = code or message.code
            message = message.message
        elif isinstance(message, dict): # 从{code: xx, message: xxx}字典构造新的BizError，直接复制期code/message字段值
            code = code or message.get("code", -1)
            message = message.get("message", str(message))
        elif isinstance(message, Exception): # 从python内置异常类构造新的BizError，根据系统内置code映射表设置code
            error = message
            code = 0
            message = None
            if len(error.args) >= 2: # 如果内置异常遵循(code, message)参数形式构建，则尝试提取其code和message
                try:
                    code = int(error.args[0])
                    message = error.args[1:]
                    if len(message) == 1:
                        message = message[0]
                except Exception:
                    pass
            if not code: # 如果提取失败，则根据异常类名提取code
                code = SYSTEM_ERROR_CODE_MAPPING.get(error.__class__.__name__, 0)
            info = get_error_info(self.__class__.__name__)
            if not code:
                code = info["code"]
            if not message:
                message = str(error)
            if not message:
                message = info["message"]
            if not isinstance(message, str):
                message = str(message)
        else:
            # load default code & message
            info = get_error_info(self.__class__.__name__)
            code = code or info["code"]
            message = message or info["message"]
            # message format
            if not isinstance(message, str):
                message = str(message)
        if kwargs:
            message = message.format(**kwargs)
        super().__init__(code, message)

    def __repr__(self):
        return str(self)

    def __str__(self):
        result = json.dumps({
            "code": self.args[0],
            "message": self.args[1]
        }, ensure_ascii=False)
        return result

    def update(self, **kwargs):
        self.args = (self.args[0], self.args[1].format(**kwargs))

    @property
    def code(self):
        return self.args[0]

    @property
    def message(self):
        return self.args[1]

    @property
    def json(self):
        return {
            "code": self.code,
            "message": self.message,
        }


class OK(BizErrorBase):
    pass
set_error_info("en", "OK", 0, "OK")
set_error_info("zh-hans", "OK", 0, "正常。")

class BizError(BizErrorBase):
    pass
set_error_info("en", "BizError", 1, "Error")
set_error_info("zh-hans", "BizError", 1, "异常！")

SYSTEM_ERROR_CODE_MAPPING = {
    'ArithmeticError': 102,
    'AssertionError': 104,
    'AttributeError': 106,
    'BaseException': 108,
    'BlockingIOError': 110,
    'BrokenPipeError': 112,
    'BufferError': 114,
    'BytesWarning': 116,
    'ChildProcessError': 118,
    'ConnectionAbortedError': 120,
    'ConnectionError': 122,
    'ConnectionRefusedError': 124,
    'ConnectionResetError': 126,
    'DeprecationWarning': 128,
    'EOFError': 130,
    'EncodingWarning': 132,
    'Exception': 134,
    'FileExistsError': 136,
    'FileNotFoundError': 138,
    'FloatingPointError': 140,
    'FutureWarning': 142,
    'GeneratorExit': 144,
    'ImportError': 146,
    'ImportWarning': 148,
    'IndentationError': 150,
    'IndexError': 152,
    'InterruptedError': 154,
    'IsADirectoryError': 156,
    'KeyError': 158,
    'KeyboardInterrupt': 160,
    'LookupError': 162,
    'MemoryError': 164,
    'ModuleNotFoundError': 166,
    'NameError': 168,
    'NotADirectoryError': 170,
    'NotImplementedError': 172,
    'OSError': 174,
    'OverflowError': 176,
    'PendingDeprecationWarning': 178,
    'PermissionError': 180,
    'ProcessLookupError': 182,
    'RecursionError': 184,
    'ReferenceError': 186,
    'ResourceWarning': 188,
    'RuntimeError': 190,
    'RuntimeWarning': 192,
    'StopAsyncIteration': 194,
    'StopIteration': 196,
    'SyntaxError': 198,
    'SyntaxWarning': 200,
    'SystemError': 202,
    'SystemExit': 204,
    'TabError': 206,
    'TimeoutError': 208,
    'TypeError': 210,
    'UnboundLocalError': 212,
    'UnicodeDecodeError': 214,
    'UnicodeEncodeError': 216,
    'UnicodeError': 218,
    'UnicodeTranslateError': 220,
    'UnicodeWarning': 222,
    'UserWarning': 224,
    'ValueError': 226,
    'Warning': 228,
    'ZeroDivisionError': 230,
}