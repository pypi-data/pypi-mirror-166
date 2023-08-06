# -*- coding: utf-8 -*-
"""
移除文字中的冗余垃圾信息

"""
try:
    from .regex_plus import auto_regex_replace,auto_regex
except:
    from regex_plus import auto_regex_replace,auto_regex

def remove_follow_characters(my_str):
    """移除文本中的follow广告

    """
    # my_str = "Here is our guide on how to give CBD oil to dogs. Follow us on Twitter @TriBeCa and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
    regexs=[
        {
            "regex":r'Follow us on (.*?) @(.*?) and @(.*?).\.',
            "replace":''
        }

    ]
    # print(auto_regex_replace(my_str,regexs))
    return auto_regex_replace(my_str,regexs)

def test_remove_follow_characters():
    my_str = "Here is our guide on how to give CBD oil to dogs. Follow us on Twitter @TriBeCa and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
    print(remove_follow_characters(my_str))

if __name__ == "__main__":
    test_remove_follow_characters()