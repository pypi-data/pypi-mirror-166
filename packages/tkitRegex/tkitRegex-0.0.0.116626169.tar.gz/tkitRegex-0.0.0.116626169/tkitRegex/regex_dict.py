
from types import SimpleNamespace
import pregex as px
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

tld = '.' + px.op.Either('com', 'org')
cnn=px.qu.Optional(px.op.Either('https://', 'http://'))+px.qu.Optional('www.')+px.op.Either('cnn', 'CNN', 'Cnn')+tld

pre:px.Pregex=cnn
# pre:px.Pregex="Follow us on "+px.Word()+twitter+" and "+ twitter
# pre
text="Here is our guide on how to 123@qq.com give 123@qq.com CBD oil to dogs. Follow us on Twitter abc@cnn.com and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
# pre.get_matches(text)
cnn=pre.get_pattern()

REGEX_DICT['cnn'] = {
    # "regex":r'Follow us on (.*?) @(.*?) and @(.*?).\.',
    "regex":cnn,
    "type":"replace",
    "description":"""
        过滤cnn网址

        """,
    "demo":"sss",
    "test":{
        "text":"Here is our guide on how to give CBD oil to dogs. Follow us on Twitter @TriBeCa and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
        },
    "status": True
    }


cnn_mail=px.Word()+"@cnn.com"
pre:px.Pregex=cnn_mail
# pre:px.Pregex="Follow us on "+px.Word()+twitter+" and "+ twitter
# pre
text="Here is our guide on how to 123@qq.com give 123@qq.com CBD oil to dogs. Follow us on Twitter abc@cnn.com and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
# pre.get_matches(text)
cnn_mail=pre.get_pattern()

REGEX_DICT['cnn_mail'] = {
    # "regex":r'Follow us on (.*?) @(.*?) and @(.*?).\.',
    "regex":cnn_mail,
    "type":"replace",
    "description":"""
        过滤cnn邮箱

        """,
    "demo":"sss",
    "test":{
        "text":"Here is our guide on how to give CBD oil to dogs. Follow us on Twitter @TriBeCa and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
        },
    "status": True
    }







# follow_characters 生成
twitter=" @"+px.Word()
pre:px.Pregex="Follow"+px.qu.Optional(px.qu.OneOrMore(" "+px.Word())) +twitter +px.qu.Optional(" and"+twitter) +px.qu.Optional(px.qu.OneOrMore(" "+px.Word()))+px.cl.AnyPunctuation()
# pre:px.Pregex="Follow us on "+px.Word()+twitter+" and "+ twitter
# pre
text="Here is our guide on how to 123@qq.com give 123@qq.com CBD oil to dogs. Follow us on Twitter @TriBeCa and @TriBeCaDog. Follow us on Facebook @TriBeCa and @TriBeCaDog."
# pre.get_matches(text)
follow_characters=pre.get_pattern()

REGEX_DICT['follow_characters'] = {
    # "regex":r'Follow us on (.*?) @(.*?) and @(.*?).\.',
    "regex":follow_characters,
    "type":"replace",
    "description":"""
        删除和移除follow 字符

        """,
    "demo":"sss",
    "test":{
        "text":"Other helpful accessories include web harnesses designed to be used with service dog vests. When owners have sight or mobility issues, it is especially important to make sure the dog is always securely leashed. High-Performance Service & Therapy Dog Vest / Cape with Pockets. Use the weekly Newsquiz to test your knowledge of stories you saw on CNN.com. Buy Patch, Diabetic Alert, Service Dog. Read More. Follow us on Twitter @TribeLive. Read more. Buy Patch, Please Don't Pet Me - For Service Dogs. For Service Dogs. Buy Patch, Please Don’t Pet Me - Follow us on Twitter @TributesToThe and @wqwq.  Follow us on Twitter @TributesToThe Crate. Follow our Instagram @TributestoThe Crate. "
        },
    "status": True
    }
# email_regex = r"^((?!\.)[\w-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$"

# print(REGEX_DICT)




# date             = re.compile('(?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)|(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)(?:\,)?\s*(?:\d{4})?|[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4}', re.IGNORECASE)
# time             = re.compile('\d{1,2}:\d{2} ?(?:[ap]\.?m\.?)?|\d[ap]\.?m\.?', re.IGNORECASE)
# phone            = re.compile('''((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))''')
# phones_with_exts = re.compile('((?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*(?:[2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|(?:[2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?(?:[2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?(?:[0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(?:\d+)?))', re.IGNORECASE)
# link             = re.compile('(?i)((?:https?://|www\d{0,3}[.])?[a-z0-9.\-]+[.](?:(?:international)|(?:construction)|(?:contractors)|(?:enterprises)|(?:photography)|(?:immobilien)|(?:management)|(?:technology)|(?:directory)|(?:education)|(?:equipment)|(?:institute)|(?:marketing)|(?:solutions)|(?:builders)|(?:clothing)|(?:computer)|(?:democrat)|(?:diamonds)|(?:graphics)|(?:holdings)|(?:lighting)|(?:plumbing)|(?:training)|(?:ventures)|(?:academy)|(?:careers)|(?:company)|(?:domains)|(?:florist)|(?:gallery)|(?:guitars)|(?:holiday)|(?:kitchen)|(?:recipes)|(?:shiksha)|(?:singles)|(?:support)|(?:systems)|(?:agency)|(?:berlin)|(?:camera)|(?:center)|(?:coffee)|(?:estate)|(?:kaufen)|(?:luxury)|(?:monash)|(?:museum)|(?:photos)|(?:repair)|(?:social)|(?:tattoo)|(?:travel)|(?:viajes)|(?:voyage)|(?:build)|(?:cheap)|(?:codes)|(?:dance)|(?:email)|(?:glass)|(?:house)|(?:ninja)|(?:photo)|(?:shoes)|(?:solar)|(?:today)|(?:aero)|(?:arpa)|(?:asia)|(?:bike)|(?:buzz)|(?:camp)|(?:club)|(?:coop)|(?:farm)|(?:gift)|(?:guru)|(?:info)|(?:jobs)|(?:kiwi)|(?:land)|(?:limo)|(?:link)|(?:menu)|(?:mobi)|(?:moda)|(?:name)|(?:pics)|(?:pink)|(?:post)|(?:rich)|(?:ruhr)|(?:sexy)|(?:tips)|(?:wang)|(?:wien)|(?:zone)|(?:biz)|(?:cab)|(?:cat)|(?:ceo)|(?:com)|(?:edu)|(?:gov)|(?:int)|(?:mil)|(?:net)|(?:onl)|(?:org)|(?:pro)|(?:red)|(?:tel)|(?:uno)|(?:xxx)|(?:ac)|(?:ad)|(?:ae)|(?:af)|(?:ag)|(?:ai)|(?:al)|(?:am)|(?:an)|(?:ao)|(?:aq)|(?:ar)|(?:as)|(?:at)|(?:au)|(?:aw)|(?:ax)|(?:az)|(?:ba)|(?:bb)|(?:bd)|(?:be)|(?:bf)|(?:bg)|(?:bh)|(?:bi)|(?:bj)|(?:bm)|(?:bn)|(?:bo)|(?:br)|(?:bs)|(?:bt)|(?:bv)|(?:bw)|(?:by)|(?:bz)|(?:ca)|(?:cc)|(?:cd)|(?:cf)|(?:cg)|(?:ch)|(?:ci)|(?:ck)|(?:cl)|(?:cm)|(?:cn)|(?:co)|(?:cr)|(?:cu)|(?:cv)|(?:cw)|(?:cx)|(?:cy)|(?:cz)|(?:de)|(?:dj)|(?:dk)|(?:dm)|(?:do)|(?:dz)|(?:ec)|(?:ee)|(?:eg)|(?:er)|(?:es)|(?:et)|(?:eu)|(?:fi)|(?:fj)|(?:fk)|(?:fm)|(?:fo)|(?:fr)|(?:ga)|(?:gb)|(?:gd)|(?:ge)|(?:gf)|(?:gg)|(?:gh)|(?:gi)|(?:gl)|(?:gm)|(?:gn)|(?:gp)|(?:gq)|(?:gr)|(?:gs)|(?:gt)|(?:gu)|(?:gw)|(?:gy)|(?:hk)|(?:hm)|(?:hn)|(?:hr)|(?:ht)|(?:hu)|(?:id)|(?:ie)|(?:il)|(?:im)|(?:in)|(?:io)|(?:iq)|(?:ir)|(?:is)|(?:it)|(?:je)|(?:jm)|(?:jo)|(?:jp)|(?:ke)|(?:kg)|(?:kh)|(?:ki)|(?:km)|(?:kn)|(?:kp)|(?:kr)|(?:kw)|(?:ky)|(?:kz)|(?:la)|(?:lb)|(?:lc)|(?:li)|(?:lk)|(?:lr)|(?:ls)|(?:lt)|(?:lu)|(?:lv)|(?:ly)|(?:ma)|(?:mc)|(?:md)|(?:me)|(?:mg)|(?:mh)|(?:mk)|(?:ml)|(?:mm)|(?:mn)|(?:mo)|(?:mp)|(?:mq)|(?:mr)|(?:ms)|(?:mt)|(?:mu)|(?:mv)|(?:mw)|(?:mx)|(?:my)|(?:mz)|(?:na)|(?:nc)|(?:ne)|(?:nf)|(?:ng)|(?:ni)|(?:nl)|(?:no)|(?:np)|(?:nr)|(?:nu)|(?:nz)|(?:om)|(?:pa)|(?:pe)|(?:pf)|(?:pg)|(?:ph)|(?:pk)|(?:pl)|(?:pm)|(?:pn)|(?:pr)|(?:ps)|(?:pt)|(?:pw)|(?:py)|(?:qa)|(?:re)|(?:ro)|(?:rs)|(?:ru)|(?:rw)|(?:sa)|(?:sb)|(?:sc)|(?:sd)|(?:se)|(?:sg)|(?:sh)|(?:si)|(?:sj)|(?:sk)|(?:sl)|(?:sm)|(?:sn)|(?:so)|(?:sr)|(?:st)|(?:su)|(?:sv)|(?:sx)|(?:sy)|(?:sz)|(?:tc)|(?:td)|(?:tf)|(?:tg)|(?:th)|(?:tj)|(?:tk)|(?:tl)|(?:tm)|(?:tn)|(?:to)|(?:tp)|(?:tr)|(?:tt)|(?:tv)|(?:tw)|(?:tz)|(?:ua)|(?:ug)|(?:uk)|(?:us)|(?:uy)|(?:uz)|(?:va)|(?:vc)|(?:ve)|(?:vg)|(?:vi)|(?:vn)|(?:vu)|(?:wf)|(?:ws)|(?:ye)|(?:yt)|(?:za)|(?:zm)|(?:zw))(?:/[^\s()<>]+[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019])?)', re.IGNORECASE)
# email            = re.compile("([a-z0-9!#$%&'*+\/=?^_`{|.}~-]+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)", re.IGNORECASE)
# ip               = re.compile('(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', re.IGNORECASE)
# ipv6             = re.compile('\s*(?!.*::.*::)(?:(?!:)|:(?=:))(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)){6}(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)[0-9a-f]{0,4}(?:(?<=::)|(?<!:)|(?<=:)(?<!::):)|(?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)){3})\s*', re.VERBOSE|re.IGNORECASE|re.DOTALL)
# price            = re.compile('[$]\s?[+-]?[0-9]{1,3}(?:(?:,?[0-9]{3}))*(?:\.[0-9]{1,2})?')
# hex_color        = re.compile('(#(?:[0-9a-fA-F]{8})|#(?:[0-9a-fA-F]{3}){1,2})\\b')
# credit_card      = re.compile('((?:(?:\\d{4}[- ]?){3}\\d{4}|\\d{15,16}))(?![\\d])')
# btc_address      = re.compile('(?<![a-km-zA-HJ-NP-Z0-9])[13][a-km-zA-HJ-NP-Z0-9]{26,33}(?![a-km-zA-HJ-NP-Z0-9])')
# street_address   = re.compile('\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|park|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)', re.IGNORECASE)
# zip_code         = re.compile(r'\b\d{5}(?:[-\s]\d{4})?\b')
# po_box           = re.compile(r'P\.? ?O\.? Box \d+', re.IGNORECASE)
# ssn              = re.compile('(?!000|666|333)0*(?:[0-6][0-9][0-9]|[0-7][0-6][0-9]|[0-7][0-7][0-2])[- ](?!00)[0-9]{2}[- ](?!0000)[0-9]{4}')

# regexes = {
#   "dates"            : date,
#   "times"            : time,
#   "phones"           : phone,
#   "phones_with_exts" : phones_with_exts,
#   "links"            : link,
#   "emails"           : email,
#   "ips"              : ip,
#   "ipv6s"            : ipv6,
#   "prices"           : price,
#   "hex_colors"       : hex_color,
#   "credit_cards"     : credit_card,
#   "btc_addresses"    : btc_address,
#   "street_addresses" : street_address,
#   "zip_codes"        : zip_code,
#   "po_boxes"         : po_box,
#   "ssn_number"       : ssn
# }



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