
# -*- coding: utf-8 -*-
"""
RegEx email

> /^((?!\.)[\w-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$/gim;

Just playing with Reg Ex. This to validate emails in following ways



The email couldn't start or finish with a dot

The email shouldn't contain spaces into the string

The email shouldn't contain special chars (<:, *,ecc)

The email could contain dots in the middle of mail address before the @

The email could contain a double doman ( '.de.org' or similar rarity)


"""
try:
    from .regex_plus import auto_regex_replace,auto_regex

except:
    from regex_plus import auto_regex_replace,auto_regex




# email_regex = r"^((?!\.)[\w-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$"
