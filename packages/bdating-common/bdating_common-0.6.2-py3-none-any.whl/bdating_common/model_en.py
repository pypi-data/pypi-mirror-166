
from typing import List, Optional
from enum import Enum

class Gender(str, Enum):
  male = 'Male'
  female = 'Female'

class EyeColor(str, Enum):
  blue = 'Blue'
  black = 'Black'
  green = 'Green'
  other = 'Other'
  brown = 'Brown'


class HairColor(str, Enum):
  blue = 'Blue'
  black = 'Black'
  red = 'Red'
  other = 'Other'
  blond = 'Blond'


class Ethnicity(str, Enum):
  asian = 'Asian'
  caucasian = 'Caucasian'
  australian = 'Australian'


class BuildType(str, Enum):
  slender = 'Slender'
  fit = 'Fit'
  skinny = 'Skinny'
  athletic = 'Athletic'
  chunky = 'Chunky'


class BustSize(str, Enum):
  a = 'A'
  b = 'B'
  c = 'C'
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
  english = 'English'
  mandarine = 'Mandarine'
  japanese = 'Japanese'
  korean = 'Korean'
  cantonese = 'Cantonese'


class PaymentMethod (str, Enum):
  card ='Card'
  cash = 'Cash'
  pay_id = 'Pay_id'


class TimeSlotStatus(str, Enum):
  available = 'Available'
  booked = 'Booked'
  locked = 'Locked'


class BookingStatus(str, Enum):
  attempt = 'Attempt'
  confirmed = 'Confirmed'
  cancel_attempt = 'Cancel_Attempt'
  canceled = 'Cancel_Confirmed'  # ?? need this or directly delete
  fulfilled = 'Fulfilled'
  archived = 'Archived'
  deleted = 'Deleted'  # need this? or simply delete it. as _id will conflict
