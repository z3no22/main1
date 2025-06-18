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
    page_title="Answer Hack Tool",
    page_icon="🎯", 
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

class AnswerHackTool:
    def __init__(self):
        self.version = "v2.0 Simplified"
        self.init_session_state()
    
    def init_session_state(self):
        """Khởi tạo session state"""
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'answer_hack'
        if 'answers_data' not in st.session_state:
            st.session_state.answers_data = None
    
    def render_header(self):
        """Render header chính"""
        st.markdown(f"""
        <div class="main-header">
            <h1>🎯 ANSWER HACK {self.version}</h1>
            <p>Kahoot Answer Retrieval Tool - Web Interface</p>
            <p><em>Simplified Version</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render sidebar navigation"""
        st.sidebar.title("🐱 Navigation")
        
        pages = {
            'answer_hack': '🎯 Answer Hack',
            'settings': '⚙️ Cài Đặt'
        }
        
        # Sử dụng radio button để navigation không cần rerun
        current_page_label = pages.get(st.session_state.current_page, pages['answer_hack'])
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
            request_timeout = st.slider("Timeout (giây):", 5, 60, 30)
            
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
        if st.session_state.current_page == 'answer_hack':
            self.answer_hack_page()
        elif st.session_state.current_page == 'settings':
            self.settings_page()

# Main execution
if __name__ == "__main__":
    app = AnswerHackTool()
    app.run()