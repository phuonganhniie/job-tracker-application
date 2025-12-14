# 🌱 SEED DATABASE ON RENDER

Hướng dẫn seed dữ liệu mẫu vào database production trên Render.

---

## 🎯 Vấn đề

Database trên Render đã có tables nhưng **chưa có dữ liệu**. Frontend hiển thị trống vì backend không có data để trả về.

---

## ✅ Giải pháp: Chạy Seed Script

### **CÁCH 1: Dùng Render Shell (Khuyến nghị)** ⭐

1. **Vào Backend Service:**
   - Login Render Dashboard: https://dashboard.render.com
   - Click vào service `job-tracker-backend`

2. **Mở Shell:**
   - Click tab **"Shell"** (bên cạnh Logs, Metrics)
   - Hoặc click **"Connect"** → **"Shell"**

3. **Chạy seed script:**
   ```bash
   python scripts/seed_db_prod.py
   ```

4. **Verify output:**
   ```
   🚀 Starting database seeding...
   📊 Database: postgresql://...
   📝 Seeding jobs...
   ✅ Created 10 jobs
   📝 Seeding interviews...
   ✅ Created 2 interviews
   📝 Seeding email templates...
   ✅ Created 2 email templates
   ✅ Database seeded successfully!
   ```

5. **Test:**
   - Reload frontend: `https://your-frontend.onrender.com`
   - Trang "Quản Lý Jobs" sẽ hiển thị 10 jobs
   - Trang "Thống Kê" sẽ có charts

---

### **CÁCH 2: Dùng Render SSH (Nâng cao)**

1. **Enable SSH:**
   - Service Settings → SSH Public Key → Add your SSH key

2. **Connect:**
   ```bash
   ssh <username>@<service-name>.onrender.com
   ```

3. **Run seed:**
   ```bash
   cd /opt/render/project/src
   python scripts/seed_db_prod.py
   ```

---

### **CÁCH 3: Dùng Custom Deploy Script**

Nếu muốn tự động seed mỗi lần deploy:

1. **Update `render.yaml`:**
   ```yaml
   services:
     - type: web
       name: job-tracker-backend
       buildCommand: "pip install -r requirements.txt && python scripts/init_db_prod.py && python scripts/seed_db_prod.py"
   ```

   ⚠️ **Lưu ý:** Cách này sẽ seed lại mỗi lần deploy → data duplicate!

2. **Hoặc dùng Init Container (1 lần duy nhất):**
   - Không khả dụng với Free tier
   - Cần upgrade plan

---

## 🔄 Re-seed Database (Xóa và seed lại)

Nếu muốn **xóa data cũ** và seed lại từ đầu:

1. **Mở file `scripts/seed_db_prod.py`**

2. **Uncomment dòng:**
   ```python
   # clear_existing_data(db)  # ← Bỏ comment dòng này
   ```

3. **Commit & push:**
   ```bash
   git add scripts/seed_db_prod.py
   git commit -m "feat: Enable clear data before seeding"
   git push
   ```

4. **Chạy lại seed script** trên Render Shell

---

## 📊 Data được seed

Script sẽ tạo:

| Data Type | Count | Description |
|-----------|-------|-------------|
| **Jobs** | 10 | 3 Applied, 2 Screening, 2 Interview, 1 Offer, 1 Hired, 1 Rejected |
| **Interviews** | 2 | Cho 2 jobs có status "Interview" |
| **Email Templates** | 2 | Thank You Email, Application Follow-up |

---

## 🐛 Troubleshooting

### ❌ "Shell not available"

**Giải pháp:**
- Free tier có giới hạn shell access
- Dùng Render CLI thay thế:
  ```bash
  # Install Render CLI
  npm install -g @render/cli
  
  # Login
  render login
  
  # Connect to service
  render ssh job-tracker-backend
  
  # Run seed
  python scripts/seed_db_prod.py
  ```

### ❌ "Permission denied"

**Giải pháp:**
- Ensure bạn là owner/admin của service
- Check file permissions: `chmod +x scripts/seed_db_prod.py`

### ❌ "Module not found"

**Giải pháp:**
- Shell đang ở wrong directory
- Run: `cd /opt/render/project/src`
- Hoặc dùng absolute path: `python /opt/render/project/src/scripts/seed_db_prod.py`

---

## 🎓 Notes

- **One-time operation:** Chỉ cần seed 1 lần sau khi deploy
- **Safe to re-run:** Script không duplicate data (trừ khi uncomment clear_existing_data)
- **Customize data:** Edit `scripts/seed_db_prod.py` để thêm/sửa sample data

---

**Good luck! 🚀**
