# 🌱 SEED DATABASE ON RENDER

Hướng dẫn seed dữ liệu production vào database trên Render.

---

## 🎯 Vấn đề

Database trên Render đã có tables nhưng **chưa có dữ liệu**. Frontend hiển thị trống vì backend không có data để trả về.

---

## ✅ Giải pháp: Auto-Seed (Tự động)

Backend đã được config để **tự động seed database** khi start lần đầu.

### **Cách hoạt động:**

1. Backend start → Check database có data chưa
2. Nếu database trống + `AUTO_SEED_DB=true` → Tự động chạy seed script
3. Database được populate với production data
4. Frontend sẽ hiển thị data ngay lập tức

### **Đã được enable trong `render.yaml`:**

```yaml
envVars:
  - key: AUTO_SEED_DB
    value: true  # ← Enable auto-seed
```

### **Verify auto-seed hoạt động:**

1. **Check Backend Logs trên Render:**
   - Tab "Logs" trong backend service
   - Tìm dòng:
     ```
     🌱 Database is empty, running auto-seed...
     🚀 Starting database seeding...
     ✅ Created 7 production jobs
     ✅ Created 2 production interviews
     ✅ Created 3 email templates
     ✅ Auto-seed completed successfully
     ```

2. **Test Frontend:**
   - Mở: `https://your-frontend.onrender.com`
   - Vào "Quản Lý Jobs" → thấy 7 jobs
   - Vào "Thống Kê Tổng Quan" → thấy charts có data

---

## 🔄 Manual Seed (Nếu cần)

Nếu auto-seed không chạy hoặc muốn re-seed:

### **Cách 1: Trigger Redeploy**

1. Vào Backend Service trên Render
2. Click **"Manual Deploy"** → **"Clear build cache & deploy"**
3. Backend sẽ redeploy và tự động seed (nếu DB vẫn trống)

### **Cách 2: Dùng Build Command**

Update `render.yaml` để seed trong build phase:

```yaml
buildCommand: "pip install -r requirements.txt && python scripts/seed_db_prod.py"
```

⚠️ **Lưu ý:** Cách này sẽ seed lại mỗi lần deploy → có thể duplicate data

---

## 📊 Production Data

Script seed dữ liệu **thực tế cho sinh viên tốt nghiệp**:

| Data Type | Count | Description |
|-----------|-------|-------------|
| **Jobs** | 7 | Realistic job applications with full details |
| **Status Distribution** | - | 1 Applied, 1 Screening, 1 Interview, 2 Offers, 1 Rejected, 1 Withdrawn |
| **Interviews** | 2 | 1 Scheduled (VNG), 1 Completed (Phone Screening) |
| **Email Templates** | 3 | Professional templates for follow-up, thank you, acceptance |

### **Job Details:**

1. **VNG Corporation** (Interview) - Backend Engineer, TP.HCM, 25-40M
2. **Tiki** (Screening) - Python Backend, TP.HCM, 20-35M
3. **FPT Software** (Applied) - Junior Backend, Hà Nội, 12-18M
4. **Shopee Vietnam** (Offer) - Backend Intern, TP.HCM, 8-12M
5. **Momo** (Offer) - Software Engineer, TP.HCM, 15-25M
6. **Base.vn** (Rejected) - Python Developer, Remote
7. **KiotViet** (Withdrawn) - Backend Developer, TP.HCM

### **Production-Ready Features:**

- ✅ Realistic company names và job titles
- ✅ Actual salary ranges cho từng level
- ✅ Real locations (TP.HCM, Hà Nội)
- ✅ Detailed job descriptions
- ✅ Contact information (name, email, phone)
- ✅ Interview details với location cụ thể
- ✅ Notes với context thực tế
- ✅ Timeline hợp lý (5-60 days ago)

---

## 🔧 Disable Auto-Seed

Nếu không muốn auto-seed:

1. **Update Backend env var trên Render:**
   ```
   AUTO_SEED_DB = false
   ```

2. **Hoặc remove khỏi `render.yaml`:**
   ```yaml
   # envVars:
   #   - key: AUTO_SEED_DB
   #     value: true  # ← Comment out hoặc xóa
   ```

---

## 🐛 Troubleshooting

### ❌ Auto-seed không chạy

**Nguyên nhân:**
- Database đã có data (count > 0)
- `AUTO_SEED_DB` không được set hoặc = false

**Fix:**
1. Check env var `AUTO_SEED_DB = true`
2. Nếu DB đã có data, cần clear trước:
   - Connect database trực tiếp
   - Run: `DELETE FROM jobs; DELETE FROM interviews;`
   - Redeploy backend

### ❌ "subprocess failed" error

**Nguyên nhân:**
- Script path không đúng
- Python dependencies chưa install

**Fix:**
- Verify `scripts/seed_db_prod.py` exists in repo
- Check build logs cho pip install errors

---

## 💡 Best Practices

### **For Development:**
- Use local seed script: `python scripts/seed_db.py`
- Có nhiều data hơn để test

### **For Production:**
- Use auto-seed với minimal realistic data
- Disable sau khi có real user data

### **For Demo/Graduation Project:**
- Keep auto-seed enabled
- Data showcase được tính năng của app
- Professional và có ý nghĩa

---

**No Shell access needed! Everything automatic! 🚀**
