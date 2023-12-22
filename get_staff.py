import json
import requests
import sys
import os
import re
from time import sleep

def get_from(link: str, count=10) -> str:
    link_status: int
    for i in range(count):
        reply = requests.get(link)
        link_status = reply.status_code
        if reply.status_code in range(200, 300):
            return reply.text
        sleep(1)
    print(f"Status {link_status}:", link)
    sys.exit(os.EX_UNAVAILABLE)

teachers = {}
template = "https://ssau.ru/staff?page={0}&letter=0"

raw = get_from("https://ssau.ru/staff").replace('\n', ' ')
page_max = max(map(int, re.findall(r"(?<=page=)\d+", raw)))
for i in range(page_max):
    tmp_raw = get_from(template.format(i+1)).replace('\n', ' ')
    tmp_info = re.findall(r"https://ssau.ru/staff/\d+.*?(?=</a>)", tmp_raw)
    for j in tmp_info:
        tmp = re.sub("-.+>", "", j)
        tmp = re.sub(r".*/", "", tmp).strip().split(" ", 1)
        teachers[tmp[1]] = tmp[0]

with open("staff.json", "w") as f:
    json.dump(teachers, f, indent=4, ensure_ascii=False, sort_keys=True)
