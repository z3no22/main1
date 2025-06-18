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
        """Lấy đáp án thực từ Kahoot API"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🔍 Đang tìm kiếm quiz...")
            progress_bar.progress(10)
            
            # Xác định quiz_id
            quiz_id = quiz_input.strip()
            
            if input_type == "Game PIN":
                status_text.text("📡 Đang chuyển đổi Game PIN thành Quiz ID...")
                progress_bar.progress(25)
                
                if not quiz_id.isdigit():
                    raise ValueError("Game PIN phải chỉ chứa số")
                
                pin_result = self.get_quiz_id_from_pin(quiz_id)
                if 'error' in pin_result:
                    raise ValueError(f"Không thể lấy Quiz ID từ PIN: {pin_result['error']}")
                
                quiz_id = pin_result['quiz_id']
                status_text.text(f"✅ Đã tìm thấy Quiz ID: {quiz_id}")
                progress_bar.progress(40)
            
            status_text.text("📡 Đang kết nối Kahoot API...")
            progress_bar.progress(60)
            
            # Lấy quiz data từ API
            quiz_data = self.get_quiz_by_id(quiz_id)
            if 'error' in quiz_data:
                raise ValueError(f"Lỗi API: {quiz_data['error']}")
            
            status_text.text("📥 Đang xử lý dữ liệu quiz...")
            progress_bar.progress(80)
            
            # Xử lý dữ liệu
            quiz_result = self.process_quiz_data(quiz_data, method)
            
            status_text.text("✅ Hoàn thành!")
            progress_bar.progress(100)
            time.sleep(0.5)
            
            st.session_state.answers_data = quiz_result
            
            progress_bar.empty()
            status_text.empty()
            
            st.success(f"✅ Đã lấy thành công {quiz_result['total_questions']} câu hỏi!")
            
        except Exception as e:
            st.error(f"❌ Lỗi: {str(e)}")
            progress_bar.empty()
            status_text.empty()
    
    def get_quiz_by_id(self, quiz_id):
        """Lấy quiz data từ Kahoot API"""
        import re
        import urllib.request
        import urllib.error
        import json
        
        if not re.fullmatch(r"^[A-Za-z0-9-]*$", quiz_id):
            return {'error': 'Invalid quiz ID format'}
        
        url = f"https://play.kahoot.it/rest/kahoots/{quiz_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json'
        }
        
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {'error': 'Quiz not found. The ID may be incorrect.'}
            return {'error': f'HTTP Error: {e.code} - {e.reason}'}
        except urllib.error.URLError as e:
            return {'error': f'Connection error: {e.reason}. Check your internet connection.'}
        except json.JSONDecodeError:
            return {'error': 'Failed to parse the response from Kahoot servers.'}
        except Exception as e:
            return {'error': f'Unexpected error: {str(e)}'}
    
    def get_quiz_id_from_pin(self, pin):
        """Lấy quiz ID từ Game PIN"""
        import urllib.request
        import urllib.error
        import json
        
        if not pin.isdigit():
            return {'error': 'PIN must contain only digits'}
        
        url = f"https://kahoot.it/rest/challenges/pin/{pin}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json'
        }
        
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                return {'quiz_id': data.get('id')}
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {'error': 'No active game found with this PIN.'}
            return {'error': f'HTTP Error: {e.code} - {e.reason}'}
        except Exception as e:
            return {'error': f'Failed to fetch quiz ID from PIN: {str(e)}'}
    
    def clean_text(self, text):
        """Làm sạch text từ HTML tags"""
        if not text:
            return ""
        
        text = str(text)
        replacements = [
            ("<p>", ""), ("</p>", ""), 
            ("<strong>", ""), ("</strong>", ""),
            ("<b>", ""), ("</b>", ""),
            ("<br/>", "\n"), ("<br>", "\n"),
            ("<span>", ""), ("</span>", ""),
            ("<math>", ""), ("</math>", ""),
            ("<semantics>", ""), ("</semantics>", ""),
            ("<mrow>", ""), ("</mrow>", ""),
            ("<mo>", ""), ("</mo>", ""),
            ("<msup>", ""), ("</msup>", ""),
            ("<mi>", ""), ("</mi>", ""),
            ("<mn>", ""), ("</mn>", ""),
            ("<annotation>", ""), ("</annotation>", "")
        ]
        
        for old, new in replacements:
            text = text.replace(old, new)
        
        return text.strip()
    
    def process_quiz_data(self, quiz_data, method):
        """Xử lý dữ liệu quiz thành format hiển thị"""
        if 'error' in quiz_data or 'uuid' not in quiz_data:
            raise ValueError("Invalid quiz data")
        
        quiz_title = quiz_data.get("title", "Untitled Quiz")
        creator = quiz_data.get("creator_username", "Unknown")
        questions = quiz_data.get("questions", [])
        
        processed_answers = []
        
        for i, question in enumerate(questions):
            question_type = question.get("type", "unknown")
            
            # Skip content slides
            if question_type == "content":
                continue
            
            question_text = self.clean_text(question.get("question", f"Question {i+1}"))
            choices = question.get("choices", [])
            
            # Xử lý choices
            processed_choices = []
            correct_answers = []
            
            for choice in choices:
                answer_text = self.clean_text(choice.get("answer", ""))
                is_correct = choice.get("correct", False)
                
                processed_choices.append(answer_text)
                if is_correct:
                    correct_answers.append(answer_text)
            
            # Xử lý đặc biệt cho jumble type
            if question_type == "jumble":
                correct_answers = processed_choices.copy()
            
            processed_answers.append({
                'question': question_text,
                'correct_answer': ', '.join(correct_answers) if correct_answers else 'No correct answer',
                'options': processed_choices,
                'type': question_type
            })
        
        return {
            'quiz_title': quiz_title,
            'creator': creator,
            'quiz_id': quiz_data.get("uuid", ""),
            'total_questions': len(processed_answers),
            'answers': processed_answers,
            'method_used': method,
            'fetch_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def display_answers(self, answers_data):
        """Hiển thị đáp án"""
        st.success(f"📚 **{answers_data['quiz_title']}**")
        
        # Hiển thị thông tin quiz
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tổng số câu", answers_data['total_questions'])
        with col2:
            st.metric("Creator", answers_data.get('creator', 'Unknown'))
        with col3:
            st.metric("Quiz ID", answers_data.get('quiz_id', '')[:8] + "..." if answers_data.get('quiz_id', '') else 'N/A')
        
        st.info(f"Phương thức: {answers_data['method_used']} | Thời gian: {answers_data['fetch_time']}")
        
        # Export button
        if st.button("💾 Export Đáp Án"):
            self.export_answers(answers_data)
        
        st.markdown("---")
        
        # Hiển thị từng câu hỏi
        for i, qa in enumerate(answers_data['answers'], 1):
            question_title = qa['question'][:50] + "..." if len(qa['question']) > 50 else qa['question']
            
            with st.expander(f"Câu {i}: {question_title}", expanded=True):
                st.write(f"**Câu hỏi:** {qa['question']}")
                
                if qa.get('type'):
                    st.caption(f"Loại: {qa['type']}")
                
                st.write(f"**✅ Đáp án đúng:** {qa['correct_answer']}")
                
                if qa.get('options') and len(qa['options']) > 0:
                    st.write("**Tất cả lựa chọn:**")
                    for j, option in enumerate(qa['options']):
                        if option in qa['correct_answer']:
                            st.success(f"✅ {chr(65+j)}. {option}")
                        else:
                            st.write(f"❌ {chr(65+j)}. {option}")
    
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