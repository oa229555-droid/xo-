#!/bin/bash

# ============================================
# سكريبت تثبيت أداة Virtual Number Hacker
# للاستخدام في Termux
# ============================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}🔥 تثبيت أداة Virtual Number Hacker 🔥${NC}"
echo -e "${GREEN}============================================${NC}"

# التحقق من وجود Termux
if [ ! -d "/data/data/com.termux" ] && [ ! -d "$PREFIX" ]; then
    echo -e "${YELLOW}تحذير: يبدو أنك لست في Termux${NC}"
    echo -e "${YELLow}قد تحتاج لتعديل بعض الأوامر${NC}"
fi

# تحديث الحزم
echo -e "${GREEN}[1/5] تحديث الحزم...${NC}"
pkg update -y && pkg upgrade -y

# تثبيت Python
echo -e "${GREEN}[2/5] تثبيت Python...${NC}"
pkg install python -y
pkg install python-pip -y

# تثبيت المكتبات المطلوبة
echo -e "${GREEN}[3/5] تثبيت المكتبات المطلوبة...${NC}"
pip install --upgrade pip
pip install requests beautifulsoup4 fake-useragent phonenumbers schedule python-telegram-bot colorama

# إنشاء مجلد للأداة
echo -e "${GREEN}[4/5] تجهيز ملفات الأداة...${NC}"
if [ ! -f "vnh.py" ]; then
    echo -e "${RED}ملف vnh.py غير موجود!${NC}"
    echo -e "${YELLow}الرجاء تحميل الملف من GitHub${NC}"
else
    # إعطاء صلاحيات التنفيذ
    chmod +x vnh.py
    
    # إنشاء اختصار للتشغيل السريع
    echo 'python vnh.py' > run.sh
    chmod +x run.sh
fi

# رسالة النجاح
echo -e "${GREEN}[5/5] التثبيت اكتمل بنجاح!${NC}"
echo -e "${GREEN}============================================${NC}"
echo -e "${YELLOW}لتشغيل الأداة:${NC}"
echo -e "  python vnh.py"
echo -e "  أو"
echo -e "  ./run.sh"
echo -e "${GREEN}============================================${NC}"

# عرض معلومات الاستخدام
echo -e "\n${GREEN}📱 الأوامر المتاحة:${NC}"
echo -e "  /number - الحصول على رقم"
echo -e "  /israeli - رقم إسرائيلي"
echo -e "  /usa - رقم أمريكي"
echo -e "  /safeum - رقم SafeUM"
echo -e "  /help - المساعدة"
echo -e "${GREEN}============================================${NC}"
