from google.appengine.ext import webapp
import time, datetime
import random

register = webapp.template.create_template_register()

@register.filter
def formatTime(yyyyMMddTHHmmssZ):
  time_format = "%Y%m%dT%H%M%SZ"
  dt = datetime.datetime.strptime(yyyyMMddTHHmmssZ, time_format)
  est_dt = dt - datetime.timedelta(hours=4)
  date_str = est_dt.strftime("%Y-%m-%d %H:%M")
  return date_str

@register.filter
def formatTimeWithSeconds(yyyyMMddTHHmmssZ):
  time_format = "%Y%m%dT%H%M%SZ"
  dt = datetime.datetime.strptime(yyyyMMddTHHmmssZ, time_format)
  est_dt = dt - datetime.timedelta(hours=4)
  date_str = est_dt.strftime("%H:%M:%S")
  return date_str

@register.filter
def convertSecsToMins(value):
  return int(value / 60)

@register.filter
def randomizeColor(value):
  return random.randint(1, value)

@register.filter
def setMoveHeight(value):
  minute = int(value / 60)
  if int(value / 60) * 20 <= 40:
    return 40
  if int(value / 60) * 20 >= 250:
    return 250
  return int(value / 60) * 15



