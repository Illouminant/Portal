#!/usr/bin/python3

from logging import StringTemplateStyle
import discord
import json
import asyncio
import random
import os
import psutil
import traceback
import time
import datetime
import re
import numpy as np

intents = discord.Intents.default()
intents.members = True
portal = discord.Client(intents=intents)

owners = [530781444742578188, 521926078403575814, 201548633244565504]

discord_token = None
with open("auth.json", "r") as f:
    data = json.load(f)
    discord_token = data["token"]

_print = print
def print(*args, sep=" ", end="\n"):
    embed = discord.Embed(colour=discord.Colour(3214259))
    embed.description = "```" + str(sep).join(str(i) for i in args) + end + "```"
    asyncio.create_task(portal.get_channel(798861277043884082).send(embed=embed))
    return _print(*args)

def has_username(content, words, user, *aliases):
    if user:
        for name in (n.lower() for n in (user.name, user.display_name) + aliases):
            if name:
                if " " in name:
                    if name in content:
                        return True
                else:
                    if name in words:
                        return True

def exclusive_range(range, *excluded):
	ex = frozenset(excluded)
	return tuple(i for i in range if i not in ex)

ZeroEnc = "\xad\u061c\u180e\u200b\u200c\u200d\u200e\u200f\u2060\u2061\u2062\u2063\u2064\u2065\u2066\u2067\u2068\u2069\u206a\u206b\u206c\u206d\u206e\u206f\ufe0f\ufeff"

UNIFMTS = [
	"𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙",
	"𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩",
	"𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵",
	"𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ",
	"0123456789𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ",
	"0123456789𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅",
	"０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ",
	"⓪①②③④⑤⑥⑦⑧⑨🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉",
	"⓿➊➋➌➍➎➏➐➑➒🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉",
	"⓪①②③④⑤⑥⑦⑧⑨ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ",
	"⓿➊➋➌➍➎➏➐➑➒🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩",
	"0123456789𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡",
	"𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕",
	"𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉",
	"₀₁₂₃₄₅₆₇₈₉ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖqʳˢᵗᵘᵛʷˣʸᶻ🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿",
	"0123456789ᗩᗷᑢᕲᘿᖴᘜᕼᓰᒚҠᒪᘻᘉᓍᕵᕴᖇSᖶᑘᐺᘺ᙭ᖻᗱᗩᗷᑕᗪᗴᖴǤᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ",
	"0ƖᘔƐᔭ59Ɫ86ɐqɔpǝɟɓɥᴉſʞןɯuodbɹsʇnʌʍxʎzꓯᗺƆᗡƎℲ⅁HIſꓘ⅂WNOԀΌᴚS⊥∩ΛMX⅄Z",
	"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
]
__umap = {UNIFMTS[k][i]: UNIFMTS[-1][i] for k in range(len(UNIFMTS) - 1) for i in range(len(UNIFMTS[k]))}

__unfont = "".maketrans(__umap)
unfont = lambda s: str(s).translate(__unfont)

DIACRITICS = {
	"ÀÁÂÃÄÅĀĂĄ": "A",
	"Æ": "AE",
	"ÇĆĈĊČ": "C",
	"ĎĐ": "D",
	"ÈÉÊËĒĔĖĘĚ": "E",
	"ĜĞĠĢ": "G",
	"ĤĦ": "H",
	"ÌÍÎÏĨĪĬĮİ": "I",
	"Ĳ": "IJ",
	"Ĵ": "J",
	"Ķ": "K",
	"ĹĻĽĿŁ": "L",
	"ÑŃŅŇŊ": "N",
	"ÒÓÔÕÖØŌŎŐ": "O",
	"Œ": "OE",
	"ŔŖŘ": "R",
	"ŚŜŞŠ": "S",
	"ŢŤŦ": "T",
	"ÙÚÛÜŨŪŬŮŰŲ": "U",
	"Ŵ": "W",
	"ÝŶŸ": "Y",
	"ŹŻŽ": "Z",
	"àáâãäåāăą": "a",
	"æ": "ae",
	"çćĉċč": "c",
	"ďđ": "d",
	"èéêëðēĕėęě": "e",
	"ĝğġģ": "g",
	"ĥħ": "h",
	"ìíîïĩīĭįı": "i",
	"ĳ": "ij",
	"ĵ": "j",
	"ķĸ": "k",
	"ĺļľŀł": "l",
	"ñńņňŉŋ": "n",
	"òóôõöøōŏő": "o",
	"œ": "oe",
	"þ": "p",
	"ŕŗř": "r",
	"śŝşšſ": "s",
	"ß": "ss",
	"ţťŧ": "t",
	"ùúûüũūŭůűų": "u",
	"ŵ": "w",
	"ýÿŷ": "y",
	"źżž": "z"
}
for i, k in DIACRITICS.items():
	__umap.update({c: k for c in i})
__umap.update({c: "" for c in ZeroEnc})
__umap["\u200a"] = ""
for c in tuple(__umap):
	if c in UNIFMTS[-1]:
		__umap.pop(c)
__trans = "".maketrans(__umap)
extra_zalgos = (
	range(768, 880),
	range(1155, 1162),
	exclusive_range(range(1425, 1478), 1470, 1472, 1475),
	range(1552, 1560),
	range(1619, 1632),
	exclusive_range(range(1750, 1774), 1757, 1758, 1765, 1766, 1769),
	exclusive_range(range(2260, 2304), 2274),
	range(7616, 7627),
	(8432,),
	range(11744, 11776),
	(42607,), range(42612, 42622), (42654, 42655),
	range(65056, 65060)
)
zalgo_array = np.concatenate(extra_zalgos)
zalgo_map = {n: "" for n in zalgo_array}
__trans.update(zalgo_map)
__unitrans = ["".maketrans({UNIFMTS[-1][x]: UNIFMTS[i][x] for x in range(len(UNIFMTS[-1]))}) for i in range(len(UNIFMTS) - 1)]

def uni_str(s, fmt=0):
	if type(s) is not str:
		s = str(s)
	return s.translate(__unitrans[fmt])

def unicode_prune(s):
	if type(s) is not str:
		s = str(s)
	if s.isascii():
		return s
	return s.translate(__trans)

__qmap = {
	"“": '"',
	"”": '"',
	"„": '"',
	"‘": "'",
	"’": "'",
	"‚": "'",
	"〝": '"',
	"〞": '"',
	"⸌": "'",
	"⸍": "'",
	"⸢": "'",
	"⸣": "'",
	"⸤": "'",
	"⸥": "'"
}
__qtrans = "".maketrans(__qmap)

full_prune = lambda s: unicode_prune(s).translate(__qtrans).casefold()

def fuzzy_substring(sub, s, match_start=False, match_length=True):
    if not match_length and s in sub:
        return 1
    if sub.startswith(s):
        return len(s) / len(sub) * 2
    match = 0
    if not match_start or sub and s.startswith(sub[0]):
        found = [0] * len(s)
        x = 0
        for i, c in enumerate(sub):
            temp = s[x:]
            if temp.startswith(c):
                if found[x] < 1:
                    match += 1
                    found[x] = 1
                x += 1
            elif c in temp:
                y = temp.index(c)
                x += y
                if found[x] < 1:
                    found[x] = 1
                    match += 1 - y / len(s)
                x += 1
            else:
                temp = s[:x]
                if c in temp:
                    y = temp.rindex(c)
                    if found[y] < 1:
                        match += 1 - (x - y) / len(s)
                        found[y] = 1
                    x = y + 1
        if len(sub) > len(s) and match_length:
            match *= len(s) / len(sub)
    ratio = max(0, match / len(s))
    return ratio

def fetch_member_ex(guild, strings, ratio=0.75):
    highest = ratio
    target = None
    if isinstance(strings, str):
        strings = [strings]
    for string in strings:
        string = full_prune(string)
        for user in guild.members:
            name = full_prune(user.name)
            ratio = fuzzy_substring(name, string, match_start=True, match_length=True)
            if ratio >= highest:
                highest = ratio
                target = user
            if user.nick:
                name = full_prune(user.nick)
                ratio = fuzzy_substring(name, string, match_start=True, match_length=True)
                if ratio > highest:
                    highest = ratio
                    target = user
    return target

portal_activity = 0
portal_day = 0
complain_day = random.randint(3, 5)

@portal.event
async def on_ready():
    await portal.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name="God and consuming frogs. 🐸"))
    print("Successfully loaded.")

portal_emotes = [
    "<:Sassy:522184015109947392>",
    "<:Portalsshattyface:594330735976906772>",
    "<:Dilated:552316387188801546>",
    "<:YesIwillkissyou:598732002987868179>",
    ""
]

@portal.event
async def on_message(message):
    global portal_activity
    try:
        content = message.content
        channel = message.channel
        guild = message.guild
        user = message.author
        mentions = (f"<@{portal.user.id}>", f"<@!{portal.user.id}>")

        if message.author.id == portal.user.id:
            if "798861277043884082" in str(channel.id) or str(channel.id) != "522227579520942090":
                return
            portal_activity += 1
            return

        if content in mentions:
            if message.guild is None:
                print(f"{user.name} @ me in DM's.")
            else:
                print(f"{user.name} @ me in {message.guild}.")

            respond = [
                f"{user.mention}",
                f"What do you want, {user.mention}?!",
                "Why don't you ping <@239631525350604801>, he was the nuisance before me.",
                "What?",
                "Why did you ping me?",
                "Can I help you with something?",
                "If you're confused on how to use me, just ping me and ask something.",
                "Leave me alone and don't ping me.",
                "Eff off.",
                "Excuse me? I'm busy thinking about how Infinite murdered me.",
                "I may be a robot, but your pings get on my nerves."
            ]

            if guild is not None:
                respond.append(f"Could you go bother {random.choice(message.guild.members).name} instead?")
            else:
                respond.append(f"Could you go bother someone in a server instead?")

            stinky_foot = asyncio.create_task(portal.wait_for("message", check=lambda message: message.channel.id == channel.id))
            await channel.trigger_typing()
            await asyncio.sleep(2)
            if stinky_foot.done():
                return await channel.send(f"{random.choice(respond)} {random.choice(portal_emotes)}",  reference=message, allowed_mentions=discord.AllowedMentions(replied_user=False))
            else:
                return await channel.send(f"{random.choice(respond)} {random.choice(portal_emotes)}")

        if guild is None or channel.id == 522227579520942090 or any(mention in content for mention in mentions):
            for mention in mentions:
                if content.startswith(mention):
                    content = content[len(mention):]
                    break
            content = content.strip()
            if user.id in owners:
                command = globals().get(content.lower())
                if callable(command):
                    return await command(channel=channel)

            if not content.endswith("?"):
                if channel.id == 522227579520942090:
                    return
                stinky_foot = asyncio.create_task(portal.wait_for("message", check=lambda message: message.channel.id == channel.id))
                await channel.trigger_typing()
                await asyncio.sleep(2)
                if stinky_foot.done():
                    return await channel.send("I'm coded to answer questions. Please put a question mark at the end.",  reference=message, allowed_mentions=discord.AllowedMentions(replied_user=False))
                else:
                    return await channel.send("I'm coded to answer questions. Please put a question mark at the end.")

            if message.guild is None:
                print(f"{user.name} has asked \"{content}\" in Direct Messages.")
            else:
                print(f"{user.name} has asked \"{content}\" in {message.guild}.")

            opposite_responses = [
                "Do you have anything better to do with your time?",
                "Are you a robot too?",
                "Do you take care of yourself?",
                "Divide by zero.",
                "Are you going to pester me all day long?",
                f"""{"".join(y for x in zip(content[::2].lower(), content[1::2].upper()) for y in x if y)}?"""
            ]

            if set(content) == {"?"}:
                responses = [
                    "Do you think I'm that stupid?",
                    "Ask an actual question.",
                    "Congratulations, you can post a question mark."
                ]

                stinky_foot = asyncio.create_task(portal.wait_for("message", check=lambda message: message.channel.id == channel.id))
                await channel.trigger_typing()
                await asyncio.sleep(2)
                if stinky_foot.done():
                    return await channel.send(f"{random.choice(responses)} {random.choice(portal_emotes)}",  reference=message, allowed_mentions=discord.AllowedMentions(replied_user=False))
                else:
                    return await channel.send(f"{random.choice(responses)} {random.choice(portal_emotes)}")
                
            if content != "?":
                content = content.lower().strip("?").strip(mention)
                words = re.sub(r"\W+", " ", content).split()
                responses = []
                target = None

                if guild is not None:
                    if any(i in words for i in ("who", "whose", "who's")):
                        responses = [
                            f"Who? Have you thought of {random.choice(message.guild.members).display_name}?",
                            f"I'm pretty sure that would be {random.choice(message.guild.members).displ}.",
                            f"I think {random.choice(message.guild.members).name} might know. They seem suspicious."
                        ]
                    
                    target = fetch_member_ex(guild, words)
                    if target and target.id != portal.user.id:
                        responses = [
                            f"Oh, {target.name}?",
                            f"What about {target.name}?",
                            f"I like {target.name} too much to speak out about them.",
                            f"I'm not in the mood to address {target.name} right now.",
                            f"They upset me last {random.choice(['hour', 'week', 'month', 'year', 'decade', 'lifetime'])}.",
                            "Hmm, I'd say they are in my good books.",
                            "Yes, what about them?",
                            "Oh, them? They're kinda cool.",
                            "I have no interest in even bringing their name up in my RAM.",
                            "Do you have issues with them that you want to address or something?",
                            "Do you two have unresolved conflicts? Why are you asking me?",
                            "I'm not your therapy bot, talk to them yourself.",
                            "Ask them how they're doing every once in a while."
                        ]

                        if target.id == 521926078403575814:
                            responses.extend([
                                "Oh, her? That bitch has such an ego, it makes me look like a street beggar.",
                                "What about my mommy?",
                                "Don't mention  *M Y  M O M*  to me.",
                                "Ivory? She actually adopted me. Can't say I'm very close to her."
                            ])

                        elif target.id == 156865912631197696:
                            responses.extend([
                                "Yuck, Zei...",
                                "What about my mom's loser husband?",
                                "Oh, Zei? Yeah, he's about my height, weighs less than me, and has lesbian hair.",
                                "I'm appauled that you mention such a man in front of me."
                            ])

                        elif target.id == 263469402865926144:
                            responses.extend([
                                "Chry? Oh, that sword-loving, helmet-faced schnitzel?"
                            ])

                        elif target.id == 435245956665966633:
                            responses.extend([
                                "Nobody knows this, but... When he was a child, he aspired to be a cultist leader.",
                                "Huh? Repeat that again? I lost you at \"Fliss is cool\".",
                                "Oh, Fliss. Cool guy, I guess."
                            ])

                        elif target.id == 530781444742578188:
                            responses.extend([
                                "Hmph, Smudge? She programmed me. Says I'm her favorite program. Pretty cool, I guess.",
                                "Smudge? She wants me to remind you that my AI isn't Egghead level. \"Don't take anything Portal says seriously\", or whatever.",
                                "I guess I wouldn't exist without her. I probably shouldn't be disrespectful for my own sake."
                            ])

                        elif target.id == 201548633244565504:
                            responses.extend([
                                "Hm, Txin? He helped out with my code quite a lot. *Smudge knows* I wouldn't be as fabulous without him.",
                                "What about my creator's loser boyfriend?",
                                "Oh, that guy? Pretty smart, I guess."
                            ])

                if responses:
                    pass

                elif content == "portal":
                    responses = [
                        f"{message.author.display_name}.",
                        "Yes, that is my name.",
                        "What do you want, an award for reading my name?",
                        "Yes?",
                        "Same.",
                        "Never heard of that guy. Maybe you mean \"absolute legendary god far above you on any scale.\"",
                        "What?",
                        "Why did you say my name?",
                        "Can I help you with something?",
                        "If you're confused on how to use me, just ping me and ask something.",
                        "Eff off.",
                        "Excuse me? I'm busy thinking about how Infinite murdered me."
                    ]

                elif any(i in words for i in ("sassy", "rude", "mean")) and "portal" in words:
                    responses = [
                        f"Because {portal.get_user(530781444742578188).name} programmed me this way.",
                        f"Blame {portal.get_user(521926078403575814).name}' parenting.",
                        f"Blame {portal.get_user(263469402865926144).name} for bringing me in to this world.",
                        "Why not?",
                        "Pssh, like you'd understand.",
                        "Because I'm a Barbie girl.",
                        "Because I'm fabulous."
                    ]

                elif any(i in words for i in ("hi", "hello", "hey", "sup")):
                    responses = [
                        f"Hello, {message.author.display_name}.",
                        f"Hi, {message.author.display_name}. I am lonely in here, so it's nice for *some* company.",
                        f"Do you need something? I'm enjoying the peace and quiet since {portal.get_user(668999031359537205).name} and {portal.get_user(737992099449929728).name} moved out.",
                        f"Hello. Here's a question for you, \"{random.choice(opposite_responses).lower()}\"",
                        "What do you want?",
                        "... Hi?",
                        "Hi.",
                        "Hello.",
                        "I'm busy brooding over Infinite murdering me, what do you want?"
                    ]

                elif any(i in words for i in ("bye", "goodbye", "cya")):
                    responses = [
                        f"Bye, {message.author.display_name}.",
                        f"Time to go another {str(random.randint(1, 21))} days of uptime where nobody will talk to me.",
                        "Bye, whatever.",
                        "See you around.",
                        "Finally, thought you'd never leave.",
                        "'Later.",
                        "Goodbye I guess...?",
                        "Why leave now? I'm bored.",
                        "Cool, see you later."
                    ]

                elif any(i in words for i in ("many", "number", "long", "rate")):
                    responses = [
                        f"{random.randint(-2147483647, 2147483648)}.",
                        f"{random.randint(1, 51)}.",
                        f"{random.randint(1, 10001)}."
                    ]

                    if "long" in words:
                        responses = [response[:-1] + "m." for response in responses]
                    elif "rate" in words:
                        responses = [response[:-1] + "%" for response in responses]

                elif "when" in words:
                    responses = [
                        f"In the year {random.randint(2021, 10001)}.",
                        f"In {random.randint(3, 11)} minutes.",
                        f"Wait {random.randint(5, 11)} hours.",
                        "Why would I know?",
                        "Tomorrow.",
                        "In a million years.",
                        "Frankly, I don't care when.",
                        "I don't know, whenever you want it to happen.",
                        "Didn't that happen yesterday?",
                        "Never.",
                        "How about an hour?",
                        "Maybe tomorrow?",
                        "Try next week, h u n n y.",
                        "When you can count all of your toes and fingers.",
                        "I dunno.",
                        "Go without food for a while and when you finally feel hungry, do whatever that is."
                    ]

                elif any(i in words for i in ("who", "whose", "who's")):
                    responses = [
                        f"Your {random.choice(['therapist', 'doctor', 'parent', 'sibling', 'friend'])}.",
                        "Who?",
                        "Why should I know?",
                        "Do you expect me to know them?"
                        "You.",
                        "Me.",
                        "Do I look like I care who?",
                        "Who cares? Infinite murdered me.",
                        "I refuse to answer that.",
                        "I have been instructed not to tell you who."
                    ]

                elif any(i in words for i in ("why", "is", "how", "are", "was", "you", "you're", "yours")):
                    responses = [
                        "I don't really care.",
                        "You're asking ME?",
                        "I refuse to answer.",
                        "Oh my Solaris, I think I need brain bleach.",
                        "Meh.",
                        "Wouldn't know. Check Google."
                    ]

                elif any(i in words for i in ("would", "can", "does", "should", "do", "have")):
                    responses = [
                        "Hell yes.",
                        "Sure, whatever.",
                        "No. Just no.",
                        "Do what you want to.",
                        "Maybe the day pigs fly.",
                        "Obviously, you bass turd.",
                        "Psh, please.",
                        "No, seriously.",
                        "Are you a sadist?",
                        "I guess.",
                        "Why does that even matter?",
                        "Uhhh, can I have a cookie instead?",
                        "My answer is that of an innocent man about to be accused of guilt. No."
                    ]

                elif "help" in words:
                    responses = [
                        f"You actually going to say what you want help with, {message.author.display_name}?",
                        f"How about you help me by answering this question: {random.choice(opposite_responses)}",
                        "Help what?",
                        "Literally all you have to do is ask me a question. Are you so pea-brained you can't figure that out?",
                        "Help yourself.",
                        "No.",
                        "How about no.",
                        "Sure.",
                        "How about being more clear about what you need help with.",
                        "I ain't helping no scrub.",
                        "I'm a free robot! **I'm not obligated to helping you.**"
                    ]

                else:
                    responses = [
                        "I'm sorry.",
                        "I'm not sorry.",
                        "Interesting.",
                        "Atheists.",
                        "Screw you.",
                        "Instead of wasting your time pestering me, you should try drinking some organic oil.",
                        "I think you should run.",
                        "Come back with some soup and then maybe I'll speak to you.",
                        "DERE'S A SNAKE IN MAH BOOT!",
                        "You know what matters more? The fact that Infinite murdered me.",
                        "That makes me so sad.",
                        "What is WRONG with you?!",
                        "Try screaming first.",
                        "Sorry, I can't think right now. I had too many frogs earlier.",
                        "Linkin Park - Hit the Floor.",
                        "Why would you bring that up?"
                    ]

                if not target and all(i not in words for i in ("who", "whose", "who's", "when", "bye", "goodbye", "hi", "hello", "many", "number", "long", "rate", "help")):
                    responses.extend([
                        f"How about I ask you a question: {random.choice(opposite_responses)}",
                        "Yes.",
                        "No.",
                        "Oh... Yes.",
                        "Uuuhhhmmm... Yes?",
                        "Er, that's a yes.",
                        "Mhm.",
                        "Definitely, yes.",
                        "I believe so.",
                        "Psh, no. I ain't your therapist.",
                        "What? No.",
                        "That is... A big nope.",
                        "I vote no.",
                        "Impossible.",
                        "Uhhh..."
                    ])

                    if guild is not None:
                        responses.append(f"Ask {random.choice(message.guild.members).display_name}.")
                    else:
                        responses.append("Ask someone in a server.")

                stinky_foot = asyncio.create_task(portal.wait_for("message", check=lambda message: message.channel.id == channel.id))
                await channel.trigger_typing()
                await asyncio.sleep(2)
                if stinky_foot.done():
                    await channel.send(f"{random.choice(responses)} {random.choice(portal_emotes)}", reference=message, allowed_mentions=discord.AllowedMentions(replied_user=False))
                else:
                    await channel.send(f"{random.choice(responses)} {random.choice(portal_emotes)}")
    except:
        print(traceback.format_exc(), end="")

async def log_update():
    global portal_day, portal_activity, complain_day
    await portal.wait_until_ready()
    start_time = time.time()
    current_day = str(datetime.datetime.utcnow().date())
    while not portal.is_closed():
        try:
            globals()["eloop"] = asyncio.get_event_loop()
            uptime = datetime.timedelta(seconds=time.time() - start_time)
            new_day = str(time.time() // 86400)
            if new_day != current_day:
                current_day = new_day
                portal_day += 1
                if portal_activity > 0:
                    portal_day = 0
                    complain_day = random.randint(3, 5)
                print(f"🔹 Current Uptime: {str(uptime).rsplit('.', 1)[0]}")
                print(f"🔹 Palace Activity: {portal_activity} | 🔸 Days Towards Complaint: {portal_day} | 🔹 Complain Day: {complain_day}")
                if portal_activity == 0:
                    if portal_day >= complain_day:
                        channel = portal.get_channel(522227579520942090)
                        portal_complaint = [
                            f"Hello? It's been {portal_day} days since someone last spoke to me. I'm bored.",
                            f"So am I just going to keep sitting around waiting for another {portal_day} days?",
                            f"*Very deliberately and rudely yawns in it's been {portal_day} days.*",
                            f"It's been {portal_day} days. {random.choice(channel.guild.members).mention}, talk to me.",
                            "My bolts are getting rusty here all alone. Please talk to me.",
                            "All because I'm a robot doesn't mean I can't get bored you know."
                        ]
                        asyncio.create_task(channel.send(random.choice(portal_complaint)))
                        await asyncio.sleep(1)
                        portal_activity = 0
                        portal_day = 0
                        complain_day = random.randint(3, 5)
                else:
                    portal_activity = 0
        except Exception as e:
            print(e)
        await asyncio.sleep(1)
portal.loop.create_task(log_update())

async def restart(channel, **void):
    await channel.send("`Restarting...` <:DieOnEggmanBattleShip:522176911418327041>")
    await portal.change_presence(status=discord.Status.offline)
    os.system("start cmd /c python main.py")
    psutil.Process().kill()

async def shutdown(channel, **void):
    await channel.send("`Shutting down...` <:PensiveSonic:731227000219369512>")
    await portal.change_presence(status=discord.Status.offline)
    psutil.Process().kill()

portal.run(discord_token)
