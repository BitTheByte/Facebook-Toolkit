# -*- coding: utf-8 -*-
import requests
import pyquery
import hashlib
import urllib2
import json
import sys
from urllib import urlencode
import collections


class FacebookToolkit:

    def __init__(self, email="",password=""):
        self.email  = email
        self.password = password
        self.access_token = self.__accessToken()
        self.__fb_dtsg , self.id , self.__cookie = self.__login()
        #----------------------Checks-----------------------#
        if self.email:
            if self.password:
                if self.access_token:
                    if self.__cookie:
                        if self.__fb_dtsg:
                            print "[*] Login Success : {0}".format(self.email)
                        else:
                            print "[!] Oops I couldn't get data i need , make sure there is no check point on facebook"
                            sys.exit()
                    else:
                        print "[!] Failed to Fetch Cookies .. check your email or password"
                        sys.exit()
                else:
                    print "[!] Failed to Fetch Access token .. check your email or password"
                    sys.exit()
            else:
                print "[!] Please Enter Facebook Email's Password"
                sys.exit()
        else:
            print "[!] Please Enter Email Address"
            sys.exit()
    def __accessToken(self):
        data = collections.OrderedDict()
        data["api_key"] = "882a8490361da98702bf97a021ddc14d"
        data["email"] = self.email
        data["format"]= "JSON"
        data["locale"] = "vi_vn"
        data["method"] = "auth.login"
        data["password"] = self.password
        data["return_ssl_resources"] = "0"
        data["v"] = "1.0"
        sig = "".join("{0}={1}".format(key,data[key]) for key in data)
        data["sig"] = hashlib.md5(f"{sig}62f8ce9f74b12f84c123cc23437a4a32").hexdigest()
        try:
            return json.loads(urllib2.urlopen("https://api.facebook.com/restserver.php?{0}".format(urlencode(data))).read())["access_token"]
        except:
            return False
    def __login(self):
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
        })

        response = session.get('https://m.facebook.com')
        response = session.post('https://m.facebook.com/login.php', data={
            'email': self.email,
            'pass': self.password
        }, allow_redirects=False)

        if 'c_user' in response.cookies:
            homepage_resp = session.get('https://m.facebook.com/home.php')
            dom = pyquery.PyQuery(homepage_resp.text.encode('utf8'))
            fb_dtsg = dom('input[name="fb_dtsg"]').val()
            return fb_dtsg, response.cookies['c_user'], response.cookies
        else:
            return "", "" ,""
    def get_r(self, query):
        """
        GET Requset to Graph.facebook.com
        """
        try:
            return urllib2.urlopen("https://graph.facebook.com/{0}?access_token={1}&method=get".format(str(query), str(self.access_token))).read()
        except:
            return False
    def post_r(self, query):
        """
        POST to Graph.facebook.com
        """
        try:
            return urllib2.urlopen("https://graph.facebook.com/{0}&access_token={1}&method=post".format(str(query), str(self.access_token))).read()
        except:
            return False
    def comment(self,post_id,msg):
        """
        Comment on Facebook Post
        """
        return self.post_r("{0}/comments?message={1}".format(post_id, msg))
    def share(self,post_url):
        """
        Share Facebook Post on User's Profile
        """
        return self.post_r("{0}/feed/?link={1}".format(json.loads(self.get_r("me"))["id"], post_url))
    def react(self,post_id ,reaction):
        """
        React to Post {LIKE,LOVE,HAHA,ANGRY,WOW}
        """
        reactions = {
            "LIKE": "1",
            "LOVE": "2",
            "WOW":"3",
            "HAHA": "4",
            "GAY": "5",
            "THANKFUL" :"6",
            "SAD": "7",
            "ANGRY": "8"
        }
        data = [
            ('ft_ent_identifier',post_id),
            ('reaction_type', reactions[reaction]),
            ('fb_dtsg', self.__fb_dtsg)
        ]
        requests.post('https://www.facebook.com/ufi/reaction/', data=data, cookies=self.__cookie)
    def add_friend(self,profile_id):
        """
        Add a Facebook's Friend
        """
        data = [
            ('to_friend', profile_id),
            ('fb_dtsg', self.__fb_dtsg),
            ('action', 'add_friend'),
            ('how_found', 'profile_button')
        ]
        requests.post('https://www.facebook.com/ajax/add_friend/action.php', data=data, cookies=self.__cookie)
    def add_to_group(self,group_id , profile_id):
        """
        Add Friend to Group
        """
        data = [
            ('group_id', group_id),
            ('fb_dtsg', self.__fb_dtsg),
            ('source', 'typeahead'),
            ('members', profile_id)
        ]
        requests.post('https://www.facebook.com/ajax/groups/members/add_post.php', data=data, cookies=self.__cookie)
    def post(self,text):
        """
        Create Post on User's Timeline
        """
        print self.post_r("me/feed?message={0}".format(text))
    def send_message(self,to_id,msg):
        """
        Send Message to User
        """
        data = [
            ('ids', to_id),
            ('body', msg),
            ('waterfall_source', 'message'),
            ('fb_dtsg', self.__fb_dtsg)
        ]
        requests.post('https://m.facebook.com/messages/send/', data=data, cookies=self.__cookie)
    def posts_of(self,profile_id):
        """
        Get Posts of Profile or Page
        """
        return self.post_r("{0}/feed".format(profile_id))
    def printinfo(self):
        print "=================================================================================="
        print "COOKIE JAR : {0}".format(self.__cookie)
        print "FB_DSTG : {0}".format(self.__fb_dtsg)
        print "COOkIE ID : {0}".format(self.id)
        print "ACCESS_TOKEN : {0}".format(self.access_token)
        print "=================================================================================="
class GraphQl:
    def __init__(self, access_token):
        self.access_token = access_token
    def query(self,query):
        print "https://graph.facebook.com/graphql?q={0}&access_token={1}".format(str(query), str(self.access_token))
        return urllib2.urlopen("https://graph.facebook.com/graphql?q={0}&access_token={1}".format(str(query), str(self.access_token))).read()





