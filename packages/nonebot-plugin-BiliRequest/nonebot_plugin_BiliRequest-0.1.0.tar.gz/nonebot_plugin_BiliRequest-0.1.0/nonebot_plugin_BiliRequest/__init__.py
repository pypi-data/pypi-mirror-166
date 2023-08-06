# python 3.10.5
# Time    : 2022/09/07
# Author  : Shadow403
# Email   : anonymous_hax@foxmail.com
# File    : group_request.py
# Software: Visual Studio Code

# 关注审核

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
        url_main = ('https://api.bilibili.com/x/relation/followings?vmid=' + BiliUID + '&pn=1&ps=50&order=desc&order_type=attention')# <- API
        response = requests.get(url_main)
        response = response.text
        time.sleep(7)
        # 同意入群
        if '<主播UID>' in response:
                logger.info(f"同意{uid}加入群 {gid},验证消息为 “{comment}”")
                await bot.set_group_add_request(
                    flag=flag,
                    sub_type=sub_type,
                    approve=True,
                    reason=' ',
                )
        # 隐私设置，拒绝入群
        if '用户已设置隐私，无法查看' in response :
                logger.info(f"同意{uid}加入群 {gid},验证消息为 “{comment}”")
                await bot.set_group_add_request(
                    flag=flag,
                    sub_type=sub_type,
                    approve=False,
                    reason=' ',
                )
        # 未关注，拒绝入群
        else:
            logger.info(f"拒绝{uid}加入群 {gid},验证消息为 “{comment}”")
            await bot.set_group_add_request(
                flag=flag,
                sub_type=sub_type,
                approve=False,
                reason='未关注',
            )

         
