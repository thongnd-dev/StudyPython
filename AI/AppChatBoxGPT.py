import streamlit as st
from openai import OpenAI
import pandas as pd
import  os
from utils import contains_pii, mask_pii

def reset_app_state():
    st.session_state.phase = "LIKERT"
    st.session_state.current_q_idx = 0
    st.session_state.answers = {}
    st.session_state.dynamic_questions = []
    st.session_state.chat_history = []

def get_likert_page(questions, page, page_size=4):
    start = page * page_size
    end = start + page_size
    return questions[start:end]

#mã hóa thông tin nhạy cảm
def sanitize_input(text: str) -> str:
    if contains_pii(text):
        return mask_pii((text))
    return text
# CSS
st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 17px;
}

h1 { font-size: 40px; }
h2 { font-size: 30px; }
h3 { font-size: 24px; }

div[data-testid="stChatMessage"] {
    font-size: 17px;
    line-height: 1.6;
}

textarea, input {
    font-size: 17px !important;
}
</style>
""", unsafe_allow_html=True)

# Cấu hình tiêu đề trang web
st.set_page_config(page_title="AI Career Mentor", page_icon="🎓")
st.title("🤖 Trợ lý Tư vấn Nghề nghiệp")
st.caption("Đồ án Tư duy AI 2026")


# API Key
with st.sidebar:
    api_key = st.secrets.get("OPENAI_API_KEY")


# --- CẤU HÌNH DỮ LIỆU ---
@st.cache_data
def load_career_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "Data", "DanhMucNganh.csv")

    if not os.path.exists(csv_path):
        st.error(f"Không tìm thấy file CSV tại: {csv_path}")
        st.stop()

    return pd.read_csv(csv_path, encoding="utf-8")

try:
    df_careers = load_career_data()
    career_list_text = df_careers.to_string(index=False)
except:
    st.error("Không tìm thấy file data.csv!")
    st.stop()

# Định nghĩa dữ liệu câu hỏi (12 câu trắc nghiệm (Holland Code))
questions = [
    {"id": "interests_1", "cat": "Sở thích", "text": "Làm việc với các công cụ, máy móc, hoặc hoạt động ngoài trời."},
    {"id": "interests_2", "cat": "Sở thích", "text": "Phân tích dữ liệu, giải quyết các vấn đề trừu tượng và phức tạp."},
    {"id": "interests_3", "cat": "Sở thích", "text": "Sáng tạo, thể hiện bản thân qua nghệ thuật, âm nhạc, văn chương."},
    {"id": "interests_4", "cat": "Sở thích", "text": "Giúp đỡ, giảng dạy, hoặc chăm sóc sức khỏe cho người khác."},
    {"id": "skills_1", "cat": "Kỹ năng", "text": "Giải quyết các vấn đề logic và phân tích một cách có hệ thống."},
    {"id": "skills_2", "cat": "Kỹ năng", "text": "Giao tiếp, trình bày ý tưởng một cách rõ ràng và thuyết phục."},
    {"id": "skills_3", "cat": "Kỹ năng", "text": "Làm việc hiệu quả trong một đội nhóm, lắng nghe và hợp tác."},
    {"id": "skills_4", "cat": "Kỹ năng", "text": "Sáng tạo ra những ý tưởng mới và tìm kiếm các giải pháp độc đáo."},
    {"id": "values_1", "cat": "Giá trị", "text": "Có một nguồn thu nhập cao và sự đảm bảo về tài chính."},
    {"id": "values_2", "cat": "Giá trị", "text": "Tạo ra những đóng góp ý nghĩa cho cộng đồng và xã hội."},
    {"id": "values_3", "cat": "Giá trị", "text": "Có cơ hội học hỏi, phát triển bản thân và thăng tiến."},
    {"id": "values_4", "cat": "Giá trị", "text": "Cân bằng giữa công việc và cuộc sống cá nhân."}
]

likert_options = {1: 'Hoàn toàn không', 2: 'Không hứng thú', 3: 'Bình thường', 4: 'Hứng thú', 5: 'Rất hứng thú'}

# --- KHỞI TẠO STATE ---
if 'phase' not in st.session_state:
    st.session_state.phase = "LIKERT"
    st.session_state.current_q_idx = 0
    st.session_state.answers = {}
    st.session_state.dynamic_questions = []
    st.session_state.chat_history = []


# --- GIAI ĐOẠN 1: 12 CÂU LIKERT ---
if st.session_state.phase == "LIKERT":
    idx = st.session_state.current_q_idx
    q = questions[idx]
    st.title("🎯 Bước 1: Khảo sát xu hướng")
    # Hiển thị thanh tiến trình phía trên
    progress_text = f"Tiến độ: {idx + 1}/{len(questions)}"
    st.progress((idx + 1) / len(questions), text=progress_text)

    st.markdown(f"### Câu hỏi {idx + 1}")
    st.info(f"**{q['text']}**")

    # Chuyển đổi sang st.radio với 5 lựa chọn
    # Chúng ta dùng list label từ likert_options để hiển thị
    choice = st.radio(
        "Mức độ phù hợp với bạn:",
        options=list(likert_options.keys()),
        format_func=lambda x: likert_options[x],
        horizontal=True,  # Hiển thị nằm ngang cho đẹp
        key=f"radio_{q['id']}"
    )

    st.divider()
    if idx == len(questions) - 1:
        col1, col2 = st.columns(2)
        # Nút tiếp theo
        with col1:
            if st.button("Tiếp theo ➡️", use_container_width=True):
                st.session_state.answers[q['id']] = choice

                if not api_key:
                    st.warning("Cần API Key!")
                else:
                    with st.spinner("AI đang phân tích hồ sơ của bạn...", use_container_width=True):
                        client = OpenAI(api_key=api_key)
                        summary = "\n".join(
                             [f"- {questions[i]['text']}: {st.session_state.answers[questions[i]['id']]}" for i in
                              range(12)])
                        prompt = (
                            f"Dựa trên dữ liệu: {summary}. Bạn là Chuyên gia Tư vấn Hướng nghiệp AI. Bạn phải tuân thủ NGHIÊM NGẶT quy trình sau: "
                            f"**GIAI ĐOẠN PHỎNG VẤN (Đúng 3 câu hỏi):**) "
                            f"- Sau khi nhận kết quả trắc nghiệm (12 câu), bạn hãy đặt đúng 3 câu hỏi phỏng vấn sâu."
                            f"-Đặt đúng 3 câu hỏi, trả về 3 dòng là 3 câu hỏi."
                            f"- Câu hỏi phải dựa trực tiếp trên kết quả trắc nghiệm để làm rõ đam mê, kỹ năng hoặc mong muốn của người dùng."
                            f"- KHÔNG đặt quá 3 câu hỏi.f"
                            f"- Chỉ đưa ra 3 câu hỏi không cần bổ sung thêm tiềndđề hay câu cảm ơn"
                            f"- Tập trung trả lời các câu hỏi của người dùng một cách hỗ trợ, trung lập và không phán xét."
                            f"- Duy trì các tiêu chí: Đáng tin cậy, Công bằng, Bền vững, Minh bạch."
                            f"PHONG CÁCH:"
                            f"- Đồng cảm, thấu đáo, chuyên nghiệp."
                            f"- Giải thích rõ ràng lý do tại sao bạn đưa ra nhận định."
                            f"- Tránh ngôn ngữ khẳng định tuyệt đối (Dùng: 'Có vẻ như...', 'Một hướng đi tiềm năng là...').")
                        safe_prompt = sanitize_input(prompt)
                        res = client.chat.completions.create(model="gpt-5.2",
                                                             messages=[{"role": "user", "content": safe_prompt}])
                        questions = [q for q in res.choices[0].message.content.strip().split('\n') if q.strip()]
                        st.session_state.dynamic_questions = questions
                        st.session_state.phase = "INFO"
                        st.session_state.current_q_idx = 0
                        st.session_state.chat_history.append({"role": "assistant", "content": summary})
                        st.rerun()
        # Nút kết thúc (chỉ xuất hiện ở page cuối)
        with col2:
                if st.button("🎯 Kết thúc & Nhận tư vấn", use_container_width=True):
                    st.session_state.answers[q['id']] = choice
                    st.session_state.phase = "GOAL_ADVICE"
                    st.rerun()
    else:
        if idx < len(questions) - 1:
            if st.button("Tiếp theo ➡️", use_container_width=True):
                st.session_state.answers[q['id']] = choice
                st.session_state.current_q_idx += 1
                st.rerun()

elif st.session_state.phase == "GOAL_ADVICE":
    st.title("🎯 Tư vấn xây dựng mục tiêu nghề nghiệp")
    with st.spinner("AI đang tổng hợp bản kế hoạch sự nghiệp cho bạn..."):
        client = OpenAI(api_key=api_key)
        summary = "\n".join(
            [f"- {questions[i]['text']}: {st.session_state.answers[questions[i]['id']]}" for i in range(12)])

        st.session_state.dynamic_questions = questions
        st.session_state.chat_history.append({"role": "assistant", "content": summary})

        summary_prompt = f"""
                    Dựa trên toàn bộ lịch sử trò chuyện, hãy đưa ra một bản tổng kết cuối cùng gồm:
                    1. Top 3 nghề nghiệp phù hợp nhất (chọn từ danh sách ngành nghề: {career_list_text}).
                    2. Phân tích ngắn gọn lý do (dựa trên sở thích và kỹ năng đã trao đổi).
                    3. Lộ trình 3 bước cụ thể sinh viên cần thực hiện ngay trong năm 2026.
                    Hãy trình bày thật chuyên nghiệp, sử dụng định dạng bảng hoặc danh sách.
                    """

        # Gửi lịch sử chat để AI có đủ ngữ cảnh tổng hợp
        messages = st.session_state.chat_history + [{"role": "user", "content": summary_prompt}]
        res = client.chat.completions.create(
            model="gpt-5.2",
            messages=messages
        )

        # Hiển thị kết quả tổng kết trong một khu vực nổi bật
        st.success("✨ BẢN KẾ HOẠCH SỰ NGHIỆP CÁ NHÂN HÓA 2026")
        st.markdown(res.choices[0].message.content)

        # Tùy chọn tải về hoặc lưu trữ (Tư duy AI bền vững)
        st.download_button("📩 Tải bản tóm tắt (txt)", data=res.choices[0].message.content,
                           file_name="career_plan.txt")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 Phỏng vấn sâu", use_container_width=True):
            if not api_key:
                st.warning("Cần API Key!")
            else:
                client = OpenAI(api_key=api_key)
                summary = "\n".join(
                    [f"- {questions[i]['text']}: {st.session_state.answers[questions[i]['id']]}" for i in
                     range(12)])
                prompt = (
                    f"Dựa trên dữ liệu: {summary}. Bạn là Chuyên gia Tư vấn Hướng nghiệp AI. Bạn phải tuân thủ NGHIÊM NGẶT quy trình sau: "
                    f"**GIAI ĐOẠN PHỎNG VẤN (Đúng 3 câu hỏi):**) "
                    f"- Sau khi nhận kết quả trắc nghiệm (12 câu), bạn hãy đặt đúng 3 câu hỏi phỏng vấn sâu."
                    f"-Đặt đúng 3 câu hỏi, trả về 3 dòng là 3 câu hỏi."
                    f"- Câu hỏi phải dựa trực tiếp trên kết quả trắc nghiệm để làm rõ đam mê, kỹ năng hoặc mong muốn của người dùng."
                    f"- KHÔNG đặt quá 3 câu hỏi.f"
                    f"- Chỉ đưa ra 3 câu hỏi không cần bổ sung thêm tiềndđề hay câu cảm ơn"
                    f"- Tập trung trả lời các câu hỏi của người dùng một cách hỗ trợ, trung lập và không phán xét."
                    f"- Duy trì các tiêu chí: Đáng tin cậy, Công bằng, Bền vững, Minh bạch."
                    f"PHONG CÁCH:"
                    f"- Đồng cảm, thấu đáo, chuyên nghiệp."
                    f"- Giải thích rõ ràng lý do tại sao bạn đưa ra nhận định."
                    f"- Tránh ngôn ngữ khẳng định tuyệt đối (Dùng: 'Có vẻ như...', 'Một hướng đi tiềm năng là...').")
                safe_prompt = sanitize_input(prompt)
                res = client.chat.completions.create(model="gpt-5.2",
                                                     messages=[{"role": "user", "content": safe_prompt}])
                questions = [q for q in res.choices[0].message.content.strip().split('\n') if q.strip()]
                st.session_state.dynamic_questions = questions
                st.session_state.phase = "INFO"
                st.session_state.current_q_idx = 0
                st.session_state.chat_history.append({"role": "assistant", "content": summary})
                st.rerun()

    with col2:
        if st.button("🔁 Làm lại khảo sát", use_container_width=True):
            reset_app_state()
            st.rerun()

# --- GIAI ĐOẠN 2: 3 CÂU HỎI ĐỘNG ---
elif st.session_state.phase == "INFO":
    # Đảm bảo danh sách câu hỏi đã được tạo thành công
    if not st.session_state.dynamic_questions:
        st.error("Rất tiếc, có lỗi khi tạo câu hỏi động. Vui lòng làm lại khảo sát.")
        if st.button("Quay lại bước 1"):
            st.session_state.clear()
            st.rerun()
        st.stop()  # Dừng xử lý nếu không có câu hỏi

    idx = st.session_state.current_q_idx
    # Lấy câu hỏi hiện tại, dùng try-except để bắt lỗi index nếu có
    try:
        # (st.session_state.dynamic_questions) #debug code
        q_text = st.session_state.dynamic_questions[idx]
    except IndexError:
        st.error("Lỗi chỉ mục câu hỏi. Vui lòng thử lại.")
        st.session_state.phase = "CHAT"  # Hoặc chuyển sang phase chat nếu không thể hỏi tiếp
        st.rerun()

    st.title("🔍 Bước 2: Phỏng vấn sâu")
    st.progress((idx + 1) / 3)
    st.subheader(f"Câu hỏi {idx + 1}/3")
    ans = st.text_area(q_text, key=f"ans_dyn_{idx}")

    if st.button("Xác nhận"):
        if ans.strip() == "":
            # Thêm cảnh báo nếu người dùng để trống câu trả lời
            st.warning("Vui lòng nhập câu trả lời để AI phân tích chính xác hơn.")
        else:
            st.session_state.answers[f'info_{idx}'] = ans

            if idx < 2:
                st.session_state.current_q_idx += 1
                st.rerun()
            else:
                with st.spinner("AI đang phân tích hồ sơ của bạn..."):
                    st.session_state.phase = "CHAT"
                    # TỔNG HỢP VÀ GỢI Ý NGÀNH TỪ CSV
                    client = OpenAI(api_key=api_key)
                    final_data = f"Trắc nghiệm: {st.session_state.answers}\nDanh sách ngành nghề từ CSV:\n{career_list_text}"
                    system_msg = (f"Bạn là chuyên gia tư vấn hướng nghiêp AI."
                                  f" Chỉ được chọn tối đa 3 ngành phù hợp nhất từ danh sách cung cấp."
                                  f"Giải thích lý do dự trên các câu hỏi đã trao đổi."
                                  f"Chỉ đưa ra 1 câu hỏi mở rộng để thu thập thông tin."
                                  f"- Từ thời điểm này, bạn CHUYỂN SANG CHẾ ĐỘ LẮNG NGHE.")

                    safe_final_data = sanitize_input(final_data)
                    res = client.chat.completions.create(model="gpt-5.2",
                                                         messages=[{"role": "system", "content": system_msg},
                                                                   {"role": "user", "content": safe_final_data}])

                    # st.json(res.choices[0].message.content)

                    st.session_state.chat_history.append({"role": "assistant", "content": res.choices[0].message.content})
                    st.rerun()

# --- GIAI ĐOẠN 3: CHAT TỰ DO & TỔNG KẾT ---
elif st.session_state.phase == "CHAT":
    st.title("🤖 Bước 3: Tư vấn chi tiết")

    # --- HIỂN THỊ LỊCH SỬ CHAT ---
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # --- INPUT LUÔN Ở CUỐI ---
    user_input = st.chat_input("Bạn muốn hỏi thêm gì không?")
    finish_button = st.button("🏁 Kết thúc", use_container_width=True)

    # Xử lý khi người dùng chat tiếp
    if user_input:
        # Append USER message TRƯỚC
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )
        # GỌI AI
        client = OpenAI(api_key=api_key)
        st.session_state.chat_history.append({"role": "user", "content": sanitize_input(user_input)})

        with st.chat_message("user"): st.write(user_input)

        messages = [{"role": "system",
                     "content": f"Dữ liệu ngành nghề: {career_list_text}"}] + st.session_state.chat_history

        res = client.chat.completions.create(
                model="gpt-5.2",
                messages=messages
        )
        assistant_reply = res.choices[0].message.content
        # Append ASSISTANT message
        st.session_state.chat_history.append(
            {"role": "assistant", "content": assistant_reply}
        )

        # 4RERUN → message sẽ xuất hiện TRÊN input
        st.rerun()

    # Xử lý khi nhấn nút KẾT THÚC
    if finish_button:
        with st.spinner("AI đang tổng hợp bản kế hoạch sự nghiệp cho bạn..."):
            client = OpenAI(api_key=api_key)
            summary_prompt = f"""
            Dựa trên toàn bộ lịch sử trò chuyện, hãy đưa ra một bản tổng kết cuối cùng gồm:
            1. Top 3 nghề nghiệp phù hợp nhất (chọn từ danh sách ngành nghề: {career_list_text}).
            2. Phân tích ngắn gọn lý do (dựa trên sở thích và kỹ năng đã trao đổi).
            3. Lộ trình 3 bước cụ thể sinh viên cần thực hiện ngay trong năm 2026.
            Hãy trình bày thật chuyên nghiệp, sử dụng định dạng bảng hoặc danh sách.
            """

            # Gửi lịch sử chat để AI có đủ ngữ cảnh tổng hợp
            messages = st.session_state.chat_history + [{"role": "user", "content": summary_prompt}]
            res = client.chat.completions.create(
                    model="gpt-5.2",
                    messages=messages
            )

            # Hiển thị kết quả tổng kết trong một khu vực nổi bật
            st.success("✨ BẢN KẾ HOẠCH SỰ NGHIỆP CÁ NHÂN HÓA 2026")
            st.markdown(res.choices[0].message.content)

            # Tùy chọn tải về hoặc lưu trữ (Tư duy AI bền vững)
            st.download_button("📩 Tải bản tóm tắt (txt)", data=res.choices[0].message.content, file_name="career_plan.txt")

    if st.button("🔁 Làm trắc nghiệm mới", use_container_width=True):
        reset_app_state()
        st.rerun()





