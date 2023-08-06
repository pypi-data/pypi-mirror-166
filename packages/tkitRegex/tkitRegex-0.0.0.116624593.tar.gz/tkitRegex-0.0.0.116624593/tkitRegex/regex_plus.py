# -*- coding: utf-8 -*-

import re
import sys
# from type import List
try:
    from .regex_dict import REGEX_DICT
except ImportError:
    from regex_dict import REGEX_DICT

def auto_test_regex(regexs,my_str):
    """
    用于测试正则使用。

    The auto_test_regex function takes a string and a list of regexs as arguments.
    It then iterates through the list of regexs, running each one against the my_str.
    For each match it prints out information about that match including:
    the index where it was found, what text matched, and which groups were captured.

    :param my_str:str: Used to Pass in the string that you want to test.
    :param regexs=[]: Used to Pass a list of regexs to the function.
    :return: The match object for each regex in the list of regexs.

    :doc-author: Trelent
    """

    for regex in regexs:
        matches = re.finditer(regex, my_str, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):

            print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1

                print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))



def auto_regex(my_str,regexs):
    """
    可以匹配多个正则中的匹配。

    The auto_regex function takes a string and a list of regular expressions as arguments.
    It then iterates through the list of regular expressions, running each one against the test string.
    If there is a match, it returns all matches found in an array along with some other information about the match.
    The auto_regex function was created to help automate parsing text files for data that may be split across multiple lines or sections.

    :param my_str: Used to Pass in a string to search for matches using the regex pattern provided.
    :param regexs: Used to Pass a list of regexs to be tested against the my_str parameter.
    :return: A generator that yields a dictionary with the following keys:.

    :doc-author: Trelent
    """
    """

    """
    for i,item in enumerate(regexs):
        matches = re.finditer(item['regex'], my_str, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            yield {
                "matchNum":matchNum,
                "start" :match.start(),
                "end" :match.end(),
                "match":match.group(),
                "data":match,
                "regex":item['regex'],
                "regex_index":i
            }
def test_auto_regex():
    """Test that auto_regex

    """
    funcName = sys._getframe().f_code.co_name # 获取调用函数名
    print("run function :",funcName)
    regex = r"Follow us on (.*?) @(.*?) and @(.*?)\."

    my_str = "Here is our guide on how to give CBD oil to dogs. Follow us on Twitter @TriBeCa and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
    for it in auto_regex(my_str,[regex]):
        print(it)


def auto_regex_replace(my_str,regexs)->str:
    """
    批量替换模式
    regexs=[
        {
            "regex":r'Follow us on (.*?) @(.*?) and @(.*?).',
            "replace":'\\1'
        }

    ]

    """


    for i,item in enumerate(regexs):
        # print(item)
        my_str = re.sub(item['regex'], item['replace'], my_str)
    return my_str
def test_auto_regex_replace():
    """Test that auto-regex_replace() works correctly

    """
    funcName = sys._getframe().f_code.co_name # 获取调用函数名
    print("run function :",funcName)

    my_str = "Here is our guide on how to give CBD oil to dogs. Follow us on Twitter @TriBeCa and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
    regexs=[
        {
            "regex":r'Follow us on (.*?) @(.*?) and @(.*?).\.',
            "replace":''
        }

    ]
    print(auto_regex_replace(my_str,regexs))

def regex_plus(text,regexs=None,do="replace",test=False):
    """ 自动进行

    do replace match


    """
    # if key is None:
    assert regexs # "regexs must not be None

    new_regexs = []
    for item in regexs:
        if item.get("regex"):
            one ={
                "regex_key":item.get("regex_key"),
                "regex":item.get("regex"),
                "replace":item.get("replace")
                }
        else:
            key=item.get("regex_key")
            one ={
                "regex_key":item.get("regex_key"),
                "regex":REGEX_DICT[key]['regex'],
                "replace":item.get("replace")
                }
        new_regexs.append(one)


    # print(auto_regex_replace(my_str,regexs))
    print("new_regexs",new_regexs)
    if do=="replace":
        return auto_regex_replace(text,new_regexs)
    else:
        return auto_regex(text,new_regexs)

if __name__ == "__main__":
    # test_auto_regex()

    # test_auto_regex_replace()
    regexs=[
        {
            "regex_key":'follow_characters',
            "replace":''
        },
        {
            "regex_key":'email',
            "replace":'your_email_address'
        }
    ]
    text="Here is our guide on how to 123@qq.com give 123@qq.com CBD oil to dogs. Follow us on Twitter @TriBeCa and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
    print("replace:")
    out=regex_plus(text,regexs=regexs,test=True,do="replace")
    print(out)
    print("match:")
    for it in regex_plus(text,regexs=regexs,test=True,do="match"):
        print(it)

