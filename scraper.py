import requests
from bs4 import BeautifulSoup
import random
import time

# إعدادات الربط
BASE_URL = "https://ammarninja.pythonanywhere.com"
API_ENDPOINT = f"{BASE_URL}/api/add_car"
API_KEY = "ninja_bot_password_2025" 
SOURCE_URL = "https://en.bidfax.info/list/sort/date_desc/"

def run_mission():
    print(f"🕵️‍♂️ Connecting to Bidfax...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(SOURCE_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        car_cards = soup.select('.short-poster')
        
        print(f"🔎 Found {len(car_cards)} cars.")

        for card in car_cards[:5]: # هنسحب أول 5 عربيات
            try:
                title = card.select_one('.short-teaser-title a').text.strip()
                link = card.select_one('.short-teaser-title a')['href']
                image = card.select_one('.short-img img')['src']
                if not image.startswith('http'): image = f"https://en.bidfax.info{image}"
                
                # استخراج VIN حقيقي من الرابط
                vin = "UNKNOWN"
                for part in link.split('/'):
                    if len(part) == 17: vin = part.upper(); break
                
                # لو معرفناش نطلعه، نكتب واحد مميز عشان نعرف
                if vin == "UNKNOWN": vin = f"REAL{random.randint(10000,99999)}"

                car_data = {
                    "vin": vin,
                    "title": title,
                    "price": "$0 Call for Price",
                    "image_url": image,
                    "source_url": link,
                    "damage_type": "Accident/Salvage"
                }
                
                # إرسال للموقع
                requests.post(API_ENDPOINT, json=car_data, headers={'X-API-KEY': API_KEY})
                print(f"✅ Sent: {title}")
                time.sleep(1)
                
            except Exception as e:
                print(e)
                continue

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_mission()
