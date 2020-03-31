#!/usr/bin/env python3

import os
import random

GROUP_ID = 57653465

bot_id = os.environ.get("GROUPME_BOT_ID")
if not bot_id:
    with open(os.environ["HOME"] + "/groupme_bot_id.txt", "r") as f:
        bot_id = f.read().strip()


