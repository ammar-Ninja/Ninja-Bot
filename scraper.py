import requests
from bs4 import BeautifulSoup
import random
import time

# إعدادات الربط بموقعك
BASE_URL = "https://ammarninja.pythonanywhere.com"
API_ENDPOINT = f"{BASE_URL}/api/add_car"
API_KEY = "ninja_bot_password_2025" 

# المصدر الحقيقي (Bidfax)
SOURCE_URL = "https://en.bidfax.info/list/sort/date_desc/"

def get_real_cars():
    print(f"🕵️‍♂️ Connecting to Bidfax...")
    # متصفح مزيف عشان الموقع ميعملش بلوك
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(SOURCE_URL, headers=headers)
        if response.status_code != 200:
            print("❌ Failed to reach source.")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        car_cards = soup.select('.short-poster')
        
        print(f"🔎 Found {len(car_cards)} real cars on the page.")
        
        found_cars = []

        for card in car_cards[:5]: # هنسحب أول 5 عربيات حقيقية
            try:
                # استخراج العنوان
                title_tag = card.select_one('.short-teaser-title a')
                title = title_tag.text.strip()
                link = title_tag['href']
                
                # استخراج الصورة
                img_tag = card.select_one('.short-img img')
                image = img_tag['src']
                if not image.startswith('http'):
                    image = f"https://en.bidfax.info{image}"
                
                # استخراج رقم الشاسيه من الرابط
                # الرابط بيبقى شكله: /.../2024-toyota-camry-vin-4t1...html
                vin = "UNKNOWN"
                parts = link.split('-')
                for part in parts:
                    if len(part) == 17 and any(c.isdigit() for c in part):
                        vin = part.upper()
                        break
                
                # لو فشلنا في استخراج الفين، نكتب واحد مميز يبدأ بـ REAL
                if vin == "UNKNOWN":
                    vin = f"REAL{random.randint(100000,999999)}"

                # تجهيز البيانات
                car_data = {
                    "vin": vin,
                    "title": title,
                    "price": "$0 (Check Auction)",
                    "image_url": image,
                    "source_url": link,
                    "damage_type": "Collision/Salvage"
                }
                found_cars.append(car_data)
                
            except Exception as e:
                print(f"Skipped car: {e}")
                continue
                
        return found_cars

    except Exception as e:
        print(f"Error: {e}")
        return []

def run_mission():
    cars = get_real_cars()
    if not cars:
        print("No cars found.")
        return

    print(f"🚚 Sending {len(cars)} REAL cars to your website...")
    
    for car in cars:
        headers = {'X-API-KEY': API_KEY}
        try:
            r = requests.post(API_ENDPOINT, json=car, headers=headers)
            if r.status_code == 201:
                print(f"✅ Uploaded Real Car: {car['title']}")
            else:
                print(f"⚠️ Server response: {r.status_code}")
        except:
            pass
        time.sleep(1)

if __name__ == "__main__":
    run_mission()
