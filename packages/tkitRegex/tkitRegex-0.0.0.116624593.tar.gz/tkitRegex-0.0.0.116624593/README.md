# tkit-regex-tools
tkit regex tools 正则合集





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