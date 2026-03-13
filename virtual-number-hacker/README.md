# Virtual Number Hacker (VNH) 🔥

أداة للحصول على أرقام افتراضية مجانية من مصادر متعددة، مخصصة للاستخدام في Termux.

## 📱 المميزات

- ✅ الحصول على أرقام إسرائيلية (+972)
- ✅ الحصول على أرقام أمريكية (+1)
- ✅ استخراج أرقام من OnlineSim
- ✅ قاعدة بيانات محلية لتخزين الأرقام
- ✅ واجهة عربية سهلة
- ✅ مجاني 100% - بدون مفاتيح API

## ⚡ طريقة التثبيت في Termux

### الطريقة السريعة (نسخ ولصق)

```bash
# 1. تحديث الحزم
pkg update && pkg upgrade -y

# 2. تثبيت git
pkg install git -y

# 3. تحميل الأداة
git clone https://github.com/yourusername/virtual-number-hacker.git

# 4. الدخول للمجلد
cd virtual-number-hacker

# 5. تشغيل سكريبت التثبيت
chmod +x install.sh
./install.sh

# 6. تشغيل الأداة
python vnh.py
