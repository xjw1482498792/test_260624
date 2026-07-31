from datetime import datetime


def _preview(text: str | None, limit: int = 200) -> str:
    if not text:
        return ""
    text = text.replace("\n", " ").strip()
    return text if len(text) <= limit else text[:limit] + "..."

str1 = """
          第一行：内容。
          第二行，内容。
        """
str2 = "    第一行：内容。\n" + "第二行，内容。"
str3 = "第一行：内容。"        "第二行，内容。"
str4 = ("第一行：内容。" 
        "第二行，内容。")

str5 = "-".join(str(num) for num in range(100))

# print(str1)
# print(str2)
# print(str3)
# print(str4)
print(str5)
print(len(str5))
print(_preview(str5))
print(len(_preview(str5)))

print(len("\n"))


#时间
date1 = datetime.now().isoformat(sep = " ",timespec="minutes")
# date1 = datetime.now().isoformat(sep = " ",timespec="seconds")
date2 = datetime.now().isoformat()
print(date1)
print(date2)