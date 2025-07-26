from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Telegram Bot Token
BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class UserData(BaseModel):
    user_id: str
    language: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Language translations
LANGUAGES = {
    "en": {
        "name": "🇺🇸 English",
        "welcome": "Welcome! This bot helps you access Quran learning programs.",
        "choose_language": "Please choose your language:",
        "main_menu": "Main Menu - Choose an option:",
        "channel": "⭐ Select Channel",
        "admin": "📞 Administration", 
        "register": "📝 Register",
        "education_info": "ℹ️ Education Information",
        "restart": "🔁 Restart",
        "mini_app": "🔷 Learning Portal",
        "education_details": "📚 **Education Program Details:**\n\n📅 Days: 7 days a week\n⏰ Duration: 30 minutes per day\n💰 Cost: 1500 Ethiopian Birr\n\nFor more information, contact administration."
    },
    "am": {
        "name": "🇪🇹 አማርኛ",
        "welcome": "እንኮዋን ደህና መጡ! ይህ ቦት የቁርአን ትምህርት ፕሮግራሞችን ለማግኘት ይረዳዎታል።",
        "choose_language": "እባክዎ ቋንቋዎን ይምረጡ:",
        "main_menu": "ዋና ዝርዝር - አንድ አማራጭ ይምረጡ:",
        "channel": "⭐ ቻናል ምረጥ",
        "admin": "📞 አስተዳደር",
        "register": "📝 ይመዝገቡ", 
        "education_info": "ℹ️ የትምህርት መረጃ",
        "restart": "🔁 እንደገና ጀምር",
        "mini_app": "🔷 የትምህርት መግቢያ",
        "education_details": "📚 **የትምህርት ፕሮግራም ዝርዝሮች:**\n\n📅 ቀናት: በሳምንት 7 ቀን\n⏰ የሚፈጅ ጊዜ: በቀን 30 ደቂቃ\n💰 ዋጋ: 1500 ብር\n\nለተጨማሪ መረጃ፣ አስተዳደርን ያነጋግሩ።"
    },
    "ar": {
        "name": "🇸🇦 العربية",
        "welcome": "أهلاً وسهلاً! يساعدك هذا البوت في الوصول إلى برامج تعلم القرآن.",
        "choose_language": "يرجى اختيار لغتك:",
        "main_menu": "القائمة الرئيسية - اختر خياراً:",
        "channel": "⭐ اختر القناة",
        "admin": "📞 الإدارة",
        "register": "📝 سجل",
        "education_info": "ℹ️ معلومات التعليم",
        "restart": "🔁 إعادة البدء",
        "mini_app": "🔷 بوابة التعلم",
        "education_details": "📚 **تفاصيل البرنامج التعليمي:**\n\n📅 الأيام: 7 أيام في الأسبوع\n⏰ المدة: 30 دقيقة يومياً\n💰 التكلفة: 1500 بر إثيوبي\n\nللمزيد من المعلومات، اتصل بالإدارة."
    },
    "fr": {
        "name": "🇫🇷 Français", 
        "welcome": "Bienvenue! Ce bot vous aide à accéder aux programmes d'apprentissage du Coran.",
        "choose_language": "Veuillez choisir votre langue:",
        "main_menu": "Menu Principal - Choisissez une option:",
        "channel": "⭐ Sélectionner la chaîne",
        "admin": "📞 Administration",
        "register": "📝 S'inscrire",
        "education_info": "ℹ️ Informations éducatives", 
        "restart": "🔁 Redémarrer",
        "mini_app": "🔷 Portail d'apprentissage",
        "education_details": "📚 **Détails du programme éducatif:**\n\n📅 Jours: 7 jours par semaine\n⏰ Durée: 30 minutes par jour\n💰 Coût: 1500 Birr éthiopien\n\nPour plus d'informations, contactez l'administration."
    },
    "so": {
        "name": "🇸🇴 Soomaali",
        "welcome": "Soo dhawaada! Botkan wuxuu kaa caawinyaa inaad hesho barnaamijyada waxbarashada Quraanka.",
        "choose_language": "Fadlan dooro luqaddaada:",
        "main_menu": "Liiska Weyn - Dooro mid:",
        "channel": "⭐ Dooro Channelka",
        "admin": "📞 Maamulka",
        "register": "📝 Isdiiwaangeli",
        "education_info": "ℹ️ Macluumaadka Waxbarashada",
        "restart": "🔁 Dib u bilow",
        "mini_app": "🔷 Albaabka Waxbarashada", 
        "education_details": "📚 **Faahfaahinta Barnaamijka Waxbarashada:**\n\n📅 Maalmaha: 7 maalmood todobaadkii\n⏰ Muddada: 30 daqiiqadood maalintii\n💰 Qiimaha: 1500 Birr Ethiopian\n\nWixii macluumaad dheeraad ah, kala soo xidhiidh maamulka."
    }
}

# Telegram Bot Setup
telegram_app = None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    
    # Save user data to database
    user_data = UserData(
        user_id=str(user.id),
        username=user.username,
        full_name=user.full_name
    )
    await db.users.replace_one(
        {"user_id": str(user.id)}, 
        user_data.dict(), 
        upsert=True
    )
    
    # Send welcome message with mosque image
    mosque_image_url = "https://images.unsplash.com/photo-1512970648279-ff3398568f77?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwyfHxtb3NxdWV8ZW58MHx8fHwxNzUzNTMxNTc2fDA&ixlib=rb-4.1.0&q=85"
    
    welcome_text = """
🕌 ኣስላም ዐላይኹም ወ ረሕመቱላሒ ወ በረካቱ

እንኮዋን ወደ የቁርአን ትምህርት ቦት ደህና መጡ!

በዚህ ቦት ላይ የሚያገኟቸው አገልግሎቶች:
✅ ቁርአን ማንበብ እና መዘከር (ተጅዊድ፣ ሂፍዝ፣ ቃኢዳ፣ ኢጅዛ)
✅ ተጅዊድ (ተከክለኛው የቁርአን አነባበብ መማር)
✅ ሂፍዝ (ቁርአንን በቅርበት መዘከር)
✅ ኢጅዛ (ፈተናና ፍቃድ የማግኘት ዕድል)

ለመጀመር ከታች ያለውን ቁልፍ ይጫኑ 👇
"""
    
    keyboard = [[InlineKeyboardButton("🚀 ጀምር", callback_data="start_bot")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_photo(
        photo=mosque_image_url,
        caption=welcome_text,
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_lang = context.user_data.get('language', 'am')
    
    if query.data == "start_bot":
        # Show language selection
        keyboard = []
        for lang_code, lang_data in LANGUAGES.items():
            keyboard.append([InlineKeyboardButton(lang_data["name"], callback_data=f"lang_{lang_code}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption="እባክዎ ቋንቋዎን ይምረጡ / Please choose your language:",
            reply_markup=reply_markup
        )
    
    elif query.data.startswith("lang_"):
        # Set language and show main menu
        lang_code = query.data.split("_")[1]
        context.user_data['language'] = lang_code
        
        # Update user language in database
        await db.users.update_one(
            {"user_id": str(query.from_user.id)},
            {"$set": {"language": lang_code}}
        )
        
        await show_main_menu(query, lang_code)
    
    elif query.data == "main_menu":
        await show_main_menu(query, user_lang)
    
    elif query.data == "channel":
        channel_url = "https://t.me/channelname"
        await query.edit_message_caption(
            caption=f"📺 {LANGUAGES[user_lang]['channel']}\n\n{channel_url}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 ወደ ዋና ዝርዝር", callback_data="main_menu")
            ]])
        )
    
    elif query.data == "admin":
        admin_url = "https://t.me/adminusername"
        await query.edit_message_caption(
            caption=f"👨‍💼 {LANGUAGES[user_lang]['admin']}\n\n{admin_url}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 ወደ ዋና ዝርዝር", callback_data="main_menu")
            ]])
        )
    
    elif query.data == "register":
        admin_url = "https://t.me/adminusername" 
        await query.edit_message_caption(
            caption=f"📝 {LANGUAGES[user_lang]['register']}\n\nለምዝገባ አስተዳደርን ያነጋግሩ:\n{admin_url}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 ወደ ዋና ዝርዝር", callback_data="main_menu")
            ]])
        )
    
    elif query.data == "education_info":
        await query.edit_message_caption(
            caption=LANGUAGES[user_lang]['education_details'],
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 ወደ ዋና ዝርዝር", callback_data="main_menu")
            ]])
        )
    
    elif query.data == "restart":
        # Restart flow - show language selection
        keyboard = []
        for lang_code, lang_data in LANGUAGES.items():
            keyboard.append([InlineKeyboardButton(lang_data["name"], callback_data=f"lang_{lang_code}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_caption(
            caption="እባክዎ ቋንቋዎን ይምረጡ / Please choose your language:",
            reply_markup=reply_markup
        )

async def show_main_menu(query, lang_code):
    """Show the main menu"""
    web_app_url = f"{os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:3000')}"
    
    keyboard = [
        [InlineKeyboardButton(LANGUAGES[lang_code]['channel'], callback_data="channel")],
        [InlineKeyboardButton(LANGUAGES[lang_code]['admin'], callback_data="admin")],
        [InlineKeyboardButton(LANGUAGES[lang_code]['register'], callback_data="register")],
        [InlineKeyboardButton(LANGUAGES[lang_code]['education_info'], callback_data="education_info")],
        [InlineKeyboardButton(LANGUAGES[lang_code]['restart'], callback_data="restart")],
        [InlineKeyboardButton(LANGUAGES[lang_code]['mini_app'], web_app=WebAppInfo(url=web_app_url))]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_caption(
        caption=LANGUAGES[lang_code]['main_menu'],
        reply_markup=reply_markup
    )

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Telegram Bot API is running"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

@api_router.get("/users")
async def get_users():
    users = await db.users.find().to_list(1000)
    return users

# Portal login endpoints
@api_router.post("/login/admin")
async def admin_login(credentials: dict):
    if credentials.get("username") == "admin" and credentials.get("password") == "admin123":
        return {"success": True, "message": "Admin login successful", "role": "admin"}
    return {"success": False, "message": "Invalid credentials"}

@api_router.post("/login/teacher")  
async def teacher_login(credentials: dict):
    if credentials.get("username") == "teacher" and credentials.get("password") == "teacher123":
        return {"success": True, "message": "Teacher login successful", "role": "teacher"}
    return {"success": False, "message": "Invalid credentials"}

@api_router.post("/login/student")
async def student_login(credentials: dict):
    if credentials.get("username") == "student" and credentials.get("password") == "student123":
        return {"success": True, "message": "Student login successful", "role": "student"}
    return {"success": False, "message": "Invalid credentials"}

# Include the router in the main app
app.include_router(api_router)

# Serve static files from frontend build
app.mount("/", StaticFiles(directory="/app/frontend/build", html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Start the Telegram bot when FastAPI starts"""
    global telegram_app
    try:
        telegram_app = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        telegram_app.add_handler(CommandHandler("start", start_command))
        telegram_app.add_handler(CallbackQueryHandler(button_callback))
        
        # Start polling in background
        await telegram_app.initialize()
        await telegram_app.start()
        await telegram_app.updater.start_polling()
        
        logger.info("Telegram bot started successfully")
    except Exception as e:
        logger.error(f"Failed to start Telegram bot: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the Telegram bot when FastAPI shuts down"""
    global telegram_app
    if telegram_app:
        await telegram_app.updater.stop()
        await telegram_app.stop()
        await telegram_app.shutdown()
    client.close()