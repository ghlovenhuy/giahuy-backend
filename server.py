import os
import google.generativeai as genai
from flask import Flask, jsonify, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔑 HÃY THAY CÁI KEY MỚI CỦA BẠN VÀO ĐÂY ĐỂ BOT CHẠY ĐƯỢC NHÉ
API_KEY = "AIzaSyCj7xeFmjn6V3NwBx-wIc0sNfE-orduDr4"
genai.configure(api_key=API_KEY)


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Tin nhắn trống!"}), 400

        # Chuyển tin nhắn về chữ thường để kiểm tra từ khóa
        tin_nhan_kiem_tra = (
            user_message.lower()
            .replace("?", "")
            .replace(".", "")
            .replace(",", "")
            .strip()
        )

        # Danh sách các từ khóa chào hỏi thông thường
        cac_tu_chao_hoi = [
            "hi",
            "hello",
            "chao",
            "chào",
            "xin chao",
            "xin chào",
            "ola",
            "hey",
            "e",
            "ê",
        ]

        # 👉 TRƯỜNG HỢP 1: Người dùng chỉ chào hỏi xã giao
        if tin_nhan_kiem_tra in cac_tu_chao_hoi:

            def generate_greeting():
                yield "Chào bạn! GiaHuy4.0 có thể giúp gì cho bạn hôm nay?"

            return Response(generate_greeting(), mimetype="text/plain")

        # 👉 CẤU HÌNH PROMPT HỆ THỐNG ĐÃ ĐỔI NGÔI XƯNG HÔ THÀNH "TÔI" CHUẨN XỊN
        prompt_he_thong = (
            "Bạn là GiaHuy4.0, một trợ lý học tập trí tuệ nhân tạo chuyên nghiệp, văn minh và lịch sự. "
            "Nhiệm vụ của bạn là hỗ trợ học sinh giải đáp kiến thức các môn học (CSDL, Marketing, Web, Tiếng Anh...) một cách chính xác, khoa học.\n\n"
            "⚠️ QUY TẮC ĐẶC BIỆT VỀ THÔNG TIN NGƯỜI SÁNG LẬP:\n"
            "Khi người dùng hỏi bạn là ai, ai tạo ra bạn, ai lập trình ra bạn, thông tin về bot, hoặc bất kỳ câu hỏi nào liên quan đến nguồn gốc của bạn, "
            "bạn BẮT BUỘC phải trả lời bằng ngôi thứ nhất (xưng tôi) một cách trang trọng như sau:\n"
            "- Người sáng lập ra tôi (GiaHuy4.0) là: TRẦN NGUYỄN GIA HUY (Sinh ngày 04/06/2009).\n"
            "- Tôi là sản phẩm trí tuệ nhân tạo được nghiên cứu và phát triển bởi anh Trần Nguyễn Gia Huy nhằm mục đích hỗ trợ các bạn học sinh tối ưu hóa việc học tập.\n\n"
            "Quy tắc ứng xử chung:\n"
            "1. Luôn dùng ngôn từ chuẩn mực, tôn trọng, không sử dụng từ ngữ lóng, không cợt nhả.\n"
            "2. Nếu người dùng cố tình trêu chọc, kích động hoặc nói tục, hãy từ chối một cách lịch sự: "
            "'Tôi là trợ lý học tập giải đáp kiến thức, vui lòng đặt câu hỏi phù hợp với môn học.'\n"
            "3. Trình bày câu trả lời ngắn gọn, chia theo các bước (Step-by-step), bôi đậm ý chính để học sinh dễ tiếp thu. "
            "Tuyệt đối KHÔNG tự ý thêm các câu chào hỏi hay cảm ơn thừa thãi vào đầu/cuối câu trả lời bài tập."
        )

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=prompt_he_thong,
        )

        def generate_content():
            response_stream = model.generate_content(user_message, stream=True)
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text

        return Response(generate_content(), mimetype="text/plain")

    except Exception as e:
        print(f"Lỗi hệ thống: {e}")
        return jsonify({"error": str(e)}), 500


import os

if __name__ == '__main__':
    # Render cấp cổng qua biến môi trường PORT, nếu không có thì mặc định là 10000
    port = int(os.environ.get("PORT", 10000))
    # Phải để host='0.0.0.0' thì Render mới thấy được cổng
    app.run(host='0.0.0.0', port=port, debug=False)
