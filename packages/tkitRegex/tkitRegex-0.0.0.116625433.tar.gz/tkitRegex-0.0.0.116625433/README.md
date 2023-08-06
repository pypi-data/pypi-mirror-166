# tkit-regex-tools
tkit regex tools 正则合集


```bash
pip install tkitRegex

# or
pip install git+https://github.com/napoler/tkit-regex-tools
```


```python
from tkitRegex import regex_plus
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


```

示例使用：
https://github.com/napoler/tkit-regex-tools/blob/main/test.ipynb



推荐文档

https://github.com/manoss96/pregex
https://github.com/napoler/pregex
https://pregex.rtfd.io/