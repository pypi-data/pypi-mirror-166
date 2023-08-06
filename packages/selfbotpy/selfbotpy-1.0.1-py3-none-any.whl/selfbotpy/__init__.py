import fortnitepy
import json
from termcolor import colored
import os 
from fortnitepy.ext import commands
import aioconsole
from functools import partial
import logging
import FortniteAPIAsync
import asyncio
from typing import Optional
import aiohttp
from discord import Webhook
from discord.ext import commands as discord
import discord as disc
fortnite_api = FortniteAPIAsync.APIClient()

with open('Settings.json') as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(colored("มีข้อผิดพลาดในไฟล์ใดไฟล์หนึ่งของบอท!(Settings.json) หากคุณมีปัญหาในการพยายามแก้ไขให้เข้าร่วมเซิร์ฟเวอร์สนับสนุนความไม่ลงรอยกันเพื่อขอความช่วยเหลือ - https://discord.gg/Xqm7DaSCES", "red"))
        exit(1)



server = None
if data['Discord']['Webhook'] == "":
    filename = 'device_auths.json'
else: 
    webhook = Webhook.from_url(data['Discord']['Webhook'], session=aiohttp.ClientSession())
    filename = 'device_auths.json'



def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(Email, details):
    existing = get_device_auth_details()
    existing[Email] = details


    with open(filename, 'w') as fp:
        json.dump(existing, fp)

def is_admin():
    async def predicate(ctx):
        return ctx.author.id in data['Control']['Give full access to']
    return commands.check(predicate)

async def get_authorization_code():
    while True:
        response = await aioconsole.ainput("นี่เป็นเหตุการณ์ที่เกิดขึ้นครั้งเดียว! ลุยเลย https://rebrand.ly/authcode และลงชื่อเข้าใช้เป็น "  + data['Account']['Email'] + "แล้วป้อนคําตอบ: ")
        if "redirectUrl" in response:
            response = json.loads(response)
            if "?code" not in response["redirectUrl"]:
                print(colored("การตอบสนองที่ไม่ถูกต้อง.", "red"))
                continue
            code = response["redirectUrl"].split("?code=")[1]
            return code
        else:
            if "https://accounts.epicgames.com/fnauth" in response:
                if "?code" not in response:
                    print(colored("การตอบสนองที่ไม่ถูกต้อง.", "red"))
                    continue
                code = response.split("?code=")[1]
                return code
            else:
                code = response
                return code

device_auth_details = get_device_auth_details().get(data['Account']['Email'], {})
client = discord.Bot(
    command_prefix=data['Discord']['Prefix'],
    case_insensitive=True,
    intents=disc.Intents.all()
)

bot = commands.Bot(
    command_prefix=data['Account']['Prefix'],case_insensitive=True,
    auth=fortnitepy.AdvancedAuth(
        Email=data['Account']['Email'],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        authorization_code=get_authorization_code,
        **device_auth_details
    ),
    status=data['Party']['Status'],
    platform=fortnitepy.Platform(data['Party']['Platform']),
)

@bot.event
async def event_device_auth_generate(details, Email):
    store_device_auth_details(data['Account']['Email'], details)




@bot.event
async def event_ready():
    
    print(colored(f'''
----------------
บอทเริ่มต้นแล้ว.
ชื่อผู้ใช้บอท: {bot.user.display_name}
รหัสผู้ใช้บอท: {bot.user.id}
แท่น: {(str((bot.platform))[9:]).lower().capitalize()}
----------------
    ''', 'green'))
    if data['Discord']['Webhook'] == "":
        pass
    else:
        await webhook.send(f'''
    ----------------
    บอทเริ่มต้นแล้ว.
    ชื่อผู้ใช้บอท: {bot.user.display_name}
    รหัสผู้ใช้บอท: {bot.user.id}
    แท่น: {(str((bot.platform))[9:]).lower().capitalize()}
    ----------------
    ''', username = "terminal")
    member = bot.party.me
    

    await member.edit_and_keep(
        partial(
            fortnitepy.ClientPartyMember.set_outfit,
            asset=data['Party']['Cosmetics']['Skin']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_backpack,
            asset=data['Party']['Cosmetics']['Backpack']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_pickaxe,
            asset=data['Party']['Cosmetics']['Pickaxe']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_emote,
            asset=data['Party']['Cosmetics']['Emote']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=data['Party']['Cosmetics']['Banner']['Banner Name'],
            color=data['Party']['Cosmetics']['Banner']['Banner Color'],
            season_level=data['Party']['Cosmetics']['Banner']['Season Level']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=data['Party']['Cosmetics']['Banner']['battle pass tier']
        )
    )
    if data['Discord']['Token'] == "":
        return
    else:
        await client.start(data['Discord']['Token'])
   

@bot.event
async def event_friend_message(message):
    if data['Discord']['Webhook'] == "":
        pass
    else: 
        await webhook.send(f"กระซิบ: {message.content}", username = "Chat Logs")
@bot.event
async def event_party_message(message):
    if data['Discord']['Webhook'] == "":
        pass
    else:
        await webhook.send(f"แชทปาร์ตี้: {message.content}", username = "Chat Logs")

@bot.event
async def event_friend_add(Friend):
    if not data['Control']['Public Bot']:
        if not Friend.id in data['Control']['Give full access to']:
            return
    
    try:
        await Friend.invite()
    except:
        pass




    

@bot.event
async def event_party_invite(invite):
    if data['Party']['Join party on invitation'].lower() == 'true':
        try:
            await invite.accept()
            print(colored(f'ตอบรับคําเชิญจากพรรค {invite.sender.display_name}', 'blue'))
        except Exception:
            pass
    elif data['Party']['Join party on invitation'].lower() == 'false':
        if invite.sender.id in data['Control']['Give full access to']:
            await invite.accept()
            print(colored(f'ตอบรับคําเชิญจากพรรค {invite.sender.display_name}', 'blue'))
        else:
            print(colored(f'ไม่เคยตอบรับคําเชิญจากพรรค {invite.sender.display_name}', 'red'))
def lenFriends():
    friends = bot.friends
    return len(friends)

def lenPartyMembers():
    members = bot.party.members
    return len(members)
    
@bot.event
async def event_party_member_promote(old_leader, new_leader):
    if new_leader.id == bot.user.id:
        await bot.party.send(f"ขอบคุณ {old_leader.display_name} สําหรับการโปรโมตฉัน ♥")
        await bot.party.me.set_emote("EID_TrueLove")


@bot.event
async def event_friend_request(request):
    if data['Friends']['Accept all friend requests'].lower() == 'true':
        try:
            await request.accept()
            print(colored(f'คําขอเป็นเพื่อนที่ยอมรับจาก {request.display_name}' + f' ({lenFriends()})', 'blue'))
        
        except Exception:
            pass
    elif data['Friends']['Accept all friend requests'].lower() == 'false':
        if request.id in data['Control']['Give full access to']:
            try:
                await request.accept()
                print(colored(f'คําขอเป็นเพื่อนที่ยอมรับจาก {request.display_name}' + f' ({lenFriends()})', 'blue'))
            except Exception:
                pass
        else:
            print(colored(f'ไม่เคยยอมรับคําขอเป็นเพื่อนจาก {request.display_name}', 'red'))
@bot.event
async def event_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'นั่นไม่ใช่คําสั่ง ลอง !help')
    elif isinstance(error, IndexError):
        pass
    elif isinstance(error, fortnitepy.HTTPException):
        pass
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("คุณไม่มีสิทธิ์เข้าถึงคําสั่งนั้น")
    elif isinstance(error, TimeoutError):
        await ctx.send("คุณใช้เวลานานเกินไปที่จะตอบสนอง!")
    else:
        print(error)


@bot.command()
@is_admin()
async def unhide(ctx, *,user = None) -> None:
    user = await bot.fetch_profile(user)
    member = bot.party.get_member(user.id)
    if member.hidden is False:
        await ctx.send("ผู้ใช้ถูก unhidden แล้ว")
        return
    await bot.party.set_squad_assignments({member: fortnitepy.SquadAssignment(hidden=False)})
    await ctx.send(f"ผู้ใช้ {member.display_name} ได้รับการ unhidden")


@bot.command()
async def emote(ctx, *, content = None):
    if content is None:
        await ctx.send(f'ไม่ได้รับอิโมติคอนลอง: !emote (ชื่ออิโมติคอน)')
    elif content.lower() == 'floss':
        await bot.party.me.clear_emote()
        await bot.party.me.set_emote(asset='EID_Floss')
        await ctx.send(f'อิโมติคอนตั้งค่าเป็น: Floss')
    elif content.lower() == 'none':
        await bot.party.me.clear_emote()
        await ctx.send(f'อิโมติคอนตั้งค่าเป็น: None')
    elif content.upper().startswith('EID_'):
        await bot.party.me.clear_emote()
        await bot.party.me.set_emote(asset=content.upper())
        await ctx.send(f'อิโมติคอนตั้งค่าเป็น: {content}')
    else:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await bot.party.me.clear_emote()
            await bot.party.me.set_emote(asset=cosmetic.id)
            await ctx.send(f'อิโมติคอนตั้งค่าเป็น: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'ไม่พบอิโมติคอนที่ชื่อ: {content}')


@bot.command()
@is_admin()
async def promote(ctx, *, epic_username: Optional[str] = None) -> None:
    if epic_username is None:
        user = await bot.fetch_user(ctx.author.display_name)
        member = bot.party.get_member(user.id)
    else:
        user = await bot.fetch_user(epic_username)
        member = bot.party.get_member(user.id)

    if member is None:
        await ctx.send("ไม่พบผู้ใช้รายนั้นคุณแน่ใจหรือว่าพวกเขาอยู่ในปาร์ตี้?")
    else:
        try:
            await member.promote()
            await ctx.send(f"ผู้ใช้ที่โปรโมต: {member.display_name}")
            print(colored(f"ผู้ใช้ที่โปรโมท: {member.display_name}", "blue"))
        except fortnitepy.errors.Forbidden:
            await ctx.send(f"ล้มเหลวในการโปรโมต {member.display_name} เนื่องจากฉันไม่ใช่หัวหน้าพรรค")
            print(colored("ไม่สามารถเลื่อนตําแหน่งสมาชิกได้เนื่องจากฉันไม่มีสิทธิ์ที่จําเป็น", "blue"))


@bot.command()
@is_admin()
async def hide(ctx, *, user = None):
    user = await bot.fetch_profile(user)
    member = bot.party.get_member(user.id)
    if member.hidden is True:
        await ctx.send("ผู้ใช้ถูกซ่อนไว้แล้ว")
        return
    await bot.party.set_squad_assignments({member: fortnitepy.SquadAssignment(hidden=True)})
    await ctx.send(f"ผู้ใช้ {member.display_name} ถูกซ่อนไว้")


@bot.command()
async def pinkghoul(ctx):
    variants = bot.party.me.create_variants(material=3)

    await bot.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=variants
    )

    await ctx.send('ตั้งค่าผิวเป็น: Pink Ghoul Trooper')


@bot.command()
async def purpleskull(ctx):
    variants = bot.party.me.create_variants(clothing_color=1)

    await bot.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants = variants
    )

    await ctx.send('ตั้งค่าผิวเป็น: Purple Skull Trooper')





@bot.command()
async def goldpeely(ctx):
    variants = bot.party.me.create_variants(progressive=4)

    await bot.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('ตั้งค่าผิวเป็น: Golden Peely')


@bot.command()
async def hatlessrecon(ctx):
    variants = bot.party.me.create_variants(parts=2)

    await bot.party.me.set_outfit(
        asset='CID_022_Athena_Commando_F',
        variants=variants
    )

    await ctx.send('ตั้งค่าผิวเป็น: Hatless Recon Expert')



@bot.command()
async def hologram(ctx):
    await bot.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )
    
    await ctx.send("ตั้งค่าผิวเป็น: Hologram")






@bot.command()
async def ready(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send('พร้อม!')



@bot.command()
async def unready(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('ไม่ได้!')



@bot.command()
async def skin(ctx, *, content = None):
    if content is None:
        await ctx.send(f'ไม่มีผิวได้รับ, ลอง : !skin (ชื่อสกิน)')
    elif content.upper().startswith('CID_'):
        await bot.party.me.set_outfit(asset=content.upper())
        await ctx.send(f'ผิวตั้งไว้ที่: {content}')
    else:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await bot.party.me.set_outfit(asset=cosmetic.id)
            await ctx.send(f'ผิวตั้งไว้ที่: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'ไม่พบสกินที่ชื่อ: {content}')


@bot.command()
async def sitin(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('นั่งอยู่ใน')


@bot.command()
async def sitout(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await ctx.send('นั่งออก')


@bot.command()
async def tier(ctx, tier = None):
    if tier is None:
        await ctx.send(f'ไม่มีการจัดระดับชั้น ลอง: !tier (หมายเลขระดับ)') 
    else:
        await bot.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )

        await ctx.send(f'ระดับบัตรผ่านการรบที่ตั้งค่าเป็น: {tier}')


@bot.command()
async def level(ctx, level = None):
    if level is None:
        await ctx.send(f'ไม่มีระดับใดที่ได้รับ ลอง: !level (ตัวเลข)')
    else:
        await bot.party.me.set_banner(season_level=level)
        await ctx.send(f'ตั้งค่าระดับเป็น: {level}')


#discord

@client.command()
@commands.is_owner()
async def unhide(ctx, *,user = None) -> None:
    user = await bot.fetch_profile(user)
    member = bot.party.get_member(user.id)
    if member.hidden is False:
        await ctx.send("ผู้ใช้ถูก unhidden แล้ว")
        return
    await bot.party.set_squad_assignments({member: fortnitepy.SquadAssignment(hidden=False)})
    await ctx.send(f"ผู้ใช้ {member.display_name} ได้รับการ unhidden")


@client.command()
async def emote(ctx, *, content = None):
    if content is None:
        await ctx.send(f'ไม่ได้รับอิโมติคอนลอง: !emote (ชื่ออิโมติคอน)')
    elif content.lower() == 'floss':
        await bot.party.me.clear_emote()
        await bot.party.me.set_emote(asset='EID_Floss')
        await ctx.send(f'อิโมติคอนตั้งค่าเป็น: Floss')
    elif content.lower() == 'none':
        await bot.party.me.clear_emote()
        await ctx.send(f'อิโมติคอนตั้งค่าเป็น: None')
    elif content.upper().startswith('EID_'):
        await bot.party.me.clear_emote()
        await bot.party.me.set_emote(asset=content.upper())
        await ctx.send(f'อิโมติคอนตั้งค่าเป็น: {content}')
    else:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await bot.party.me.clear_emote()
            await bot.party.me.set_emote(asset=cosmetic.id)
            await ctx.send(f'อิโมติคอนตั้งค่าเป็น: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'ไม่พบอิโมติคอนที่ชื่อ: {content}')


@client.command()
@commands.is_owner()
async def promote(ctx, *, epic_username: Optional[str] = None) -> None:
    if epic_username is None:
        user = await bot.fetch_user(ctx.author.display_name)
        member = bot.party.get_member(user.id)
    else:
        user = await bot.fetch_user(epic_username)
        member = bot.party.get_member(user.id)

    if member is None:
        await ctx.send("ไม่พบผู้ใช้รายนั้นคุณแน่ใจหรือว่าพวกเขาอยู่ในปาร์ตี้?")
    else:
        try:
            await member.promote()
            await ctx.send(f"ผู้ใช้ที่โปรโมต: {member.display_name}")
            print(colored(f"ผู้ใช้ที่โปรโมท: {member.display_name}", "blue"))
        except fortnitepy.errors.Forbidden:
            await ctx.send(f"ล้มเหลวในการโปรโมต {member.display_name} เนื่องจากฉันไม่ใช่หัวหน้าพรรค")
            print(colored("ไม่สามารถเลื่อนตําแหน่งสมาชิกได้เนื่องจากฉันไม่มีสิทธิ์ที่จําเป็น", "blue"))


@client.command()
@commands.is_owner()
async def hide(ctx, *, user = None):
    user = await bot.fetch_profile(user)
    member = bot.party.get_member(user.id)
    if member.hidden is True:
        await ctx.send("ผู้ใช้ถูกซ่อนไว้แล้ว")
        return
    await bot.party.set_squad_assignments({member: fortnitepy.SquadAssignment(hidden=True)})
    await ctx.send(f"ผู้ใช้ {member.display_name} ถูกซ่อนไว้")


@client.command()
async def pinkghoul(ctx):
    variants = bot.party.me.create_variants(material=3)

    await bot.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=variants
    )

    await ctx.send('ตั้งค่าผิวเป็น: Pink Ghoul Trooper')


@client.command()
async def purpleskull(ctx):
    variants = bot.party.me.create_variants(clothing_color=1)

    await bot.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants = variants
    )

    await ctx.send('ตั้งค่าผิวเป็น: Purple Skull Trooper')





@client.command()
async def goldpeely(ctx):
    variants = bot.party.me.create_variants(progressive=4)

    await bot.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('ตั้งค่าผิวเป็น: Golden Peely')


@client.command()
async def hatlessrecon(ctx):
    variants = bot.party.me.create_variants(parts=2)

    await bot.party.me.set_outfit(
        asset='CID_022_Athena_Commando_F',
        variants=variants
    )

    await ctx.send('ตั้งค่าผิวเป็น: Hatless Recon Expert')



@client.command()
async def hologram(ctx):
    await bot.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )
    
    await ctx.send("ตั้งค่าผิวเป็น: Hologram")






@client.command()
async def ready(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send('พร้อม!')



@client.command()
async def unready(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('ไม่ได้!')



@client.command()
async def skin(ctx, *, content = None):
    if content is None:
        await ctx.send(f'ไม่มีผิวได้รับ, ลอง : !skin (ชื่อสกิน)')
    elif content.upper().startswith('CID_'):
        await bot.party.me.set_outfit(asset=content.upper())
        await ctx.send(f'ผิวตั้งไว้ที่: {content}')
    else:
        try:
            cosmetic = await fortnite_api.cosmetics.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await bot.party.me.set_outfit(asset=cosmetic.id)
            await ctx.send(f'ผิวตั้งไว้ที่: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'ไม่พบสกินที่ชื่อ: {content}')


@client.command()
async def sitin(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('นั่งอยู่ใน')


@client.command()
async def sitout(ctx):
    await bot.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await ctx.send('นั่งออก')


@client.command()
async def tier(ctx, tier = None):
    if tier is None:
        await ctx.send(f'ไม่มีการจัดระดับชั้น ลอง: !tier (หมายเลขระดับ)') 
    else:
        await bot.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )

        await ctx.send(f'ระดับบัตรผ่านการรบที่ตั้งค่าเป็น: {tier}')


@client.command()
async def level(ctx, level = None):
    if level is None:
        await ctx.send(f'ไม่มีระดับใดที่ได้รับ ลอง: !level (ตัวเลข)')
    else:
        await bot.party.me.set_banner(season_level=level)
        await ctx.send(f'ตั้งค่าระดับเป็น: {level}')




bot.run()