# YouTube to MP3/MP4 Converter + Playlist Support

โปรแกรม GUI สำหรับดาวน์โหลดวิดีโอจาก YouTube และแปลงเป็นไฟล์ MP3 หรือ MP4 รองรับการดาวน์โหลด Playlist ทั้งหมด

## ฟีเจอร์

- ✅ **EXE File พร้อมใช้งาน** - ไม่ต้องติดตั้ง Python!
- ✅ ดาวน์โหลดวิดีโอจาก YouTube
- ✅ แปลงเป็นไฟล์ **MP3** หรือดาวน์โหลดเป็น **MP4**
- ✅ **📁 Playlist Support** - ดาวน์โหลด YouTube Playlist ทั้งหมด!
- ✅ GUI ที่ใช้งานง่าย ด้วย Radio Button และ Checkbox
- ✅ เลือกคุณภาพได้ (ทั้งเสียงและวิดีโอ)
- ✅ **Progress Bar แบบละเอียด** - แสดงเปอร์เซ็นต์, ความเร็ว, เวลาที่เหลือ
- ✅ **Auto Organization** - จัดเก็บไฟล์ playlist ในโฟลเดอร์แยกตามชื่อ playlist
- ✅ Log การทำงานแบบละเอียด
- ✅ เปิดโฟลเดอร์ดาวน์โหลดได้
- ✅ รองรับ URL YouTube ทุกรูปแบบ

## ความต้องการของระบบ

- Windows 10/11
- สำหรับ EXE File: ไม่ต้องติดตั้งอะไรเพิ่ม
- สำหรับ Python Source: Python 3.8 หรือใหม่กว่า

## การใช้งาน

### 🚀 วิธีที่ 1: ใช้งาน EXE File (แนะนำ - ไม่ต้องติดตั้ง Python)

1. ดาวน์โหลดไฟล์ `YouTube_to_MP3_Converter.exe` จากโฟลเดอร์ `dist/`
2. ดับเบิลคลิกที่ไฟล์ `YouTube_to_MP3_Converter.exe` เพื่อเริ่มโปรแกรม

### 🐍 วิธีที่ 2: รันจาก Python Source Code

1. รันโปรแกรม:
```bash
python youtubeToMp3.py
```

### 📋 ขั้นตอนการใช้งาน:

1. **วาง YouTube URL** ลงในช่อง "YouTube URL"
2. **เลือกรูปแบบไฟล์**: 
   - 🎵 **MP3** (เสียงอย่างเดียว) 
   - 🎬 **MP4** (วิดีโอพร้อมเสียง)
3. **เลือกโหมด Playlist**: ☑️ ถ้าต้องการดาวน์โหลดทั้ง playlist
4. **เลือกโฟลเดอร์** ที่ต้องการเก็บไฟล์ (ถ้าต้องการ)
5. **เลือกคุณภาพ**:
   - **MP3**: best, 320, 256, 192, 128 kbps
   - **MP4**: best, 1080p, 720p, 480p, 360p

5. **คลิก** "Download & Convert to MP3" หรือ "Download as MP4"
6. **รอให้ดาวน์โหลดเสร็จ** (จะเห็นความคืบหน้าแบบละเอียด)

## ความต้องการของระบบ

- Windows 10/11
- Python 3.8 หรือใหม่กว่า
- FFmpeg (จะติดตั้งอัตโนมัติผ่าน yt-dlp)

## การติดตั้ง (สำหรับ Developer)

### ติดตั้ง Dependencies

1. ดาวน์โหลดโค้ดมาที่เครื่อง
2. เปิด Command Prompt หรือ PowerShell
3. เข้าไปที่โฟลเดอร์ที่เก็บโค้ด
4. รันคำสั่ง:

```bash
pip install -r requirements.txt
```

### สร้าง EXE File

สามารถ build เป็น EXE file เพื่อแจกยายได้โดยไม่ต้องติดตั้ง Python:

**วิธีที่ 1: ใช้ Batch File**
```bash
build_exe.bat
```

**วิธีที่ 2: Manual Command**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "YouTube_to_MP3_Converter" youtubeToMp3.py
```
''' bash
 D:/code/python/YoutubeToMp3/.venv/Scripts/pyinstaller.exe --onefile --windowed  --noconsole   --name "YouTube_to_MP3_Converter_v2" youtubeToMp3.py 
'''

6. `dist/YouTube_to_MP3_Converter_Playlist.exe` - ไฟล์ EXE พร้อมใช้งาน + Playlist Support

## การใช้งาน

1. รันโปรแกรม:
```bash
python youtubeToMp3.py
```

2. วาง YouTube URL ในช่อง "YouTube URL"
3. เลือกโฟลเดอร์ที่ต้องการเก็บไฟล์ (ถ้าต้องการ)
4. เลือกคุณภาพเสียง:
   - **best**: คุณภาพดีที่สุด
   - **320**: 320 kbps
   - **256**: 256 kbps  
   - **192**: 192 kbps
   - **128**: 128 kbps

5. คลิก "Download & Convert to MP3"
6. รอให้ดาวน์โหลดและแปลงเสร็จ

## ฟีเจอร์ที่มีใน GUI

### หน้าจอหลัก
- **YouTube URL**: ช่องใส่ลิงก์ YouTube
- **Paste Button**: ปุ่มแปะลิงก์จาก clipboard
- **Output Folder**: เลือกโฟลเดอร์ที่จะเก็บไฟล์
- **Audio Quality**: เลือกคุณภาพเสียง
- **Progress Bar**: แสดงความคืบหน้าการดาวน์โหลด

### ปุ่มต่างๆ
- **Download & Convert to MP3**: เริ่มดาวน์โหลด
- **Browse**: เลือกโฟลเดอร์เก็บไฟล์
- **Clear Log**: ล้าง log
- **Open Download Folder**: เปิดโฟลเดอร์ดาวน์โหลด

## ข้อมูลเพิ่มเติม

- ไฟล์ MP3/MP4 จะถูกเก็บที่: `~/Downloads/YouTube_MP3/` (โดยค่าเริ่มต้น)
- **📁 Playlist Organization**: ไฟล์ playlist จะถูกจัดเก็บในโฟลเดอร์ย่อยตามชื่อ playlist
- โปรแกรมรองรับ YouTube URL ทุกรูปแบบ (ทั้ง video เดี่ยวและ playlist)
- มี error handling ที่ดี
- แสดง log แบบละเอียด พร้อม emoji icons
- **Progress แบบละเอียด**: เปอร์เซ็นต์, ความเร็ว, เวลาที่เหลือ, ขนาดไฟล์
- **Smart Naming**: ไฟล์ playlist จะมีหมายเลข index และจัดเรียงลำดับ
- **EXE File**: ใช้งานได้ทันทีโดยไม่ต้องติดตั้ง Python

## การแก้ไขปัญหา

### ถ้าเกิด Error
1. ตรวจสอบว่า URL ถูกต้อง
2. ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
3. ลองรีสตาร์ทโปรแกรม
4. ดู error message ใน log

### ถ้าดาวน์โหลดช้า
- เปลี่ยนคุณภาพเสียง/วิดีโอให้ต่ำลง
- ตรวจสอบความเร็วอินเทอร์เน็ต
- ดูข้อมูล ETA และความเร็วใน progress bar

### สำหรับ EXE File
- ถ้า Windows Defender แจ้งเตือน: คลิก "More info" → "Run anyway"
- ไฟล์ EXE ใหญ่ (21.5 MB) เพราะรวม Python runtime และ libraries ไว้ด้วย

## License

This project is open source and available under the MIT License.