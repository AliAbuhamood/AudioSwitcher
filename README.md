# 🎧 Audio Switcher

برنامج صغير للويندوز يعرض لك كل البرامج الي تطلع صوت، وتقدر **تسحب أي برنامج بين السماعة والسبيكر** بسهولة.
مثلاً: اللعبة على السماعة، و Discord على السبيكر.

## المميزات
- نافذة صغيرة بعمودين: 🎧 سماعة و 🔊 سبيكر
- اسحب البرنامج من عمود للثاني وينتقل صوته فوراً
- تختار أجهزتك مرة وحدة ويحفظها
- ما يحتاج تنصيب، ملف exe واحد

## التحميل والتشغيل
1. روح لصفحة [**Releases**](../../releases) ونزّل `AudioSwitcher.exe`.
2. شغّله (دبل كليك).
3. اختار سماعتك والسبيكر من القوائم فوق.
4. اسحب البرامج بين العمودين.

> البرنامج لازم يكون يطلع صوت عشان يظهر في القائمة.

## ملاحظات
- **ويندوز ممكن يحذّر** (SmartScreen) لأن البرنامج غير موقّع. اضغط **More info ← Run anyway**.
- بعض مضادات الفيروسات تعلّم على برامج PyInstaller بالغلط. الكود مفتوح وتقدر تراجعه بنفسك.
- **Discord:** خلّ Output Device على **Default** في إعداداته، وأعد تشغيله بعد تغيير الجهاز.
- البرنامج **ما يعدل ولا يحقن أي لعبة أو برنامج**، هو بس يغير جهاز الإخراج لكل برنامج (مثل Volume Mixer في ويندوز). ومع ذلك استخدامه على مسؤوليتك مع الألعاب الي فيها حماية.

## البناء من الكود
1. ثبّت [Python](https://www.python.org/) (فعّل *Add Python to PATH*).
2. نزّل **SoundVolumeView** (نسخة x64) من [nirsoft.net](https://www.nirsoft.net/utils/sound_volume_view.html) وحط `SoundVolumeView.exe` في نفس المجلد.
3. شغّل `build.bat`، والناتج بيكون في `dist\AudioSwitcher.exe`.

## الشكر
يعتمد على أداة **SoundVolumeView** من [NirSoft](https://www.nirsoft.net) لتغيير جهاز الصوت لكل برنامج. الأداة مو مالتي وحقوقها لأصحابها.

---

## English

A small Windows tool that lists every app playing audio and lets you **drag each app between your headphones and your speakers**.
Example: game on headphones, Discord on speakers.

### Features
- Compact window with two columns: 🎧 Headphones and 🔊 Speaker
- Drag an app from one column to the other and its audio moves instantly
- Pick your devices once, it remembers them
- No installation, a single exe

### Download & use
1. Go to [**Releases**](../../releases) and download `AudioSwitcher.exe`.
2. Run it.
3. Choose your headphones and speaker at the top.
4. Drag apps between the columns.

> An app only shows up while it is playing audio.

### Notes
- **Windows SmartScreen may warn you** because the exe is unsigned. Click **More info → Run anyway**.
- Some antivirus tools falsely flag PyInstaller executables. The source is open so you can review it.
- **Discord:** set its Output Device to **Default** and restart it after changing the device.
- The tool **does not modify or inject into any game or app**. It only changes the output device per app, like the Windows Volume Mixer. Still, use it at your own risk with games that have anti-cheat.

### Build from source
1. Install [Python](https://www.python.org/) (check *Add Python to PATH*).
2. Download **SoundVolumeView** (x64) from [nirsoft.net](https://www.nirsoft.net/utils/sound_volume_view.html) and put `SoundVolumeView.exe` in the same folder.
3. Run `build.bat`. The result is `dist\AudioSwitcher.exe`.

### Credits
Relies on **SoundVolumeView** by [NirSoft](https://www.nirsoft.net) to set the audio device per app. That tool is not mine and belongs to its author.
