import requests
from bs4 import BeautifulSoup
import random
import time

# 1. إعدادات الهدف (موقعك)
BASE_URL = "https://ammarninja.pythonanywhere.com"
API_ENDPOINT = f"{BASE_URL}/api/add_car"
API_KEY = "ninja_bot_password_2025" 

# المصدر اللي هنسرق منه (أرشيف الحوادث)
SOURCE_URL = "https://en.bidfax.info/list/sort/date_desc/"

def get_real_cars():
    print(f"🕵️‍♂️ Accessing Source: {SOURCE_URL}...")
    
    # بنعمل نفسنا متصفح حقيقي عشان ميتعملش لينا بلوك
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(SOURCE_URL, headers=headers)
        if response.status_code != 200:
            print("❌ Failed to reach source.")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        cars_found = []
        
        # تجميع كروت العربيات من الصفحة
        car_cards = soup.select('.short-poster')
        
        print(f"🔎 Found {len(car_cards)} potential cars...")

        for card in car_cards[:5]: # هناخد أول 5 عربيات بس عشان السيرفر
            try:
                # استخراج البيانات بدقة
                title = card.select_one('.short-teaser-title a').text.strip()
                link = card.select_one('.short-teaser-title a')['href']
                image = card.select_one('.short-img img')['src']
                
                # تصليح رابط الصورة لو جاي ناقص
                if not image.startswith('http'):
                    image = f"https://en.bidfax.info{image}"
                
                # بيانات عشوائية لتكملة "الحبكة"
                damages = ['Front End', 'Rear End', 'Rollover', 'Undercarriage', 'Flood']
                
                # استخراج رقم الشاسيه من الرابط (ذكاء اصطناعي بسيط)
                # الرابط بيكون فيه رقم الشاسيه غالبًا
                vin = "UNKNOWN"
                for part in link.split('/'):
                    if len(part) == 17: # رقم الشاسيه دايما 17 حرف
                        vin = part.upper()
                        break
                
                if vin == "UNKNOWN":
                    vin = f"VIN{random.randint(100000,999999)}REAL"

                car_data = {
                    "vin": vin,
                    "title": title,
                    "price": f"${random.randint(2000, 45000)} USD", # السعر تقديري
                    "image_url": image,
                    "source_url": link,
                    "damage_type": random.choice(damages)
                }
                cars_found.append(car_data)
                
            except Exception as e:
                print(f"⚠️ Skipped a car due to error: {e}")
                continue
                
        return cars_found

    except Exception as e:
        print(f"❌ Critical Error: {e}")
        return []

def run_mission():
    cars = get_real_cars()
    
    if not cars:
        print("🤷‍♂️ No cars found today.")
        return

    print(f"🚚 Shipping {len(cars)} cars to HQ...")
    
    for car in cars:
        headers = {'X-API-KEY': API_KEY}
        try:
            r = requests.post(API_ENDPOINT, json=car, headers=headers)
            if r.status_code == 201:
                print(f"✅ Uploaded: {car['title']}")
            elif r.status_code == 200:
                print(f"⚠️ Exists: {car['title']}")
            else:
                print(f"❌ Failed: {r.text}")
        except:
            pass
        time.sleep(1)

if __name__ == "__main__":
    run_mission()
