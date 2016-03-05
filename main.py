#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import httplib, urllib
import config
import json
import datetime

template.register_template_library('common.filters')

def get_access_token():
  params = urllib.urlencode({'grant_type': 'authorization_code', 'code': '2kfKxKKiAX0K_6IF0jDAeuAAaP3jiAE6QT3M6VDq5qZ45YrER1FiH25v70OJF1b7', 'client_id': '2z4612HVM7626cGHakyM4C38dbZO6yUS', 'client_secret': 'hNZ49i30R9o3It7A79b3w5l8Uv231dM7Zb0mq996zW66JqT2v078q2D3t_L_fm2Y'})
  headers = {"Access-Control-Allow-Origin": "*"}
  conn = httplib.HTTPSConnection("api.moves-app.com/oauth/v1/access_token")
  conn.request("POST", "", params, headers)
  response = conn.getresponse()
  print response.status, response.reason
  data = response.read()
  print data

def get_user_profile():
  params = urllib.urlencode({'access_token': config.NEW_ACCESS_TOKEN})
  url = "api.moves-app.com/api/1.1/user/profile?%s" % (params)
  conn = httplib.HTTPSConnection(url)
  conn.request("GET", "", "")
  response = conn.getresponse()
  user_info = response.read()
  return json.loads(user_info)

def get_places(first_date, last_date=''):
  params = urllib.urlencode({'access_token': config.NEW_ACCESS_TOKEN})
  if last_date == '':
    url = "api.moves-app.com/api/1.1/user/places/daily/%s?%s" % (first_date, params)
  else:
    url = "api.moves-app.com/api/1.1/user/places/daily?from=%s&to=%s&%s" % (first_date, last_date, params)

  conn = httplib.HTTPSConnection(url)
  conn.request("GET", "", "")
  response = conn.getresponse()
  data = json.loads(response.read())
  places = data[0]["segments"]
  locations_json = json.dumps(places)
  return locations_json

def get_storyline(first_date, last_date=''):
  params = urllib.urlencode({'access_token': config.NEW_ACCESS_TOKEN})
  if last_date == '':
    url = "api.moves-app.com/api/1.1/user/storyline/daily/%s?%s" % (first_date, params)
  else:
    url = "api.moves-app.com/api/1.1/user/storyline/daily?from=%s&to=%s&%s" % (first_date, last_date, params)

  conn = httplib.HTTPSConnection(url)
  conn.request("GET", "", "")
  response = conn.getresponse()
  data = json.loads(response.read())
  storyline = data[0]["segments"]
  return storyline

class RequestHandle(webapp2.RequestHandler):
  def post(self):
    first = self.request.get("first")
    last = self.request.get("last")
    locations = get_places(first, last)
    self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
    self.response.out.write(locations)

class Home(webapp2.RequestHandler):
  def get(self):
    utc_now = datetime.datetime.now()
    est_now = utc_now - datetime.timedelta(hours=4)
    today_str = est_now.strftime('%Y-%m-%d')
    locations = get_places(today_str)
    user_info = get_user_profile()

    first_date = user_info['profile']['firstDate']
    self.response.out.write(template.render('home.html',{'locations': locations, 'first_date': first_date}))

class Storyline(webapp2.RequestHandler):
  def get(self):
    specfied_date = self.request.get("date")
    specfied_date = specfied_date.strip()
    today = False
    yesterday = False

    utc_now = datetime.datetime.now()
    est_now = utc_now - datetime.timedelta(hours=4)
    date_str = est_now.strftime('%Y-%m-%d')

    if specfied_date == '':
      today = True
    else:
      date_str = specfied_date
      # see if specified date is yesterday
      d = datetime.datetime.strptime(specfied_date, '%Y-%m-%d')
      delta = est_now - d
      if delta.days == 0:
        today = True
      if delta.days == 1:
        yesterday = True

    storyline = get_storyline(date_str)
    user_info = get_user_profile()

    first_date = user_info['profile']['firstDate']
    self.response.out.write(template.render('storyline.html',{'today': today, 'yesterday': yesterday, 'date_str': date_str, 'storyline': storyline, 'first_date': first_date, 'color_option': 10}))


class About(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(template.render('about.html',{}))


class Test(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(template.render('test.html',{}))


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/storyline', Storyline),
    ('/test', Test),
    ('/requestHandle', RequestHandle),
    ('/about', About)
], debug=True)
