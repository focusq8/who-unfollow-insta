import requests
from uuid import uuid4

get_all_following = []
get_all_followers = []
who_unfollow = []

def login():
    global get_sessionid , username , get_user_id , get_csrftoken

    username = input("[+] username: ")
    password = input("[+] password: ") 

    url_login = 'https://i.instagram.com/api/v1/accounts/login/'

    headers_login = {

        'X-Pigeon-Session-Id': str(uuid4()),
        'X-IG-Device-ID': str(uuid4()),
        'User-Agent': 'Instagram 159.0.0.40.122 Android (25/7.1.2; 240dpi; 1280x720; samsung; SM-G977N; beyond1q; qcom; en_US; 245196089)',
        'X-IG-Connection-Type': 'WIFI',
        'X-IG-Capabilities': '3brTvx8=',
        "Connection" : 'keep-alive',
        "Accept-Language": "en-US",
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        "Accept-Encoding": "gzip, deflate",
        'Host': 'i.instagram.com',
        'Cookie': 'mid=YqejMwABAAExc4QmMCMsnq5YVuEw; csrftoken=BE0qlaD88tnB3vjkLhGksva9WFE2LPYB'
        }
        
    data = {
        'username': username,
        'enc_password': f"#PWD_INSTAGRAM:0:&:{password}",
        "adid": uuid4(),
        "guid": uuid4(),
        "device_id": uuid4(),
        "phone_id": uuid4(),
        "google_tokens": "[]",
        'login_attempt_count': '0'
        }

    req_login = requests.post(url=url_login, headers=headers_login, data=data)

    if 'logged_in_user' in req_login.text:
        print(f"[+] Logged in with {username}")
        get_sessionid = req_login.cookies.get("sessionid")
        get_user_id = req_login.cookies.get("ds_user_id")
        get_csrftoken =req_login.cookies.get("csrftoken")
        get_following()
    else:
        print(req_login.text)

def get_following():

    url = f'https://i.instagram.com/api/v1/friendships/{get_user_id}/following/?includes_hashtags=true&search_surface=follow_list_page&query=&enable_groups=true&rank_token=43ad631e-d211-46a9-a5cc-9e0d2f14bcc0'
    
    header = {
        'Host': 'i.instagram.com',
        'Cookie': f'csrftoken={get_csrftoken}; sessionid={get_sessionid}',
        'X-Ig-Www-Claim':'hmac.AR2OyTfT1R295O4lDaLa3KWTfnnUlpGCei-EHkXl3J6WD6aA',
        'X-Ig-Connection-Type': 'WIFI',
        'X-Ig-Capabilities': '3brTvx8=',
        'User-Agent': 'Instagram 159.0.0.40.122 Android (25/7.1.2; 240dpi; 1280x720; samsung; SM-G977N; beyond1q; qcom; en_US; 245196089)',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate'
        }

    req = requests.get(url=url,headers=header)
    try:
        if 'users' in req.text:
            get_all_users = req.json()["users"]
            for loop in get_all_users:
                get_all_following.append(loop["username"])
        get_followers()

    except Exception:
        input(f"Error get following {req.text}")

def get_followers():

    url = f'https://i.instagram.com/api/v1/friendships/{get_user_id}/followers/?includes_hashtags=true&search_surface=follow_list_page&query=&enable_groups=true&rank_token=43ad631e-d211-46a9-a5cc-9e0d2f14bcc0'
    
    header = {
        'Host': 'i.instagram.com',
        'Cookie': f'csrftoken={get_csrftoken}; sessionid={get_sessionid}',
        'X-Ig-Www-Claim':'hmac.AR2OyTfT1R295O4lDaLa3KWTfnnUlpGCei-EHkXl3J6WD6aA',
        'X-Ig-Connection-Type': 'WIFI',
        'X-Ig-Capabilities': '3brTvx8=',
        'User-Agent': 'Instagram 159.0.0.40.122 Android (25/7.1.2; 240dpi; 1280x720; samsung; SM-G977N; beyond1q; qcom; en_US; 245196089)',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate'
        }
    req = requests.get(url=url,headers=header)

    try:
         if 'users' in req.text:
            get_all_users = req.json()["users"]
            for loop in get_all_users:
                get_all_followers.append(loop["username"])
            get_unfollow()           
    except Exception:
        input(f"Error get followers {req.text}")

def get_unfollow():
    for loop in get_all_following:
        if loop not in get_all_followers and loop not in who_unfollow:
            who_unfollow.append(loop)

    for show_who_unfollow in who_unfollow:
        with open("who_unfollow.txt","a") as f:
            f.write(f'{show_who_unfollow}\n')
    print("Save as who_unfollow")

if __name__ == "__main__":
    login()