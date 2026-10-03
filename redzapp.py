import re, string, uuid, requests, os, json, time, random
from user_agent import generate_user_agent
from random import choice 
from urllib.parse import quote
from threading import Thread, Lock
BIO = [
   "لا إِلَهَ إِلا أَنتَ سُبْحَانَكَ إِنِّي كُنتُ مِنَ الظَّالِمِينَ🌸",
   "اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ , وَشُكْرِكَ , وَحُسْنِ عِبَادَتِكَ🎈💞",
   "استغفر الله العظيم وأتوبُ إليه 🌹",
   "حَسْبِيَ اللَّهُ لا إِلَـهَ إِلاَّ هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيم"
   "سبحان الله وبحمده سبحان الله العظيم🌸",
   "اللهم إنك عفو تُحب العفو فاعفُ عنّا 🌿🌹",
   "استغفر الله العظيم وأتوبُ إليه 🌹",
   "﴿ رَبِّ اشْرَحْ لِي صَدْرِي وَيَسِّرْ لِي أَمْرِي ﴾",
   "{ تَوَفَّنِي مُسْلِمًا وَأَلْحِقْنِي بِالصَّالِحِينَ }",
   "اللهم اشفي كل مريض يتألم ولا يعلم بحاله إلا أنت",
   "استغفر الله العظيم وأتوبُ إليه.",
   "تعرف الدنيا عظيماً مِثله صلّوا عليه وسلموا تسليم",
   " أنتَ اللّطيف وأنا عبدُك الضّعيف اغفرلي وارحمني وتجاوز عنّي.",
   "- اللهُم صبراً ، اللهم جبراً ، اللهم قوّة",
   "أصبحنا وأصبح الملك لله ولا اله الا الله.",
   "اللهَ يُحِبُ المُلحِينَ فِي الدُّعَاء.",
   "الله لا يخذل يداً رُفعت إليه أبداً.",
   "يارب دُعاء القلب انت تسمعه فأستجب لهُ.",
   "- اللهم القبول الذي لا يزول ❤️🍀.",
   "- اللهُم خذ بقلبّي حيث نورك الذي لا ينطفِئ.",
   "سبحان الله وبحمده ،سبحان الله العظيم.",
   "لا تعودوا أنفسكم على الصمت، اذكرو الله، استغفروه، سبّحوه، احمدوه،"
   " عودوا السنتكم على الذكر فإنها إن اعتادت لن تصمت أبدًا.",
   "- اللهم احرمني لذة معصيتك وارزقني لذة طاعتك 🌿💜.",
   "- اللهُم إن في صوتي دُعاء وفي قلبِي أمنية اللهُم يسر لي الخير حيث كان.",
   "أرني عجائب قدرتك في تيسير أموري 💜.",
   "يغفر لمن يشاء إجعلني ممن تشاء يا الله.*",
   "اللهـم إجعلنا ممن تشهد أصابعهم بذكـر الشهادة قبل الموت 🌿💜.",
   "- وبك أصبحنا يا عظيم الشأن 🍃❤️.",
   "اللهُم الجنة ونعيَّم الجنة مع من نحب💫❤️🌹",
   "اشهد ان لا اله الا الله وان محمدا عبده ورسوله",
   "لا اله الا الله سيدنا محمد رسول الله🌿💜",
   "قول معايا - استغفر الله استفر الله استغفر الله -",
   "مُجرد ثانية تنفعِك : أستغفُرالله العظيِم وأتوب إليّه.",
   "رَبَّنَا اغفِر لي وَلِوالِدَيَّ وَلِلمُؤمِنينَ يَومَ يَقومُ الحِسابُ",
   "وَاذْكُر ربّكَ إِذَا نَسِيتَ",
   "- اللهم صلِ وسلم على نبينآ محمد ❥⇣",
   "اللهم اكفني بحلالك عن حرامك، وأغنني بفضلك عمن سواك",
   "(بِسْمِ اللَّهِ، تَوَكَّلْتُ عَلَى اللَّهِ، وَلَاَ حَوْلَ وَلَا قُوَّةَ إِلاَّ بِاللَّهِ)",
   "((أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ)) (مِائَةَ مَرَّةٍ فِي الْيَوْمِ).",
   "مَنْ كَانَ آخِرُ كَلاَمِهِ لاَ إِلَهَ إِلاَّ اللَّهُ دَخَلَ الْجَنَّة",]
FIRST_NAMES = [
    'محمد','أحمد','عبدالله','عبدالرحمن','عبدالعزيز','عبدالملك','عبدالله','خالد','سعود','فهد',
    'سلطان','ناصر','فيصل','تركي','مشعل','بندر','ماجد','وليد','ياسر','عمر',
    'علي','حسن','حسين','يوسف','إبراهيم','إسماعيل','عثمان','طارق','سامي','راشد',
    'حمد','جاسم','أنور','منصور','صالح','سليمان','زكي','نواف','مشاري','عادل',
    'كريم','باسم','رامي','هاني','فارس','زياد','مروان','أنس','بلال','أمين',
    'رائد','نبيل','جمال','شريف','هشام','ماهر','عصام','معتز','إياد','وسام',
    'لؤي','قصي','همام','غسان','فادي','سامر','نادر','طلال','علاء','رياض',
    'قاسم','سفيان','ياسين','أيوب','حمزة','زكريا','إلياس','نوح','آدم','مالك',
    'سيف','فراس','حسام','مؤيد','معاذ','أسامة','أيمن','بشار','ثامر','جهاد',
    'حيدر','داود','ذياب','رعد','زهير','سعد','شادي','صابر','ضياء','ظافر',
    'عباس','غازي','فواز','قتيبة','كامل','لطفي','محيي','نزار','هيثم','يزيد',
    'أكرم','بدر','تيم','جابر','حازم','خليل','رائد','زهدي','ساجد','شجاع',
    'صبري','طاهر','عامر','عبدالكريم','عبدالهادي','عبدالناصر','عبدالوهاب','عدنان','عز الدين','عماد',
    'غالب','فؤاد','قيس','لبيب','مجد','منير','نسيم','هلال','وائل','يحيى',
    'أوس','براء','تامر','جابر','حسان','خضر','راني','زاهر','سهيل','شكري']
LAST_NAMES = [
    'العتيبي','القحطاني','الدوسري','الشمري','الحربي','المطيري','العنزي','الزهراني','الغامدي','الشهري',
    'السبيعي','البقمي','الجعيد','الجهني','الرشيدي','الصاعدي','العمري','الفايز','القرني','المالكي',
    'النعيمي','الهذلي','اليامي','الثقفي','الحارثي','الخالدي','الدغيم','الراشد','الزيد','السالم',
    'الشريف','الصالح','الطائي','العبدلي','الفهد','الكناني','اللهيبي','المحيميد','الناصري','الهاشمي',
    'الوهيبي','اليوسف','آل سعود','آل نهيان','آل مكتوم','الكواري','المهندي','الجابر','الخليفي','المري',
    'الأنصاري','البلوشي','الجسمي','الحمادي','الخوري','الدرعي','الراشدي','الزيودي','السويدي','الشامسي',
    'الظاهري','العبيدلي','الفلاسي','الكتبي','المنصوري','النقبي','الهنائي','اليماحي','البوسعيدي','الحارثي',
    'الخروصي','السيابي','الشقصي','العامري','الفارسي','الكندي','المقبالي','النبهاني','الهنائي','اليافعي',
    'الحسيني','العلوي','الزيني','الخليل','الرفاعي','الصباغ','الطرابلسي','العلي','الفاعور','القدسي',
    'الكسواني','اللحام','المحمد','النجار','الهندي','الياسين','الأسعد','البقاعي','الجمل','الحمصي',
    'الديري','الرياشي','الزعبي','السقا','الشامي','الصيداوي','الطويل','العبسي','الفارس','القطان',
    'اللبابيدي','المصري','النابلسي','الهواري','اليوسف','أبو زيد','أبو سعد','أبو علي','ابن علي','آل علي',
    'بركات','جبران','حمادة','خوري','درويش','رزق','سلمان','شاهين','طربي','عبدالله',
    'عواد','فضل','قاسم','كنيش','لحود','مراد','ناصر','هلال','ياسين','زيدان',
    'حنا','سعود','عمر','فارس','كريم','ماجد','نادر','وسام','ياسر','حسن']
class creating_emails:
    def __init__(self):
        self.USR_AGNT = generate_user_agent()
        self.headers = {
            'Host': 'isealmail.com', 
            'User-Agent': str(self.USR_AGNT),
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://isealmail.com/en',
            'X-Inboxseal-Locale': 'en',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors', 
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=0',
            'Te': 'trailers'}
    def __get_domins(self) -> str:
        return 'JOKER1' + "".join(random.choices(string.ascii_lowercase + string.digits, k=9)) + '@innaze.com'
    def __extract_verification_code(self, html: str) -> str | None:
        if not html:
            return None
        match = re.search(r'Your verification code is\s+(\d+)', html)
        if match:
            return match.group(1)
        match = re.search(r'<div class="verification-code">\s*(\d+)\s*', html)
        return match.group(1) if match else None
    def get_inbox(self, email: str):
        try:
            summary_url = f'https://isealmail.com/api/public-mailboxes/{email}?view=summary&limit=20'
            items = []
            for attempt in range(5):
                summary = requests.get(summary_url, headers=self.headers, timeout=10).json()
                items = summary.get("data", {}).get("items", [])
                if items: break
                time.sleep(2)
            if not items:
                return None
            message_id = items[0]["id"]
            req = requests.get(
                f'https://isealmail.com/api/public-mailboxes/{email}/messages/{message_id}',
                headers=self.headers, timeout=10)
            payload = req.json()
            html = payload.get("data", {}).get("htmlBody") or req.text
            return self.__extract_verification_code(html)
        except Exception as JQ:
            print('[-] Bad Requests email get_inbox..')
            return None
    def create(self):
        try:
            email = self.__get_domins()
            req = requests.get(f'https://isealmail.com/api/public-mailboxes/{email}?view=summary&limit=20', headers=self.headers, timeout=10)
            mailbox = req.json()['data']['mailbox']['address']
            return mailbox
        except Exception as JQ:
            print('[-] Bad Requests email create..')
            return None
DEFAULT_SETTINGS = {
    "Activate": "on",
    "username_L": "random",
    "username": "vv1ck",
    "urlPost": "https://link.redzapp.net/posts/8ef80c34-2bf4-4dd5-aa9d-242785d0ffc7"}
def initialize_settings():
    os.makedirs('redzapp_accounts', exist_ok=True)
    if not os.path.exists('redzapp_accounts/Settings.json'):
        save_settings(DEFAULT_SETTINGS)
    else:
        try:
            with open('redzapp_accounts/Settings.json', 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().strip()
                if not content:
                    save_settings(DEFAULT_SETTINGS)
                else:
                    json.loads(content)
        except (json.JSONDecodeError, Exception):
            save_settings(DEFAULT_SETTINGS)
def load_settings():
    initialize_settings()
    try:
        with open('redzapp_accounts/Settings.json', 'r', encoding='utf-8', errors='ignore') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_SETTINGS.copy()
def save_settings(settings_dict):
    os.makedirs('redzapp_accounts', exist_ok=True)
    with open('redzapp_accounts/Settings.json', 'w', encoding='utf-8', errors='ignore') as wr:
        json.dump(settings_dict, wr, ensure_ascii=False, indent=5)
class interaction_with_accounts:
    def __init__(self, device_id: str , token: str , ios_user_agent: str , os_version: str, proxy: dict = None) -> None:
        self.device_id = device_id
        self.token = token
        self.ios_user_agent = ios_user_agent
        self.os_version = os_version
        self.proxy = proxy
        self.current_settings = load_settings()
        self.target = self.current_settings.get('username')
        self.LINK = self.current_settings.get('urlPost')
        self.urlSeries = self.current_settings.get('urlSeries')
    def get_headers(self) -> dict:
        return {
            'Host': 'backend.redzapp.net',
            'Accept': '*/*',
            'X-Device': self.device_id,
            'Authorization': f'Bearer {self.token}',
            'Priority': 'u=3, i',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-QR;q=1.0',
            'Language': 'en',
            'User-Agent': self.ios_user_agent,
            'X-App-Version': '5.5.4',
            'X-Platform': 'ios'}
    def get_id_post(self,IDS):
        LINK = requests.get(f'https://link.redzapp.net/posts/{IDS}', headers={'Host': 'link.redzapp.net','Sec-Fetch-Dest': 'document','User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.6 Mobile/15E148 Safari/604.1','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Sec-Fetch-Site': 'none','Sec-Fetch-Mode': 'navigate','Accept-Language': 'ar','Priority': 'u=0, i','Accept-Encoding': 'gzip, deflate','Connection': 'close'}, timeout=10).text
        try:id_post = LINK.split('type=POST&post_id=')[-1].split('"')[0]
        except Exception:
            try:id_post = LINK.split('type=POST\\u0026post_id=')[-1].split('"')[0]
            except Exception:id_post = None
        return id_post
    def get_id_series(self,IDS):
        LINK = requests.get(f'https://link.redzapp.net/series/{IDS}', headers={'Host': 'link.redzapp.net','Sec-Fetch-Dest': 'document','User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.6 Mobile/15E148 Safari/604.1','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Sec-Fetch-Site': 'none','Sec-Fetch-Mode': 'navigate','Accept-Language': 'ar','Priority': 'u=0, i','Accept-Encoding': 'gzip, deflate','Connection': 'close'}, timeout=10).text
        try:id_post = LINK.split('type=SERIE&serie_id=')[-1].split('"')[0]
        except Exception:
            try:id_post = LINK.split('type=SERIE\\u0026serie_id=')[-1].split('"')[0]
            except Exception:id_post = None
        return id_post
    def Retrieve_ID(self):
        try:ID = requests.get(f'https://backend.redzapp.net/api/users?complete_search=0&page=1&per_page=20&search={self.target}&with_following_status=1&with_history=1', headers=self.get_headers(), timeout=10).json()['data']['suggestions'][0]['id']
        except Exception:ID = None
        return ID 
    def likes_share_comments_bookmark(self, ID , city_id):
        Comments = choice(["❤️","🔥🔥","❤️🔥","💙🦋","❤️❤️❤️","👀🔥","😍😍","🃏🫣","👀💙","🔥🔥🔥🔥"])
        try:requests.post(f'https://backend.redzapp.net/api/posts/{ID}/view/', headers=self.get_headers(), json={"is_repeated":False,"video_duration":"22","city_id":city_id,"category":"SERIES_PROFILE","watch_time":"2"}, timeout=10)
        except Exception:pass
        try:requests.post(f'https://backend.redzapp.net/api/posts/{ID}/like', headers=self.get_headers(), json={"city_id":city_id}, timeout=10)
        except Exception:pass
        try:requests.post(f'https://backend.redzapp.net/api/posts/{ID}/share', headers=self.get_headers(), json={"city_id":city_id}, timeout=10)
        except Exception:pass
        try:requests.post(f'https://backend.redzapp.net/api/posts/{ID}/bookmark', headers=self.get_headers(), json={"city_id":city_id}, timeout=10)
        except Exception:pass
        try:requests.post(f'https://backend.redzapp.net/api/posts/{ID}/comments', headers=self.get_headers(), json={"mentions":[],"city_id":city_id,"content":Comments}, timeout=10)
        except Exception:pass
    def add_likes_share_series(self, ID):
        try:
            IDS = requests.get(f'https://backend.redzapp.net/api/series/{ID}', headers=self.get_headers(), timeout=10)
            try:
                idPost = IDS.json()['data']['id']
                try:city_id = IDS.json()['data']['city_id']
                except Exception:city_id = IDS.json()['data']['city']['id']
            except Exception:pass
            if city_id: 
                self.likes_share_comments_bookmark(idPost , city_id)
        except Exception:pass
    def add_likes_share_posts(self, ID):
        try:
            city_ids = requests.get(f'https://backend.redzapp.net/api/posts/{ID}?with_following_status=1&with_is_liked=1&with_is_saved=1', headers=self.get_headers(), timeout=10)
            try:city_id = city_ids.json()['data']['user']['city_id']
            except Exception:
                try:city_id = city_ids.json()['data']['city']['id']
                except Exception:
                    try:city_id = city_ids.json()['data']['serie']['city_id']
                    except Exception:city_id = None
            if city_id:self.likes_share_comments_bookmark(ID , city_id)
        except Exception:pass
    def add_follows(self):
        try:
            ID = self.Retrieve_ID()
            if ID:requests.post(f'https://backend.redzapp.net/api/users/{ID}/follows', headers=self.get_headers(), timeout=10)
        except Exception:pass
    def full_ad(self):
        self.add_follows()
        if 'posts' in self.LINK:
            IDS = self.LINK.split('/')[-1]
            ID = self.get_id_post(IDS)
            if ID:self.add_likes_share_posts(ID)
        elif 'series' in self.LINK:
            IDS = self.LINK.split('/')[-1]
            ID = self.get_id_series(IDS)
            if ID:self.add_likes_share_series(ID)
        print('[+] Added: Follow, Like, Share, comments, bookmark.')
class Redzapp_Accounts:
    def __init__(self):
        self.ERUN = True
        self.file_lock = Lock()
        self.used_names = set()
        self.current_settings = load_settings()
        self.TKN = 'qwe1rty2ui.op3asd4fg_hjkl5zxcv6bnmza7qwsxedcr9fvbhy_ojmly0'
        self.ios = ['19.5', '27.1', '23.3', '27.2', '25.1', '27.0', '26.6', '26.5', '26.4', '26.3', '26.2', '26.1', '26.0']
        self.Alamofire = ['5.12.0', '5.11.0', '5.10.0', '5.9.0', '5.8.0', '5.7.0', '5.6.0', '5.5.0', '5.4.0', '5.3.0', '5.2.0', '5.1.0', '5.0.0']    
        self.proxy_list = []
        self.thr()
    def get_proxy(self):
        if not self.proxy_list:
            return None
        PRX = choice(self.proxy_list)
        return {'http': PRX, 'https': PRX}
    def get_headers(self, device_id: str | None = None, ios_user_agent: str | None = None) -> dict:
        return {
            'Host': 'authentication.redzapp.net',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'X-Device': device_id,
            'Priority': 'u=3, i',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-QR;q=1.0',
            'X-Idempotency-Key': f'{int(time.time() * 1000)}-{str(uuid.uuid4()).upper()}',
            'Language': 'en',
            'User-Agent': ios_user_agent,
            'X-App-Version': '5.5.4',
            'X-Platform': 'ios'}
    def Generator_names(self):
        with self.file_lock:
            name = f"{choice(FIRST_NAMES)} {choice(LAST_NAMES)}"
            self.used_names.add(name)
            return name
    def upload_profile_photo(self, ID, device_id, username, token, ios_user_agent, name):
        print("[!] Uploading profile photo...")
        image_path = "cat.jpg"
        try:
            if not os.path.exists(image_path):
                print(f"[-] Image file '{image_path}' not found.")
                return False
            def get_headers():
                return {
                    'Host': 'backend.redzapp.net',
                    'Content-Type': 'application/json',
                    'Accept': '*/*',
                    'Authorization': f'Bearer {token}',
                    'X-Device': device_id,
                    'Priority': 'u=3, i',
                    'Accept-Language': 'en-QR;q=1.0',
                    'Language': 'en',
                    'X-Idempotency-Key': f'{int(time.time() * 1000)}-{str(uuid.uuid4()).upper()}',
                    'User-Agent': ios_user_agent,
                    'X-App-Version': '5.5.4',
                    'X-Platform': 'ios'}
            payload_step1 = {
                "files": [
                    {"type": "profile_images", "extension": "jpeg"}
                ]
            }
            res1 = requests.post(
                "https://backend.redzapp.net/api/s3/upload",
                headers=get_headers(),
                json=payload_step1,
                timeout=15)
            if res1.status_code != 200:
                return False
            data1_list = res1.json().get('data', {}).get('urls', [])
            if not data1_list:
                return False
            data1 = data1_list[0]
            upload_url = data1.get('url')
            file_key = data1.get('file')
            if not upload_url or not file_key:
                return False
            with open(image_path, 'rb') as img_f:
                img_data = img_f.read()
            upload_headers = {
                'Content-Type': 'image/jpeg',
                'Content-Length': str(len(img_data))}
            res_upload = requests.put(
                upload_url,
                headers=upload_headers,
                data=img_data,
                timeout=30)
            if res_upload.status_code not in [200, 204]:
                return False
            payload_step2 = {
                "key": file_key,
                "username": username,
                "file_type": "profile_images"}
            requests.post(
                'https://backend.redzapp.net/api/r2/event',
                headers=get_headers(),
                json=payload_step2,
                timeout=15)
            payload_step3 = {
                "username": username,
                "name": name,
                "profile_photo": file_key,
                "with_profile_photo": True}
            res3 = None
            for attempt in range(3):
                res3 = requests.put(
                    f'https://backend.redzapp.net/api/users/{ID}',
                    headers=get_headers(),
                    json=payload_step3,
                    timeout=15)
                if res3.status_code == 200:
                    return True
                elif res3.status_code == 409:
                    time.sleep(2)
                else:
                    break
            return False
        except Exception as e:
            return False
    def update_account(self, ID, device_id, email, username, token, ios_user_agent, os_version, proxy):
        print("[!] Updating account...")
        try:
            phone = '5' + ''.join(random.choice('0123456789') for _ in range(7))
            name = self.Generator_names()
            data = {
                "mobile_version": "5.5.4",
                "os": "IOS",
                "contact_email": email,
                "phone_number": phone,
                "country_code": "+974",
                "name": name,
                "date_of_birth": "1997-02-01",
                "device_id": device_id,
                "os_version": os_version,
                "bio":str(choice(BIO)),
                "username": username}
            headers = {
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Authorization': f'Bearer {token}',
                'X-Device': device_id,
                'Priority': 'u=3, i',
                'Accept-Language': 'en-QR;q=1.0',
                'Language': 'en',
                'X-Screen': 'HOME',
                'X-Idempotency-Key': f'{int(time.time() * 1000)}-{str(uuid.uuid4()).upper()}',
                'User-Agent': ios_user_agent,
                'X-App-Version': '5.5.4',
                'X-Platform': 'ios'}
            r = requests.put(f'https://backend.redzapp.net/api/users/{ID}', headers=headers, json=data , proxies=proxy, timeout=10)
            if ('email' in r.text):
                print("[+] Account updated successfully")
            else:
                print("[-] Account update failed")
        except (requests.exceptions.ConnectionError , requests.exceptions.ReadTimeout , requests.exceptions.ChunkedEncodingError , requests.exceptions.InvalidURL , requests.exceptions.ProxyError , requests.exceptions.Timeout , requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError):pass
        except Exception as JQ:
            print('[-] Bad Requests Update Account..')
            with self.file_lock:
                with open(f'redzapp_accounts/ERRORS_Exception.txt', 'a' , encoding='utf-8' , errors='ignore') as wr:
                    wr.write(f"update_account: {JQ}\n")
        #self.upload_profile_photo(ID, device_id, username, token, ios_user_agent ,name)
        if self.current_settings.get('Activate') == 'on':
            interaction = interaction_with_accounts(device_id, token, ios_user_agent, os_version, proxy)
            interaction.full_ad()
    def complete(self, keycloak_id , code , device_id , email , username, ios_user_agent, os_version, proxy):
        print("[!] Completing account...")
        try:
            data = {"keycloak_id":keycloak_id,"password":"JOKER=cathack","password_confirmation":"JOKER=cathack","verification_code":code}
            JQ = requests.post('https://authentication.redzapp.net/api/v2/auth/action/complete', headers=self.get_headers(device_id, ios_user_agent), json=data, proxies=proxy, timeout=10)
            if ('token' in JQ.text):
                print("[+] Account completed successfully")
                token = JQ.json()['data']['token']
                ID = JQ.json()['data']['user']['id']
                with self.file_lock:
                    if self.current_settings.get('username_L') == 'random':
                        with open(f'redzapp_accounts/new_random_accounts.txt', 'a' , encoding='utf-8' , errors='ignore') as wr:
                            wr.write(f"{email}|{username}:JOKER=cathack|{device_id}\n")
                    else:
                        with open(f'redzapp_accounts/new_{str(len(username))}L_accounts.txt', 'a' , encoding='utf-8' , errors='ignore') as wr:
                            wr.write(f"{email}|{username}:JOKER=cathack|{device_id}\n")
                self.update_account(ID, device_id , email , username, token, ios_user_agent, os_version, proxy)
            else:
                print("[-] Account completion failed")
                with self.file_lock:
                    with open(f'redzapp_accounts/ERRORS_requests.txt', 'a' , encoding='utf-8' , errors='ignore') as wr:
                        wr.write(f"complete: {JQ.text}\n")
        except (requests.exceptions.ConnectionError , requests.exceptions.ReadTimeout , requests.exceptions.ChunkedEncodingError , requests.exceptions.InvalidURL , requests.exceptions.ProxyError , requests.exceptions.Timeout , requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError):pass
        except Exception as JQ:
            print('[-] Bad Requests Complete..')
            with self.file_lock:
                with open(f'redzapp_accounts/ERRORS_Exception.txt', 'a' , encoding='utf-8' , errors='ignore') as wr:
                    wr.write(f"complete: {JQ}\n")
    def verify_email(self, keycloak_id , code, device_id , email , username, ios_user_agent, os_version, proxy):
        print("[+] Verifying email...")
        try:
            data = {"keycloak_id":keycloak_id,"verification_code":code}
            verify = requests.post('https://authentication.redzapp.net/api/auth/action/verify' , headers=self.get_headers(device_id, ios_user_agent), json=data,proxies=proxy, timeout=10)
            if ('"message":"Account is verified"' in verify.text):
                self.complete(keycloak_id, code, device_id , email , username, ios_user_agent, os_version, proxy)
            else:
                print("[-] Email verification failed")
                with self.file_lock:
                    with open(f'redzapp_accounts/ERRORS_requests.txt', 'a' , encoding='utf-8' , errors='ignore') as wr:
                        wr.write(f"verify_email: {verify.text}\n")
        except (requests.exceptions.ConnectionError , requests.exceptions.ReadTimeout , requests.exceptions.ChunkedEncodingError , requests.exceptions.InvalidURL , requests.exceptions.ProxyError , requests.exceptions.Timeout , requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError):
                print('[-] Bad Requests [Proxys]..')
        except Exception as JQ:
            print('[-] Bad Requests Verify..')
            with self.file_lock:
                with open(f'redzapp_accounts/ERRORS_Exception.txt', 'a' , encoding='utf-8' , errors='ignore') as wr:
                    wr.write(f"verify_email: {JQ}\n")
    def Create_Accounts(self):
        while self.ERUN:
            proxy = self.get_proxy()
            try:
                print("[+] Creating account...")
                creating_mails = creating_emails()
                email = creating_mails.create()
                if not email:
                    print("[-] Failed to generate email")
                    continue
                if self.current_settings.get('username_L') == '3':
                    username= str(''.join((choice(self.TKN) for i in range(3))))
                elif self.current_settings.get('username_L') == '4':
                    username= str(''.join((choice(self.TKN) for i in range(4))))
                else:
                    username= str(''.join((choice(self.TKN) for i in range(random.randint(5, 6)))))
                device_id = str(uuid.uuid4()).upper()
                os_version = random.choice(self.ios)
                ios_user_agent = f'Redz/5.5.4 (com.homyt.thex; build:0; iOS {os_version}) Alamofire/{random.choice(self.Alamofire)}'
                data = {"os_version":os_version,"username":username,"mobile_version":"5.5.4","email":email,"device_id":device_id,"os":"IOS"}
                create = requests.post('https://authentication.redzapp.net/api/v2/auth/register/initiate' , headers=self.get_headers(device_id, ios_user_agent) , json=data, proxies=proxy, timeout=10)
                if ('"message":"Waiting for verification"' in create.text):
                    keycloak_id = create.json()['data']['keycloak_id']
                    print("[!] Waiting for verification code...")
                    code = creating_mails.get_inbox(email)
                    if code:
                        self.verify_email(keycloak_id , code , device_id , email , username, ios_user_agent , os_version, proxy)
                    else:
                        print("[-] Verification code timeout/failed")
                elif ('"This username is taken"' in create.text or '"The username field format is invalid."' in create.text):
                    print(f'[-] This username is taken {username}')
                elif ('"Client temporarily blocked"' in create.text):
                    print('[-] Bad Requests [Proxys]..')
                else:
                    print("[-] Account creation failed")
                    with self.file_lock:
                        with open(f'redzapp_accounts/ERRORS_requests.txt', 'a' , encoding='utf-8' , errors='ignore') as wr:
                            wr.write(f"Create_Accounts: {create.text}\n")
            except (requests.exceptions.ConnectionError , requests.exceptions.ReadTimeout , requests.exceptions.ChunkedEncodingError , requests.exceptions.InvalidURL , requests.exceptions.ProxyError , requests.exceptions.Timeout , requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError):
                print('[-] Bad Requests [Proxys]..')
            except Exception as JQ:
                print('[-] Bad Requests..')
                with self.file_lock:
                    with open(f'redzapp_accounts/ERRORS_Exception.txt', 'a' , encoding='utf-8' , errors='ignore') as wr:
                        wr.write(f"Create_Accounts: {JQ}\n")
    def normalize_proxy_any(self , raw: str) -> str:
        prx = raw.strip()
        if prx.lower().startswith("http://"):
            prx = prx[7:]
        elif prx.lower().startswith("https://"):
            prx = prx[8:]
        host = port = user = passwd = None
        if "@" in prx:
            left, right = prx.split("@", 1)
            def is_hostport(s: str) -> bool:
                if ":" not in s: return False
                hp = s.split(":", 1)
                return hp[1].isdigit()
            if is_hostport(right):
                user, passwd = left.split(":", 1)
                host, port = right.split(":", 1)
            else:
                host, port = left.split(":", 1)
                user, passwd = right.split(":", 1)
        else:
            parts = prx.split(":", 3)
            if len(parts) == 2:
                host, port = parts
            elif len(parts) == 4:
                if parts[1].isdigit():
                    host, port, user, passwd = parts
                else:
                    user, passwd, host, port = parts
            else:
                return "Invalid proxy format"
        if not host or not port:
            return "Invalid proxy format"
        if user is not None and passwd is not None:
            user_enc = quote(user, safe="")
            pass_enc = quote(passwd, safe="")
            url = f"http://{user_enc}:{pass_enc}@{host}:{port}"
        else:
            if len(host) >= 8:
                url = f"http://{host}:{port}"
            else:
                url = f"http://{port}:{host}"
        return url
    def check_proxy(self):
        px = 'proxy.txt'
        self.proxy_list = []
        if os.path.isfile(px):
            with open(px, 'r' , encoding='utf-8' , errors='ignore') as proxy_file:
                for i in proxy_file.read().splitlines():
                    norm = self.normalize_proxy_any(i)
                    if norm != "Invalid proxy format":
                        self.proxy_list.append(norm)
    def thr(self): 
        self.check_proxy()
        if not self.proxy_list:
            print("[-] No valid proxies found in proxy.txt!")
            return
        thread = []
        os.system('cls' if os.name == 'nt' else 'clear')
        for _ in range(70):
            th = Thread(target=self.Create_Accounts)
            th.start()
            thread.append(th)
        for i in thread:
            i.join()
def logo():
    return r"""
               _                                       _                        _             
              | |                                     | |                      | |            
  _ __ ___  __| |______ _ _ __  _ __ ______ __ _ _   _| |_ ___  _ __ ___   __ _| |_ ___  _ __ 
 | '__/ _ \/ _` |_  / _` | '_ \| '_ \______/ _` | | | | __/ _ \| '_ ` _ \ / _` | __/ _ \| '__|
 | | |  __/ (_| |/ / (_| | |_) | |_) |    | (_| | |_| | || (_) | | | | | | (_| | || (_) | |   
 |_|  \___|\__,_/___\__,_| .__/| .__/      \__,_|\__,_|\__\___/|_| |_| |_|\__,_|\__\___/|_|   
                         | |   | |                                                            
                         |_|   |_|                                                            
"""
def Settings():
    current_settings = load_settings()
    os.system('cls' if os.name == 'nt' else 'clear')
    sty = input(f"""{logo()} ~~~~ Tool settings ~~~~
    1) Activate the system for sending followers to your account (Current: {current_settings.get('Activate')})
    2) Username length (Current: {current_settings.get('username_L')})
    3) Add a username (Current: {current_settings.get('username')})
    4) Add a post link (Current: {current_settings.get('urlPost')})
    5) To Back ..
  choose : """)
    if sty == '1':
        activate = input("[+] To activate, send (on); to deactivate, send (off) : ").strip()
        if activate.lower() in ['on', 'off']:
            current_settings['Activate'] = activate.lower()
            save_settings(current_settings)
            print('[+] Settings updated successfully...')
        else:
            print('[-] Invalid input! Please enter (on) or (off).')
        Settings()
    elif sty == '2':
        users = input("[+] Choose the desired username length [1- 3L , 2- 4L , 3- random(5/6)] : ").strip()
        if users == '1':
            current_settings['username_L'] = '3'
            save_settings(current_settings)
            print('[$] The username has been saved.')
        elif users == '2':
            current_settings['username_L'] = '4'
            save_settings(current_settings)
            print('[$] The username has been saved.')
        elif users == '3':
            current_settings['username_L'] = 'random'
            save_settings(current_settings)
            print('[$] The username has been saved.')
        Settings()
    elif sty == '3':
        Target = input("[+] Enter a username to send followers to : ").strip()
        if Target:
            current_settings['username'] = Target
            save_settings(current_settings)
            print('[$] The username has been saved.')
        Settings()
    elif sty == '4':
        LINK = input("[+] Enter the link to the post you want to send likes to. : ").strip()
        if LINK:
            current_settings['urlPost'] = LINK
            save_settings(current_settings)
            print("[$] The link has been saved.")
        Settings()
    else: return main()
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    mode = input(f"""{logo()}
    1) Creating new accounts (The ability to send friend requests to your account or likes to your post.)
    2) Tool settings (Add your username + add the post link.)
    0) Closing
  choose : """)
    if mode == '1':Redzapp_Accounts()
    elif mode == '2':Settings()
if __name__ == '__main__':
    load_settings()
    os.makedirs('redzapp_accounts', exist_ok=True)
    main()
