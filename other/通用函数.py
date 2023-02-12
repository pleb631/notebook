


def get_kwargs_name(**kwargs):
    prefix = []
    for k, v in kwargs.items():
        if isinstance(v, list):
            v = [str(l) for l in v]
            prefix += v
        else:
            prefix.append(str(v))
    prefix = "_".join(prefix)
    return prefix


def jujge():
    str = "hello world"
    print(str.isalnum()) # 判断所有字符都是数字或者字母
    print(str.isalpha()) # 判断所有字符都是字母
    print(str.isdigit()) # 判断所有字符都是数字
    print(str.islower()) # 判断所有字符都是小写
    print(str.isupper()) # 判断所有字符都是大写
    print(str.istitle()) # 判断所有单词都是首字母大写，像标题
    print(str.isspace()) # 判断所有字符都是空白字符、\t、\n、\r
    