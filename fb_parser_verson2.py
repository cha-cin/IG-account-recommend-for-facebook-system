import requests
import json as simplejson
import sys
import csv


input_token = input('token:')
input_id = input('id:')



my_token  = input_token

object_id = input_id
param     = "posts?fields=shares,id,message,story,created_time,name,link,status_type,type&limit=100"
post_list = []
copy_post_list = []
post_list.append(['id','message','story','status','time','type','link','name','shares'])
url       = "https://graph.facebook.com/v2.11/{}/{}&access_token={}".format(object_id, param, my_token)
res       = requests.get(url)
while "paging" in res.json():
    for info in res.json()['data']:
        # 擷取的貼文(Post)屬性
        id      = ""    # ['id']           貼文編號(ID)
        message = ""    # ['message']      貼文內容
        story   = ""    # ['story']        貼文性質(share something, add photo, update profile)
        status  = ""    # ['status_type']  貼文性質(mobile_status_update, created_note, added_photos, added_video, shared_story, created_group, created_event, wall_post, app_created_story, published_story, tagged_in_photo, approved_friend)
        time    = ""    # ['created_time'] 貼文時間
        type    = ""    # ['type']         貼文類型(link, status, photo, video, offer)
        link    = ""    # ['link']         連結的位址(外部連結或內部影片及照片的連結)
        name    = ""    # ['name']         分享連結文章的標題
        shares  = 0     # ['shares']       分享次數 = {'count': n}
        if "id" in info: id = info['id']
        if "message" in info: message = info['message'].replace("\n","")
        if "story" in info: story = info['story']
        if "status_type" in info: status = info['status_type']
        if "created_time" in info: time = info['created_time']
        if "type" in info: type = info['type']
        if "link" in info: link = info['link']
        if "name" in info: name = info['name']
        # 計算貼文分享
        if "shares" in info:
            shares = int(info['shares']['count'])
        
        post_list.append([id, message, story, status, time, type, link, name, shares])
    # 如果有下一頁，再向FB請求下一頁的資料
    if 'next' in res.json()['paging']:
        res = requests.get(res.json()['paging']['next'])
    else:
        break

copy_post_list = post_list.copy()
print(len(copy_post_list))
# 開啟輸出的 CSV 檔案
with open("new_file.csv","w+", encoding = 'utf_8_sig') as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(copy_post_list)