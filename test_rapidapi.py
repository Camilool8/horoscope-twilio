#!/usr/bin/env python3
"""
Test script for RapidAPI horoscope integration with Google Translate
Run this to verify your API key and connection before deploying
"""
import os
import requests
import asyncio
from googletrans import Translator

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

async def test_horoscope_api_with_translation(sign):
    """Test fetching horoscope from RapidAPI and translating to Spanish"""
    print(f"\n🔍 Testing {sign.upper()} horoscope with translation...")
    
    try:
        url = "https://horoscope-astrology.p.rapidapi.com/horoscope"
        
        headers = {
            'x-rapidapi-host': RAPIDAPI_HOST,
            'x-rapidapi-key': RAPIDAPI_KEY
        }
        
        params = {
            'day': 'today',
            'sunsign': sign.lower()
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        print(f"API Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            horoscope = data.get('horoscope', 'No horoscope found')
            print(f"✅ English Horoscope fetched successfully!")
            print(f"📜 Original ({sign.upper()}): {horoscope}")
            
            print(f"\n🌐 Testing Google Translate...")
            async with Translator() as translator:
                result = await translator.translate(horoscope, dest='es', src='en')
                spanish_horoscope = result.text
                
                print(f"✅ Translation successful!")
                print(f"🇪🇸 Spanish ({sign.upper()}): {spanish_horoscope}")
                
                personal_messages = {
                    'cancer': f"🦀 Querida Cáncer: {spanish_horoscope}",
                    'aquarius': f"🏺 Hermoso Acuario: {spanish_horoscope}"
                }
                
                final_message = personal_messages.get(sign.lower(), f"✨ {spanish_horoscope}")
                print(f"💕 Final Message: {final_message}")
                
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Request Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Translation Error: {e}")
        return False

async def test_translation_only():
    """Test Google Translate independently"""
    print(f"\n🌐 Testing Google Translate independently...")
    
    try:
        test_texts = [
            "Today is a great day for love and creativity.",
            "Your intuition will guide you to make the right decisions.",
            "Focus on your relationships and family today."
        ]
        
        async with Translator() as translator:
            for i, text in enumerate(test_texts, 1):
                result = await translator.translate(text, dest='es', src='en')
                print(f"✅ Test {i}: '{text}' → '{result.text}'")
        
        print(f"✅ Google Translate is working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Translation Error: {e}")
        return False

def test_twilio_config():
    """Test Twilio configuration (without sending SMS)"""
    print("\n📱 Testing Twilio configuration...")
    
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        
        client = Client(account_sid, auth_token)
        
        account = client.api.accounts(account_sid).fetch()
        print(f"✅ Twilio connection successful!")
        print(f"Account Name: {account.friendly_name}")
        print(f"Account Status: {account.status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Twilio Error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🌟 Testing Horoscope Application with Google Translate")
    print("=" * 60)
    
    translate_success = await test_translation_only()
    
    cancer_success = await test_horoscope_api_with_translation('cancer')
    aquarius_success = await test_horoscope_api_with_translation('aquarius')
    
    twilio_success = test_twilio_config()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"Google Translate: {'✅ PASS' if translate_success else '❌ FAIL'}")
    print(f"Cancer API + Translation: {'✅ PASS' if cancer_success else '❌ FAIL'}")
    print(f"Aquarius API + Translation: {'✅ PASS' if aquarius_success else '❌ FAIL'}")
    print(f"Twilio Config: {'✅ PASS' if twilio_success else '❌ FAIL'}")
    
    if all([translate_success, cancer_success, aquarius_success, twilio_success]):
        print("\n🎉 All tests passed! Your configuration is ready!")
        print("✨ Now your horoscopes will be properly translated to Spanish!")
        print("💕 Your girlfriend will receive beautiful Spanish horoscopes daily!")
    else:
        print("\n⚠️  Some tests failed. Please check:")
        if not translate_success:
            print("   - Internet connection for Google Translate")
        if not cancer_success or not aquarius_success:
            print("   - RapidAPI key and connection")
        if not twilio_success:
            print("   - Twilio credentials")

if __name__ == "__main__":
    asyncio.run(main())