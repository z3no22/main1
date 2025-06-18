# 🚀 Hướng Dẫn Deploy Kitty-Tools Web Interface

## 📋 Tổng Quan

Kitty-Tools Web Interface được xây dựng bằng Streamlit, cung cấp giao diện web hiện đại cho bộ công cụ Kahoot enhancement.

## 🔧 Cài Đặt Local

### Prerequisites
- Python 3.7+ 
- pip
- Git

### Bước 1: Clone Repository
```bash
git clone https://github.com/CPScript/Kitty-Tools
cd Kitty-Tools
```

### Bước 2: Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy Ứng Dụng
```bash
streamlit run streamlit_app.py
```

Ứng dụng sẽ chạy tại: `http://localhost:8501`

## 🌐 Deploy Lên Cloud

### 1. Streamlit Community Cloud (Miễn Phí)

**Bước 1:** Đăng nhập [share.streamlit.io](https://share.streamlit.io) bằng GitHub

**Bước 2:** Kết nối repository GitHub

**Bước 3:** Cấu hình deployment:
- **Repository:** `your-username/Kitty-Tools`
- **Branch:** `main`
- **Main file path:** `streamlit_app.py`

**Bước 4:** Deploy! URL sẽ có dạng: `https://your-app-name.streamlit.app`

### 2. Heroku

**Bước 1:** Cài đặt Heroku CLI và login
```bash
heroku login
```

**Bước 2:** Tạo app mới
```bash
heroku create kitty-tools-web
```

**Bước 3:** Tạo file `Procfile`:
```bash
echo "web: streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0" > Procfile
```

**Bước 4:** Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 3. Docker Deployment

**Bước 1:** Build Docker image
```bash
docker build -t kitty-tools-web .
```

**Bước 2:** Chạy container
```bash
docker run -p 8501:8501 kitty-tools-web
```

**Bước 3:** Truy cập ứng dụng tại `http://localhost:8501`

### 4. Railway

**Bước 1:** Đăng ký tại [railway.app](https://railway.app)

**Bước 2:** Connect GitHub repository

**Bước 3:** Deploy tự động với zero configuration

### 5. Render

**Bước 1:** Đăng ký tại [render.com](https://render.com)

**Bước 2:** Tạo Web Service mới

**Bước 3:** Cấu hình:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`

## ⚙️ Environment Variables

Có thể cấu hình các biến môi trường sau:

```bash
# Optional: Custom configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_THEME_PRIMARY_COLOR=#667eea
```

## 🔒 Cấu Hình Bảo Mật

### 1. Giới Hạn Truy Cập
Thêm authentication bằng cách sửa đổi `streamlit_app.py`:

```python
import streamlit_authenticator as stauth

# Cấu hình authentication
authenticator = stauth.Authenticate(
    credentials,
    'some_cookie_name',
    'some_signature_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Hiển thị app
    app.run()
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

### 2. Rate Limiting
Sử dụng middleware để giới hạn request:

```python
import time
from functools import wraps

def rate_limit(max_calls=10, period=60):
    def decorator(func):
        calls = []
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [call for call in calls if call > now - period]
            if len(calls) >= max_calls:
                st.error("Rate limit exceeded. Please try again later.")
                return
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## 📊 Monitoring và Analytics

### 1. Streamlit Analytics
```python
# Thêm vào streamlit_app.py
import streamlit.components.v1 as components

# Google Analytics
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", height=0)
```

### 2. Error Tracking
Tích hợp Sentry cho error tracking:

```python
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    traces_sample_rate=1.0
)
```

## 🚨 Troubleshooting

### Lỗi Thường Gặp

**1. Module Not Found**
```bash
pip install --upgrade -r requirements.txt
```

**2. Port Already in Use**
```bash
streamlit run streamlit_app.py --server.port 8502
```

**3. Memory Issues**
Thêm vào `config.toml`:
```toml
[server]
maxUploadSize = 200
```

**4. Slow Loading**
Tối ưu hóa với caching:
```python
@st.cache_data
def load_data():
    # Your expensive computation
    return data
```

## 📱 Mobile Optimization

App đã được tối ưu cho mobile, nhưng có thể cải thiện thêm:

```css
/* Thêm vào CSS custom */
@media (max-width: 768px) {
    .main-header {
        padding: 1rem;
    }
    
    .feature-card {
        padding: 1rem;
    }
}
```

## 🔄 Continuous Deployment

Thiết lập GitHub Actions cho auto-deployment:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Streamlit

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python -m pytest tests/
    - name: Deploy to Streamlit Cloud
      # Auto-deploy triggered by push
      run: echo "Deployed!"
```

## 📞 Support

Nếu gặp vấn đề, vui lòng:

1. Kiểm tra [Issues](https://github.com/CPScript/Kitty-Tools/issues)
2. Tạo issue mới với chi tiết lỗi
3. Liên hệ: [Discord/Email]

---

**🐱 Happy Deploying với Kitty-Tools!** 