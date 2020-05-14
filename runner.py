import requests
from bs4 import BeautifulSoup
import os
import re
import json
import pprint
import time
import re
import os
import struct
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import urllib3


def post(wp_url,wp_user,wp_pw,wp_title,wp_context,wp_thumbnail,wp_tags,wp_categorys):
    while True:
        try:
            client = Client(wp_url,wp_user,wp_pw)
            if wp_thumbnail != None:
                filename = wp_thumbnail
            # prepare metadata
                data = {
                        'name': 'picture.jpg',
                        'type': 'image/jpeg',  # mimetype
                }

# read the binary file and let the XMLRPC library encode it into base64
                with open(filename, 'rb') as img:
                        data['bits'] = xmlrpc_client.Binary(img.read())

                response = client.call(media.UploadFile(data))
                attachment_id = response['id']
            post = WordPressPost()
            post.title = wp_title
            post.content = wp_context
            post.post_status = 'publish'
            if wp_thumbnail != None:
                post.thumbnail = attachment_id
            post.terms_names = {
            'post_tag': wp_tags,
            'category': wp_categorys
            }
            post.id = client.call(posts.NewPost(post))
            return "https://weporn.tv/?p=" + str(post.id)
        except:
            pass

def upload_openload(file_path):
    r = requests.post('https://api.openload.co/1/file/ul?login=9639bb2e9c1e850a&key=u2OCdxck')
    print r.text
    data = json.loads(r.text)
    if data['msg'] == "OK":
        r = requests.post(data['result']['url'],files={'file': open(file_path, 'rb')})
        print r.text
        result = json.loads(r.text)
        print result
        if result["msg"] == "OK":
            return result['result']['id'],result['result']['url']

urllib3.disable_warnings()
session = requests.Session()
while True:
    main_page = session.get("http://ladybaba.net/archives/category/%E7%84%A1%E4%BF%AE%E6%AD%A3")
    soup = BeautifulSoup(main_page.text.encode("utf8"),"html.parser")
    vid_fields = soup.findAll('li',{"class":"border-radius-5 box-shadow"})
    for field in vid_fields:
        links = field.findAll('a')
        list_of_urls = open("list.txt","r").read().split("\r\n")
        if links[0]["href"] in list_of_urls:
            continue
        open("list.txt","a").write(links[0]["href"] + "\r\n")
        print "video_url: " +links[0]["href"]
        vid_page = session.get(links[0]["href"])
        vid_soup = BeautifulSoup(vid_page.content,"lxml")
        tag_grab = vid_soup.findAll('a',{'class':'tag-cloud-link'})
        tags = list()
        for x in tag_grab:
            tags.append(x.getText().encode("utf-8"))
        category_grab = vid_soup.findAll('a',{'rel':'tag'})
        categorys = list()
        for x in category_grab:
            categorys.append(x.getText().encode("utf-8"))
        thumbnail = vid_soup.findAll('img',{'class':'video-img'})[0]['src']
        r = session.get(thumbnail, stream=True)
        with open( "thumbnail.jpg", 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
        video_embed_soup = vid_soup.findAll('div',{"class":"video-embed"})
        desc = video_embed_soup[0].getText().strip()
        print "desc: " + desc.encode("utf-8") 
        title_soup = vid_soup.findAll("meta",{"property":"og:title"})
        video_url = video_embed_soup[0].findAll('iframe')[0]["src"]
        print "stream_url: " +video_url
        xvid = session.get(video_url)
        match = re.search("html5player.setVideoUrlHigh\(\'(.*?)'\)\;",xvid.text.encode("utf8"))
        print "download_url: " + match.group(1)
    #print match.group(1)
        r = session.get(match.group(1), stream=True)
        with open( "video.mp4", 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
        vid_id,vid_url = upload_openload("video.mp4")
        post_url = post("http://exmple.com/xmlrpc.php","example","example",title_soup[0]["content"].strip().encode("utf-8"),'<iframe src="https://openload.co/embed/' + str(vid_id) + '/" scrolling="no" frameborder="0" width="700" height="430" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe>' + "\r\n" + video_embed_soup[0].getText().strip().encode("utf-8"),"thumbnail" + ".jpg",tags,categorys)
        os.remove("thumbnail.jpg")
        os.remove("video.mp4")
        print "!=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~!"  
