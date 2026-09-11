# K4 — Ngày 1: Bài Tập & Phản Ánh
## Khám Phá LLM API | Phiếu Thực Hành

**Thời lượng:** 4 tiếng
**Cách làm:** Trả lời từng câu ngay sau khi hoàn thành block tương ứng —
đừng để dồn hết về cuối buổi. Thay dòng `*Câu trả lời của bạn*` bằng câu
trả lời thật (chấm tự động sẽ đếm số câu đã trả lời).

---

## Block 1 — API Cơ Bản (trả lời sau Checkpoint 1)

### Câu 1.1 — Độ nhạy của temperature
Gọi `call_openai` với temperature 0.0, 0.5, 1.0 và 1.5 dùng prompt
**"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi temp ở 0.0 câu trả lời có ít sáng tạo và đúng hơn, tập chung vào sự chính xác. khi ở mức 0.5-1.0, câu trả lời sáng tại hơn, văn phong tự nhiên đa dạng và phong phú hơn. Khi lên mức 1.5, câu từ trở nên bay bổng, khó dự đoán hơn nhưng bắt đầu có dấu hiệu lan man và giảm tính liên kết logic.

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Khi để hỗ trợ khách hàng thì độ chích xác nên đặt lên hàng đầu, vì vậy temp nên để thấp (chẳng hạn 0.0-0.3)

### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 3 lần,
mỗi lần trung bình ~350 token đầu ra.

**Ước tính GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này? Nêu một
trường hợp GPT-4o xứng đáng với chi phí và một trường hợp nên dùng mini:**
> GPT-4o đắt hơn GPT-4o-mini khoảng 16.67 lần (cho phần output: 0.010 / 0.0006; tiêu tốn khoảng $105/ngày so với chỉ $6.30/ngày của mini). Nên dùng GPT-4o cho các tác vụ phức tạp đòi hỏi suy luận nhiều bước, phân tích tài liệu pháp lý/tài chính chuyên sâu, hỗ trợ chẩn đoán y tế hoặc viết mã nguồn phức tạp nơi mà sai sót nhỏ có thể gây thiệt hại lớn. Dùng GPT-4o-mini: Các tác vụ thường nhật với lưu lượng truy cập lớn như phân loại phản hồi khách hàng, trích xuất thông tin có cấu trúc cơ bản, tóm tắt đoạn văn bản ngắn hoặc chatbot trả lời các câu hỏi thường gặp (FAQ).

---

## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích blockchain là gì?"** nhưng hai system prompt khác nhau:
- "Bạn là giáo viên tiểu học, giải thích thật đơn giản cho trẻ 8 tuổi."
- "Bạn là chuyên gia tài chính, trả lời chuyên sâu bằng thuật ngữ kỹ thuật."

**Hai phản hồi khác nhau như thế nào (độ dài, từ vựng, ví dụ)? System prompt
ảnh hưởng đến hành vi model ra sao?** (3–4 câu)
> Hai phản hồi có sự khác biệt rõ rệt: phản hồi cho trẻ 8 tuổi có dung lượng ngắn gọn, từ vựng đơn giản và dùng ví dụ ẩn dụ trực quan (như cuốn sổ ghi chép chung của lớp mà không ai tự ý tẩy xóa được); trong khi phản hồi của chuyên gia tài chính dài hơn, trang trọng và chứa nhiều thuật ngữ chuyên môn (sổ cái phân tán, cơ chế đồng thuận, mã hóa mật mã học, phi tập trung). System prompt đóng vai trò thiết lập khung ngữ cảnh và quy định đối tượng mục tiêu, từ đó điều hướng cách chọn từ vựng, giọng điệu và phong cách giải thích của model mà không làm thay đổi câu hỏi gốc của người dùng.

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~100 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Vì sao tiếng Việt thường tốn
nhiều token hơn tiếng Anh cùng độ dài?**
> Với đoạn văn mẫu 117 từ tiếng Việt, count_tokens (tiktoken với o200k_base) cho kết quả 137 token, trong khi công thức ước lượng (117 / 0.75) cho ra 156 token, chênh lệch khoảng 12.2% (với các bộ mã hóa cũ hơn như cl100k_base, số token thực tế có thể lên đến hơn 250 token, chênh lệch trên 60%). Tiếng Việt thường tốn nhiều token hơn tiếng Anh cùng độ dài vì các thuật toán token hóa (BPE) được tối ưu chủ yếu trên kho ngữ liệu tiếng Anh, trong khi các từ tiếng Việt chứa nhiều ký tự có dấu thanh (Unicode diacritics) thường bị chia tách thành nhiều sub-word hoặc byte token nhỏ thay vì giữ nguyên một token trọn từ.

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì
non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất trong các ứng dụng hội thoại tương tác trực tiếp với người dùng cuối (như chatbot hoặc trợ lý ảo) với các câu trả lời có độ dài từ trung bình đến lớn, giúp giảm thiểu thời gian chờ nhận token đầu tiên (Time to First Token - TTFT) và mang lại cảm giác phản hồi tức thì. Ngược lại, non-streaming phù hợp hơn cho các tác vụ xử lý ngầm (background batch jobs), các luồng giao tiếp backend giữa các service (API service-to-service), hoặc khi hệ thống cần nhận toàn bộ dữ liệu hoàn chỉnh để phân tích/parse (như định dạng JSON / Structured Outputs) và kiểm duyệt nội dung (content moderation) trước khi gửi kết quả về cho client.

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**So với delay cố định (ví dụ luôn chờ 1 giây), exponential backoff có lợi
thế gì khi API bị quá tải? Điều gì xảy ra nếu hàng nghìn client cùng retry
với delay cố định giống nhau?**
> So với delay cố định, exponential backoff có lợi thế kéo dãn khoảng cách giữa các lần thử lại theo cấp số nhân (0.1s, 0.2s, 0.4s...), giúp giảm áp lực và mật độ request dồn lên máy chủ, cho server thời gian cần thiết để giải phóng tài nguyên và phục hồi sau khi quá tải. Nếu hàng nghìn client cùng retry với một khoảng delay cố định (ví dụ 1 giây), hiện tượng "Thundering Herd Problem" sẽ xảy ra: toàn bộ các client sẽ đồng loạt gửi lại request tại cùng một thời điểm, tạo thành các đợt bùng nổ lưu lượng (traffic spikes) liên tiếp đánh sập hoàn toàn khả năng hồi phục của hệ thống và gây ra lỗi diện rộng kéo dài (cascading failure).

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Bạn chọn persona gì cho trợ lý của mình? Viết lại system prompt đó và giải
thích 1–2 lựa chọn từ ngữ quan trọng trong prompt (ví dụ: vì sao yêu cầu
"trả lời ngắn gọn", vì sao chỉ định ngôn ngữ...):**
> Chọn persona là: "Bạn là trợ giảng lập trình AI thân thiện, luôn giải thích bằng tiếng Việt dễ hiểu, đưa ra các ví dụ code ngắn gọn và khuyến khích sinh viên tự tư duy.". Giải thích lựa chọn từ ngữ: 1. "ngắn gọn / ví dụ code ngắn gọn": Giúp kiểm soát trần token đầu ra (output tokens), từ đó giảm thiểu chi phí API, hạ thấp độ trễ phản hồi và tránh làm người dùng bị ngợp thông tin trên giao diện terminal. 2. "bằng tiếng Việt dễ hiểu": Định hướng rõ ràng ngôn ngữ phản hồi ngay từ đầu, tránh việc mô hình tự ý chuyển sang tiếng Anh khi gặp các thuật ngữ kỹ thuật chuyên sâu.

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn hiện có hạn chế lớn nhất là gì (ví dụ: history chỉ 3 lượt,
không có bộ nhớ dài hạn, không kiểm duyệt nội dung...)? Đề xuất một cải
thiện cụ thể và mô tả ngắn cách triển khai:**
> Hạn chế lớn nhất của trợ lý hiện tại là cơ chế cắt history cứng chỉ giữ lại 3 lượt gần nhất (history[-6:]), khiến trợ lý bị mất hoàn toàn ngữ cảnh và các thông tin quan trọng được trao đổi ở đầu phiên (như tên người dùng, ràng buộc bài toán). **Đề xuất cải thiện:** Triển khai cơ chế tóm tắt ngữ cảnh tự động (Rolling Context Summarization). **Cách triển khai:** Khi danh sách messages vượt quá ngưỡng (ví dụ 6 tin nhắn), thay vì cắt bỏ thẳng tay các tin nhắn cũ, hệ thống sẽ gọi một tác vụ ngầm yêu cầu mô hình tóm tắt lại các lượt hội thoại đã qua thành 1 đoạn văn ngắn gọn. Đoạn tóm tắt này được ghim ngay sau System prompt làm ngữ cảnh nền tảng, giúp trợ lý ghi nhớ được toàn bộ diễn biến cuộc trò chuyện mà vẫn tiết kiệm đáng kể token đầu vào.

---

## Danh Sách Kiểm Tra Nộp Bài

- [ ] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [ ] Cả 4 checkpoint pytest đều pass
- [ ] Tất cả 9 câu trong file này đã được trả lời
- [ ] Đã copy bài làm vào folder `solution/`, push lên fork và dán link trên trang bài Lab ở VLearn trước 23:59 ngày 11/09/2026
