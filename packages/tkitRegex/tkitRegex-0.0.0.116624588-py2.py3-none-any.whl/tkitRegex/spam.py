# -*- coding: utf-8 -*-
"""
移除文字中的冗余垃圾信息

"""
try:
    from .regex_plus import auto_regex_replace,auto_regex
    from .regex_dict import REGEX_DICT
except:
    from regex_plus import auto_regex_replace,auto_regex
    from regex_dict import REGEX_DICT
def remove_follow_characters(text=None,test=False):
    """移除文本中的follow广告

    """
    # my_str = "Here is our guide on how to give CBD oil to dogs. Follow us on Twitter @TriBeCa and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."

    reg=REGEX_DICT['follow_characters']
    if test:
        text=REGEX_DICT['follow_characters']['test']['text']
    regexs=[
        {
            "regex":reg['regex'],
            "replace":''
        }

    ]

    # print(auto_regex_replace(my_str,regexs))
    return auto_regex_replace(text,regexs)

# def test_remove_follow_characters():
#     my_str = REGEX_DICT['follow_characters']['test']['content']
#     print(remove_follow_characters(my_str))

if __name__ == "__main__":
    out=remove_follow_characters(test=True)
    print(out)