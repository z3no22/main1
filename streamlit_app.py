#!/usr/bin/env python3
import streamlit as st
import subprocess
import time
import os
import sys
import platform
import json
from pathlib import Path
import requests
from datetime import datetime

# Cấu hình trang
st.set_page_config(
    page_title="Kitty-Tools v36.2 - Web Interface",
    page_icon="🐱", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh cho giao diện đẹp
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

class KittyToolsWeb:
    def __init__(self):
        self.version = "v36.2 Enhanced Web"
        self.init_session_state()
    
    def init_session_state(self):
        """Khởi tạo session state"""
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'home'
        if 'answers_data' not in st.session_state:
            st.session_state.answers_data = None
        if 'flood_running' not in st.session_state:
            st.session_state.flood_running = False
    
    def render_header(self):
        """Render header chính"""
        st.markdown(f"""
        <div class="main-header">
            <h1>🐱 KITTY TOOLS {self.version}</h1>
            <p>Comprehensive Kahoot Enhancement Suite - Web Interface</p>
            <p><em>by CPScript</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render sidebar navigation"""
        st.sidebar.title("🐱 Navigation")
        
        pages = {
            'home': '🏠 Trang Chủ',
            'answer_hack': '🎯 Answer Hack', 
            'kahoot_flooder': '🌊 Kahoot Flooder',
            'info': 'ℹ️ Thông Tin',
            'settings': '⚙️ Cài Đặt'
        }
        
        # Sử dụng radio button để navigation không cần rerun
        current_page_label = pages.get(st.session_state.current_page, pages['home'])
        page_labels = list(pages.values())
        
        selected_label = st.sidebar.radio(
            "Chọn trang:",
            page_labels,
            index=page_labels.index(current_page_label),
            label_visibility="collapsed"
        )
        
        # Cập nhật current_page dựa trên selection
        for page_id, page_name in pages.items():
            if page_name == selected_label:
                st.session_state.current_page = page_id
                break
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Thống Kê")
        st.sidebar.info(f"Platform: {platform.system()}")
        st.sidebar.info(f"Python: {sys.version.split()[0]}")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ⚠️ Lưu Ý Pháp Lý")
        st.sidebar.warning("Tool này chỉ dành cho mục đích giáo dục. Vui lòng sử dụng có trách nhiệm.")
    
    def home_page(self):
        """Trang chủ"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>🎯 Answer Hack</h3>
                <p>Lấy đáp án cho bất kỳ quiz Kahoot nào bằng Quiz ID hoặc Game PIN</p>
                <ul>
                    <li>✅ Lấy đáp án nhanh chóng</li>
                    <li>✅ Hỗ trợ nhiều định dạng</li>
                    <li>✅ Export kết quả</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>🌊 Kahoot Flooder</h3>
                <p>Tạo nhiều bot tham gia game Kahoot với các cấu hình khác nhau</p>
                <ul>
                    <li>✅ Tạo nhiều bot cùng lúc</li>
                    <li>✅ Tùy chỉnh hành vi bot</li>
                    <li>✅ Anti-detection mode</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Hướng dẫn nhanh
        st.markdown("### 🚀 Hướng Dẫn Nhanh")
        
        tab1, tab2, tab3 = st.tabs(["Answer Hack", "Kahoot Flooder", "Thông Tin"])
        
        with tab1:
            st.markdown("""
            **Cách sử dụng Answer Hack:**
            1. Chọn "Answer Hack" từ sidebar
            2. Nhập Quiz ID hoặc Game PIN
            3. Chọn phương thức lấy đáp án
            4. Xem kết quả và export nếu cần
            """)
        
        with tab2:
            st.markdown("""
            **Cách sử dụng Kahoot Flooder:**
            1. Chọn "Kahoot Flooder" từ sidebar  
            2. Nhập Game PIN
            3. Cấu hình số lượng bot và hành vi
            4. Bắt đầu flooding
            """)
        
        with tab3:
            st.markdown("""
            **Thông tin thêm:**
            - Xem danh sách contributors
            - Đọc legal disclaimer
            - Kiểm tra cập nhật
            """)
    
    def answer_hack_page(self):
        """Trang Answer Hack"""
        st.title("🎯 Answer Hack")
        
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ Lưu ý:</strong> Chức năng này chỉ dành cho mục đích giáo dục và nghiên cứu.
        </div>
        """, unsafe_allow_html=True)
        
        # Input form
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Nhập Thông Tin")
            input_type = st.selectbox(
                "Loại Input:",
                ["Quiz ID", "Game PIN"],
                help="Chọn loại thông tin bạn có"
            )
            
            if input_type == "Quiz ID":
                quiz_input = st.text_input(
                    "Quiz ID:", 
                    placeholder="Nhập Quiz ID (VD: 12345678-1234-1234-1234-123456789012)",
                    help="Quiz ID thường là chuỗi UUID dài"
                )
            else:
                quiz_input = st.text_input(
                    "Game PIN:",
                    placeholder="Nhập Game PIN (VD: 1234567)",
                    help="Game PIN thường là số 6-7 chữ số"
                )
            
            method = st.selectbox(
                "Phương thức:",
                ["Auto Detect", "API Method", "Web Scraping"],
                help="Chọn phương thức lấy đáp án"
            )
            
            if st.button("🔍 Lấy Đáp Án", type="primary"):
                if quiz_input:
                    self.fetch_answers(quiz_input, input_type, method)
                else:
                    st.error("Vui lòng nhập Quiz ID hoặc Game PIN!")
        
        with col2:
            st.subheader("📊 Kết Quả")
            
            if st.session_state.answers_data:
                self.display_answers(st.session_state.answers_data)
            else:
                st.info("Chưa có dữ liệu. Vui lòng nhập thông tin và lấy đáp án.")
    
    def fetch_answers(self, quiz_input, input_type, method):
        """Mô phỏng việc lấy đáp án"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🔍 Đang tìm kiếm quiz...")
            progress_bar.progress(25)
            time.sleep(1)
            
            status_text.text("📡 Đang kết nối API...")
            progress_bar.progress(50)
            time.sleep(1)
            
            status_text.text("📥 Đang tải đáp án...")
            progress_bar.progress(75)
            time.sleep(1)
            
            # Mô phỏng dữ liệu đáp án
            mock_answers = {
                'quiz_title': f'Sample Quiz ({quiz_input})',
                'total_questions': 10,
                'answers': [
                    {'question': 'Câu 1: Thủ đô của Việt Nam là?', 'correct_answer': 'Hà Nội', 'options': ['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Cần Thơ']},
                    {'question': 'Câu 2: Python được tạo ra bởi ai?', 'correct_answer': 'Guido van Rossum', 'options': ['Guido van Rossum', 'Linus Torvalds', 'Dennis Ritchie', 'Bjarne Stroustrup']},
                    {'question': 'Câu 3: Framework web phổ biến của Python?', 'correct_answer': 'Django', 'options': ['Django', 'Flask', 'FastAPI', 'Tất cả đều đúng']},
                    {'question': 'Câu 4: Streamlit dùng để làm gì?', 'correct_answer': 'Tạo web app', 'options': ['Tạo web app', 'Machine Learning', 'Data Analysis', 'Tất cả đều đúng']},
                    {'question': 'Câu 5: Kahoot là gì?', 'correct_answer': 'Nền tảng quiz trực tuyến', 'options': ['Game mobile', 'Nền tảng quiz trực tuyến', 'Mạng xã hội', 'Ứng dụng chat']}
                ],
                'method_used': method,
                'fetch_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            status_text.text("✅ Hoàn thành!")
            progress_bar.progress(100)
            time.sleep(0.5)
            
            st.session_state.answers_data = mock_answers
            
            progress_bar.empty()
            status_text.empty()
            
            st.success(f"✅ Đã lấy thành công {mock_answers['total_questions']} câu hỏi!")
            
        except Exception as e:
            st.error(f"❌ Lỗi: {str(e)}")
            progress_bar.empty()
            status_text.empty()
    
    def display_answers(self, answers_data):
        """Hiển thị đáp án"""
        st.success(f"📚 **{answers_data['quiz_title']}**")
        st.info(f"Tổng số câu: {answers_data['total_questions']} | Phương thức: {answers_data['method_used']}")
        
        # Export button
        if st.button("💾 Export Đáp Án"):
            self.export_answers(answers_data)
        
        st.markdown("---")
        
        # Hiển thị từng câu hỏi
        for i, qa in enumerate(answers_data['answers'], 1):
            with st.expander(f"Câu {i}: {qa['question'].split(':')[1].strip() if ':' in qa['question'] else qa['question']}", expanded=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write("**Các lựa chọn:**")
                    for j, option in enumerate(qa['options']):
                        if option == qa['correct_answer']:
                            st.success(f"✅ {chr(65+j)}. {option} (Đáp án đúng)")
                        else:
                            st.write(f"❌ {chr(65+j)}. {option}")
                
                with col2:
                    st.metric("Đáp án", qa['correct_answer'])
    
    def export_answers(self, answers_data):
        """Export đáp án ra file"""
        export_text = f"""KITTY TOOLS - ANSWER EXPORT
Quiz: {answers_data['quiz_title']}
Total Questions: {answers_data['total_questions']}
Method: {answers_data['method_used']}
Export Time: {answers_data['fetch_time']}

{'='*50}

"""
        
        for i, qa in enumerate(answers_data['answers'], 1):
            export_text += f"Question {i}: {qa['question']}\n"
            export_text += f"Correct Answer: {qa['correct_answer']}\n"
            export_text += "Options:\n"
            for j, option in enumerate(qa['options']):
                marker = "✓" if option == qa['correct_answer'] else " "
                export_text += f"  [{marker}] {chr(65+j)}. {option}\n"
            export_text += "\n"
        
        st.download_button(
            label="📥 Tải File Đáp Án",
            data=export_text,
            file_name=f"kitty_answers_{int(time.time())}.txt",
            mime="text/plain"
        )
        
        st.success("✅ File đáp án đã được tạo!")
    
    def kahoot_flooder_page(self):
        """Trang Kahoot Flooder"""
        st.title("🌊 Kahoot Flooder")
        
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ Cảnh báo:</strong> Chức năng này có thể ảnh hưởng đến trải nghiệm của người khác. 
            Chỉ sử dụng trong môi trường test hoặc với sự đồng ý của người tổ chức.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("⚙️ Cấu Hình Bot")
            
            game_pin = st.text_input(
                "Game PIN:",
                placeholder="Nhập Game PIN (VD: 1234567)",
                help="PIN của game Kahoot đang diễn ra"
            )
            
            bot_count = st.slider(
                "Số lượng Bot:",
                min_value=1,
                max_value=100,
                value=10,
                help="Số bot sẽ được tạo"
            )
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                name_type = st.selectbox(
                    "Loại tên Bot:",
                    ["Random Names", "Custom Prefix", "Numbered"],
                    help="Cách đặt tên cho bot"
                )
                
                if name_type == "Custom Prefix":
                    custom_prefix = st.text_input("Prefix:", value="Bot")
                else:
                    custom_prefix = ""
            
            with col_b:
                bot_behavior = st.selectbox(
                    "Hành vi Bot:",
                    ["Random Answers", "All Correct", "All Wrong", "Pattern"],
                    help="Cách bot trả lời câu hỏi"
                )
                
                delay = st.slider(
                    "Delay (giây):",
                    min_value=0.1,
                    max_value=5.0,
                    value=1.0,
                    step=0.1,
                    help="Thời gian chờ giữa các action"
                )
            
            anti_detection = st.checkbox(
                "🛡️ Anti-Detection Mode",
                help="Sử dụng các kỹ thuật để tránh bị phát hiện"
            )
            
            if st.button("🚀 Bắt Đầu Flooding", type="primary", disabled=st.session_state.flood_running):
                if game_pin:
                    self.start_flooding(game_pin, bot_count, name_type, custom_prefix, bot_behavior, delay, anti_detection)
                else:
                    st.error("Vui lòng nhập Game PIN!")
            
            if st.session_state.flood_running:
                if st.button("⏹️ Dừng Flooding", type="secondary"):
                    self.stop_flooding()
        
        with col2:
            st.subheader("📊 Trạng Thái")
            
            if st.session_state.flood_running:
                st.success("🟢 Đang chạy...")
                
                # Hiển thị thống kê giả
                st.metric("Bot đã tạo", f"{bot_count}/100")
                st.metric("Thành công", "85%")
                st.metric("Thời gian chạy", "00:02:30")
                
                # Progress bar
                progress = st.progress(0.85)
                
            else:
                st.info("🔵 Chưa chạy")
                
                st.markdown("""
                **Hướng dẫn:**
                1. Nhập Game PIN của Kahoot
                2. Cấu hình số bot và hành vi
                3. Bấm "Bắt Đầu Flooding"
                4. Theo dõi trạng thái ở đây
                """)
    
    def start_flooding(self, game_pin, bot_count, name_type, custom_prefix, bot_behavior, delay, anti_detection):
        """Bắt đầu flooding (mô phỏng)"""
        st.session_state.flood_running = True
        
        with st.spinner("🚀 Đang khởi động flooding..."):
            time.sleep(2)
        
        st.success(f"✅ Đã bắt đầu flooding với {bot_count} bot!")
    
    def stop_flooding(self):
        """Dừng flooding"""
        st.session_state.flood_running = False
        st.info("⏹️ Đã dừng flooding!")
    
    def info_page(self):
        """Trang thông tin"""
        st.title("ℹ️ Thông Tin")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Về Tool", "Contributors", "Legal", "Hướng Dẫn"])
        
        with tab1:
            st.markdown("""
            ## 🐱 Kitty-Tools v36.2 Enhanced Web
            
            **Mô tả:** Bộ công cụ toàn diện cho việc tăng cường và phân tích tương tác với Kahoot quiz.
            
            ### ✨ Tính Năng Chính:
            - **Answer Retrieval System** - Lấy đáp án cho bất kỳ quiz Kahoot nào
            - **Multi-bot Participation** - Tạo nhiều bot tham gia quiz tự động
            - **Cross-Platform Support** - Hỗ trợ Windows, macOS, Linux, Android
            - **Modern Web Interface** - Giao diện web hiện đại và dễ sử dụng
            - **Export Functionality** - Lưu đáp án dưới dạng text để tham khảo
            
            ### 🔧 Công Nghệ:
            - **Frontend:** Streamlit
            - **Backend:** Python 3.6+
            - **Database:** JSON-based storage
            - **API:** RESTful endpoints
            """)
        
        with tab2:
            st.markdown("""
            ## 🤝 Contributors
            
            Cảm ơn tất cả những người đóng góp đã giúp Kitty-Tools trở nên tốt hơn:
            """)
            
            contributors = [
                {"name": "@CPScript", "role": "Lead Developer & Project Maintainer", "avatar": "👨‍💻"},
                {"name": "@Ccode-lang", "role": "Core Development & API Integration", "avatar": "⚡"},
                {"name": "@xTobyPlayZ", "role": "Flooder Module Development", "avatar": "🌊"},
                {"name": "@cheepling", "role": "Quality Assurance & Bug Reporting", "avatar": "🐛"},
                {"name": "@Zacky2613", "role": "Technical Support & Issue Resolution", "avatar": "🔧"},
                {"name": "@KiraKenjiro", "role": "Code Review & Optimization", "avatar": "🔍"}
            ]
            
            for contributor in contributors:
                st.markdown(f"""
                <div class="feature-card">
                    <h4>{contributor['avatar']} {contributor['name']}</h4>
                    <p><em>{contributor['role']}</em></p>
                </div>
                """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("""
            ## 📜 Legal Disclaimer
            
            <div class="warning-box">
            <strong>⚠️ Tuyên bố miễn trừ trách nhiệm pháp lý</strong><br><br>
            
            Kitty-Tools được cung cấp <strong>chỉ dành cho mục đích giáo dục</strong>. 
            Phần mềm này được thiết kế để demonstate các lỗ hổng của nền tảng giáo dục 
            và được sử dụng trong môi trường có kiểm soát, đạo đức.
            <br><br>
            Các nhà phát triển không ủng hộ hoặc khuyến khích bất kỳ việc sử dụng nào 
            của phần mềm này vi phạm điều khoản dịch vụ của các nền tảng giáo dục 
            hoặc làm gián đoạn các hoạt động giáo dục.
            <br><br>
            <strong>Sử dụng với rủi ro và trách nhiệm của riêng bạn.</strong>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            ### 📋 Điều Khoản Sử Dụng:
            1. **Chỉ sử dụng cho mục đích giáo dục và nghiên cứu**
            2. **Không sử dụng để gây rối hoặc làm hại**
            3. **Tuân thủ luật pháp địa phương**
            4. **Không vi phạm điều khoản dịch vụ của các nền tảng**
            5. **Sử dụng có trách nhiệm và đạo đức**
            
            ### 🛡️ Bảo Mật:
            - Tool không lưu trữ thông tin cá nhân
            - Tất cả dữ liệu được xử lý locally
            - Không chia sẻ thông tin với bên thứ ba
            """)
        
        with tab4:
            st.markdown("""
            ## 📖 Hướng Dẫn Chi Tiết
            
            ### 🎯 Answer Hack
            **Bước 1:** Chọn "Answer Hack" từ sidebar
            **Bước 2:** Chọn loại input (Quiz ID hoặc Game PIN)
            **Bước 3:** Nhập thông tin và chọn phương thức
            **Bước 4:** Bấm "Lấy Đáp Án" và chờ kết quả
            **Bước 5:** Export đáp án nếu cần
            
            ### 🌊 Kahoot Flooder  
            **Bước 1:** Chọn "Kahoot Flooder" từ sidebar
            **Bước 2:** Nhập Game PIN của Kahoot đang diễn ra
            **Bước 3:** Cấu hình số lượng bot và hành vi
            **Bước 4:** Bấm "Bắt Đầu Flooding"
            **Bước 5:** Theo dõi trạng thái và dừng khi cần
            
            ### ⚙️ Cài Đặt
            **Cài đặt dependencies:** `pip install -r requirements.txt`
            **Chạy local:** `streamlit run streamlit_app.py`
            **Deploy:** Sử dụng Streamlit Cloud, Heroku, hoặc Docker
            
            ### 🔧 Troubleshooting
            - **Module Not Found:** Cài đặt dependencies bị thiếu
            - **Connection Error:** Kiểm tra kết nối internet
            - **Invalid PIN:** Đảm bảo Game PIN đúng và game đang diễn ra
            """)
    
    def settings_page(self):
        """Trang cài đặt"""
        st.title("⚙️ Cài Đặt")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎨 Giao Diện")
            theme = st.selectbox("Theme:", ["Light", "Dark", "Auto"])
            language = st.selectbox("Ngôn ngữ:", ["Tiếng Việt", "English"])
            
            st.subheader("🔧 Hiệu Suất")
            cache_enabled = st.checkbox("Bật Cache", value=True)
            max_bots = st.slider("Giới hạn Bot:", 1, 500, 100)
            
        with col2:
            st.subheader("🛡️ Bảo Mật")
            anonymize_data = st.checkbox("Ẩn danh hóa dữ liệu", value=True)
            log_activities = st.checkbox("Ghi log hoạt động", value=False)
            
            st.subheader("📊 Analytics")
            usage_stats = st.checkbox("Thu thập thống kê sử dụng", value=False)
            
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("💾 Lưu Cài Đặt", type="primary"):
                st.success("✅ Đã lưu cài đặt!")
        
        with col_b:
            if st.button("🔄 Reset Về Mặc Định"):
                st.info("🔄 Đã reset về cài đặt mặc định!")
    
    def run(self):
        """Chạy ứng dụng chính"""
        self.render_header()
        self.render_sidebar()
        
        # Route pages
        if st.session_state.current_page == 'home':
            self.home_page()
        elif st.session_state.current_page == 'answer_hack':
            self.answer_hack_page()
        elif st.session_state.current_page == 'kahoot_flooder':
            self.kahoot_flooder_page()
        elif st.session_state.current_page == 'info':
            self.info_page()
        elif st.session_state.current_page == 'settings':
            self.settings_page()

# Main execution
if __name__ == "__main__":
    app = KittyToolsWeb()
    app.run()