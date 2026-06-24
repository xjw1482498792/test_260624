if  __name__ == "__main__":
    print("Hello, World!")


def print_name(name: str):
    print(f"Hello, {name}!")

import re

_ERROR_SIGNATURE_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"timeout"),        "网络超时"),
    (re.compile(r"permission"),     "权限错误"),
    (re.compile(r"\d{3} error"),    "HTTP 错误"),
]

tup1 = ((1,1), 2, 3)   
print([ tmp for tmp in tup1]) 