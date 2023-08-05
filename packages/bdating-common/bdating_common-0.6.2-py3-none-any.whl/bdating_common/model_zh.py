from enum import Enum

class EyeColor(str, Enum):
  blue = '蓝色'
  black = '黑色'
  green = '绿色'
  other = '其他'
  brown = '褐色'


class HairColor(str, Enum):
  blue = '蓝发'
  black = '黑发'
  red = '红发'
  other = '其他'
  blond = '金发'

class Gender(str, Enum):
  male = '男'
  female = '女'

class Ethnicity(str, Enum):
  asian = '亚洲'
  caucasian = '白人'
  australian = '澳大利亚人'


class BuildType(str, Enum):
  slender = '高挑'
  fit = '匀称'
  skinny = '苗条'
  athletic = '健美'
  chunky = '结实'


class BustSize(str, Enum):
  a = 'A'
  b = 'B'
  c = 'D'
  d = 'D'
  e = 'E'
  f = 'F'
  g_plus = 'G+'


class DressSize(str, Enum):
  small = 'Small'
  medium = 'Medium'
  large = 'Large'
  large_plus = 'Large+'
  small_minus = 'Small-'


class SpeakingLanguage (str, Enum):
  english = '英文'
  mandarine = '普通话'
  japanese = '日语'
  korean = '韩语'
  cantonese = '广东话'


class PaymentMethod (str, Enum):
  card = '刷卡'
  cash = '现金'
  pay_id = 'PayID'

class TimeSlotStatus(str, Enum):
  available = '空闲'
  booked = '订满'
  locked = '上锁'

class BookingStatus(str, Enum):
  attempt = '预定中'
  confirmed = '已经预定'
  cancel_attempt = '取消中'
  canceled = '已取消'  # ?? need this or directly delete
  fulfilled = '已完成'
  archived = '已归档'
  deleted = '已删除'  # need this? or simply delete it. as _id will conflict
