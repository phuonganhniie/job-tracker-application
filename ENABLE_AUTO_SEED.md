# ⚡ QUICK START: Enable Auto-Seed on Render

## 🎯 Mục tiêu
Backend sẽ **tự động seed database** khi start lần đầu - không cần Shell access!

---

## 📝 Các bước (2 phút)

### 1️⃣ **Update Backend Environment Variable**

1. **Login Render:** https://dashboard.render.com

2. **Vào Backend Service:**
   - Click service: `job-tracker-backend`

3. **Add Environment Variable:**
   - Tab **"Environment"**
   - Click **"Add Environment Variable"**
   - Thêm:
     ```
     Key: AUTO_SEED_DB
     Value: true
     ```
   - Click **"Save Changes"**

4. **Backend sẽ auto redeploy** (1-2 phút)

---

### 2️⃣ **Verify Auto-Seed**

1. **Check Logs:**
   - Tab **"Logs"**
   - Tìm dòng:
     ```
     🌱 Database is empty, running auto-seed...
     ✅ Created 7 production jobs
     ✅ Created 2 production interviews
     ✅ Created 3 email templates
     ✅ Auto-seed completed successfully
     ```

2. **Test Frontend:**
   - Mở: `https://your-frontend.onrender.com`
   - **Quản Lý Jobs:** 7 jobs hiển thị
   - **Thống Kê:** Charts có data
   - **Phỏng Vấn:** 2 interviews

---

## 🎓 Production Data

### **Jobs (7):**
- ✅ VNG Corporation (Interview) - 25-40M
- ✅ Tiki (Screening) - 20-35M
- ✅ FPT Software (Applied) - 12-18M
- ✅ Shopee Vietnam (Offer) - 8-12M ⭐ Best internship
- ✅ Momo (Offer) - 15-25M ⭐ Best full-time
- ✅ Base.vn (Rejected) - Feedback included
- ✅ KiotViet (Withdrawn) - Focus on better offers

### **Interviews (2):**
- 📞 Phone Screening (Completed) - VNG
- 💻 Technical Interview (Scheduled) - VNG

### **Đặc điểm data:**
- ✨ Realistic salary ranges
- ✨ Real company names
- ✨ Detailed descriptions
- ✨ Contact information
- ✨ Interview notes
- ✨ Job application notes

---

## 🔄 Re-seed (Nếu cần)

Nếu database đã có data và muốn seed lại:

### **Option 1: Manual trigger**

1. Connect database trực tiếp (Render Database tab)
2. Run SQL:
   ```sql
   DELETE FROM interviews;
   DELETE FROM notes;
   DELETE FROM jobs;
   DELETE FROM email_templates;
   ```
3. Restart backend service → Auto-seed sẽ chạy

### **Option 2: Redeploy**

1. Backend service → **"Manual Deploy"**
2. Chọn **"Clear build cache & deploy"**
3. Auto-seed chạy nếu DB trống

---

## 🎯 Done!

Sau khi add env var `AUTO_SEED_DB=true`, backend sẽ:

✅ Check database mỗi lần start
✅ Tự động seed nếu DB trống
✅ Populate 7 jobs + 2 interviews + 3 templates
✅ Frontend hiển thị data ngay lập tức

**No Shell access needed! 🚀**
