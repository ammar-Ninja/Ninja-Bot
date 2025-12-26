import requests
import random
import time

# 1. إعدادات الهدف (موقعك اللايف)
BASE_URL = "https://ammarninja.pythonanywhere.com"
API_ENDPOINT = f"{BASE_URL}/api/add_car"
API_KEY = "ninja_bot_password_2025" 

# 2. دالة توليد عربية "تجربة" (عشان نتأكد إن الماسورة شغالة)
def get_test_car():
    models = ['BMW M3', 'Mercedes G-Class', 'Audi RS6', 'Porsche 911']
    damages = ['Front End', 'Rollover', 'Biohazard', 'Rear End']
    
    return {
        "vin": f"TEST{random.randint(1000, 9999)}VIN",
        "title": f"2024 {random.choice(models)} - Salvage Title",
        "price": f"${random.randint(15000, 85000)} USD",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/e/e8/Wrecked_Ferrari_458_Italia_%2816053073733%29.jpg", # صورة فيراري مخبوطة
        "source_url": "https://www.copart.com",
        "damage_type": random.choice(damages)
    }

def run_mission():
    print(f"🕵️‍♂️ Connecting to HQ: {BASE_URL}...")
    
    # نبعت 3 عربيات في المرة الواحدة
    for _ in range(3):
        car = get_test_car()
        print(f"🚗 Sending Car: {car['title']}...")
        
        headers = {'X-API-KEY': API_KEY}
        try:
            response = requests.post(API_ENDPOINT, json=car, headers=headers)
            if response.status_code == 201:
                print("✅ Success: Uploaded!")
            else:
                print(f"⚠️ Server says: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
            
        time.sleep(1) # راحة ثانية بين كل عربية

if __name__ == "__main__":
    run_mission()
