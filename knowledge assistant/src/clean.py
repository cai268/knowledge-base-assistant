import re

# 脏数据处理函数
def clear_data(respond:str):
    lines = respond.split('\n')
    keep_lines = []
    for line in lines:
        if any(kw in line for kw in ['邮购电话', '质量投诉', '盗版侵权', 
            '咨询联系方式', '版权所有', '翻印必究',
            '联系及邮购','邮箱']):
            continue
        keep_lines.append(line)
    respond = '\n'.join(keep_lines)

    # 删除qq号、qq群号：
    pattern=r'(?:QQ|qq)[\u4e00-\u9fa5]*\s*[: ：]\s*[1-9]\d{3,12}'
    respond = re.sub(pattern, '', respond, flags=re.IGNORECASE)
    # 删除页数，章数
    pattern=r'[第]\s*\d+\s*[页|章|版]'
    respond = re.sub(pattern, '', respond, flags=re.IGNORECASE)
    # 删除邮箱
    pattern=r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    respond = re.sub(pattern, '', respond, flags=re.IGNORECASE)
    # 删除空白
    respond = re.sub(r'\s+', ' ', respond)

    respond = respond.strip()
    # respond = ''.join(respond)
    return respond