# python 3.10.5
# Time    : 2022/09/07
# Author  : Shadow403
# Email   : 
# File    : group_request.py
# Software: Visual Studio Code

# 粉丝牌审核

import json,time, requests
from nonebot import on_request, logger
from nonebot.adapters.onebot.v11 import Bot, GroupRequestEvent

# 审核
group_req = on_request(priority=1, block=False)

@group_req.handle()
async def gr_(bot: Bot, event: GroupRequestEvent):
    # Main_Program
    if event.group_id == <群号>:
        raw = json.loads(event.json())
        gid = str(event.group_id)
        uid = str(event.user_id)
        flag = raw['flag']
        logger.info('flag:', str(flag))
        sub_type = raw['sub_type']
        comment = raw['comment']
        BiliUID = ''.join(filter(str.isdigit,comment))
        cookies = {"cookie": "<你的cookie>"}
        url_main = ('https://api.live.bilibili.com/xlive/web-ucenter/user/MedalWall?target_id=' + BiliUID)# <- API
        response = requests.get(url_main, cookies = cookies)
        response = response.text
        time.sleep(7)
        # 同意入群
        if '<粉丝牌子名>' in response:
                logger.info(f"同意{uid}加入群 {gid},验证消息为 “{comment}”")
                await bot.set_group_add_request(
                    flag=flag,
                    sub_type=sub_type,
                    approve=True,
                    reason=' ',
                )
        # 拒绝入群
        if '<粉丝牌子名>' not in response:
            logger.info(f"拒绝{uid}加入群 {gid},验证消息为 “{comment}”")
            await bot.set_group_add_request(
                flag=flag,
                sub_type=sub_type,
                approve=False,
                reason='未获得粉丝牌或未打开展示设置',
            )
