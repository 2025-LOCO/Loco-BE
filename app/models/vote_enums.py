from enum import Enum

class VoteType(str, Enum):
    real = "real"       # 진짜예요
    normal = "normal"   # 무난해요
    bad = "bad"         # 아쉬워요