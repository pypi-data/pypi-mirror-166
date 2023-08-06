
from types import SimpleNamespace

REGEX_DICT={}

# regex_dict['email'] = SimpleNamespace(regex=r"^((?!\.)[\w-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$", description="""aaa https://regex101.com/library/SOgUIV?orderBy=RELEVANCE&search=email""")



REGEX_DICT['email'] = {
    "regex":r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
    "type":"replace",
    "description":"""
        用于替换email
        Just playing with Reg Ex. This to validate emails in following ways

        The email couldn't start or finish with a dot

        The email shouldn't contain spaces into the string

        The email shouldn't contain special chars (<:, *,ecc)

        The email could contain dots in the middle of mail address before the @

        The email could contain a double doman ( '.de.org' or similar rarity)

        https://regex101.com/library/SOgUIV?orderBy=RELEVANCE&search=email""",
    "test":{
        "text":"Here 123@qq.com is our guide on how to 123@qq.com give CBD oil to dogs. Follow us on Twitter @TriBeCa and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
        # ""
    },
    "status": True
    }




REGEX_DICT['email_domain'] = {
    "regex":r" .*@(\S+)",
    "type":"replace",
    "description":"""
    邮箱域名过滤

        https://regex101.com/library/SOgUIV?orderBy=RELEVANCE&search=email""",
    "test":{
        # ""
    },
    "status":False
    }







REGEX_DICT['follow_characters'] = {
    "regex":r'Follow us on (.*?) @(.*?) and @(.*?).\.',
    "type":"replace",
    "description":"""
        删除和移除follow 字符

        """,
    "demo":"sss",
    "test":{
        "text":"Here is our guide on how to give CBD oil to dogs. Follow us on Twitter @TriBeCa and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
        },
    "status": True
    }
# email_regex = r"^((?!\.)[\w-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$"

# print(REGEX_DICT)








"""
模板示例：

REGEX_DICT['key'] ={
    "regex":r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
    "type":"replace",
    "description":"https://regex101.com/library/SOgUIV?orderBy=RELEVANCE&search=email",
    "test":{
        "text":"Here 123@qq.com is our guide on how to 123@qq.com give CBD oil to dogs. Follow us on Twitter @TriBeCa and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
        # ""
    },
    "status": True
    }
"""