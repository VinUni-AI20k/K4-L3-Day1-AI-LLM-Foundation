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
> Ở temperature 0.0, câu trả lời thường ổn định và ít biến thể; khi tăng lên 0.5 và 1.0, cách diễn đạt và lựa chọn sự thật đa dạng hơn. Ở 1.5, phản hồi sáng tạo hơn nhưng cũng dễ lan man hoặc kém nhất quán, nên đây là xu hướng chứ không phải quy luật tuyệt đối.

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Tôi sẽ bắt đầu ở khoảng 0.2–0.4. Mức thấp giúp câu trả lời nhất quán, chính xác và ít bịa đặt hơn, nhưng vẫn đủ linh hoạt để diễn đạt tự nhiên; các câu trả lời quan trọng vẫn cần dựa trên dữ liệu và quy trình kiểm tra của sản phẩm.

### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 3 lần,
mỗi lần trung bình ~350 token đầu ra.

**Ước tính GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này? Nêu một
trường hợp GPT-4o xứng đáng với chi phí và một trường hợp nên dùng mini:**
> Với cùng 350 token output, giá output của GPT-4o là 0.010 USD/1K token còn mini là 0.0006 USD/1K token, nên GPT-4o đắt khoảng 16.7 lần; workload 10.000 người dùng x 3 lượt chỉ làm thay đổi tổng số tiền, không làm đổi tỷ lệ này. GPT-4o phù hợp cho phân tích khó hoặc câu trả lời cần chất lượng cao, còn mini phù hợp cho phân loại, FAQ và các tác vụ lặp lại có lưu lượng lớn.

---

## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích blockchain là gì?"** nhưng hai system prompt khác nhau:
- "Bạn là giáo viên tiểu học, giải thích thật đơn giản cho trẻ 8 tuổi."
- "Bạn là chuyên gia tài chính, trả lời chuyên sâu bằng thuật ngữ kỹ thuật."

**Hai phản hồi khác nhau như thế nào (độ dài, từ vựng, ví dụ)? System prompt
ảnh hưởng đến hành vi model ra sao?** (3–4 câu)
> Persona giáo viên tiểu học thường tạo câu trả lời ngắn, dùng từ đơn giản và ví dụ gần gũi như các khối lego hoặc sổ cái dễ hiểu. Persona chuyên gia tài chính thường trả lời dài hơn, dùng thuật ngữ như sổ cái phân tán, đồng thuận và mật mã, đồng thời nêu nhiều chi tiết kỹ thuật. System prompt định hướng vai trò, đối tượng, giọng điệu và mức độ chi tiết của model, nên cùng một user prompt có thể tạo ra hai phản hồi rất khác nhau.

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~100 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Vì sao tiếng Việt thường tốn
nhiều token hơn tiếng Anh cùng độ dài?**
> Với đoạn khoảng 100 từ tôi đo được khoảng 155 token bằng tiktoken, trong khi ước lượng theo công thức 100 / 0.75 là khoảng 133 token, chênh khoảng 16.5% so với số tiktoken. Đây chỉ là một mẫu nên tỷ lệ thay đổi theo nội dung. Tiếng Việt có dấu, cách tách âm tiết bằng khoảng trắng và bộ mã hóa được tối ưu khác nhau, nên cùng số từ có thể cần nhiều token hơn tiếng Anh.

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì
non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming hữu ích nhất với chatbot, trợ lý viết và câu trả lời dài vì người dùng thấy phần đầu ngay, cảm nhận thời gian chờ ngắn hơn và có thể dừng khi đã đủ thông tin. Non-streaming phù hợp với tác vụ cần toàn bộ kết quả trước khi xử lý tiếp, chẳng hạn parse một JSON, chấm kiểm tra hoặc lưu một bản ghi nguyên vẹn. Vì vậy lựa chọn phụ thuộc vào yêu cầu UX và định dạng đầu ra, không chỉ vào tốc độ tổng của model.

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**So với delay cố định (ví dụ luôn chờ 1 giây), exponential backoff có lợi
thế gì khi API bị quá tải? Điều gì xảy ra nếu hàng nghìn client cùng retry
với delay cố định giống nhau?**
> Exponential backoff làm khoảng chờ tăng dần, ví dụ 0.1, 0.2 rồi 0.4 giây, nên giảm áp lực lên server đang quá tải và cho hệ thống thời gian phục hồi. Nếu hàng nghìn client cùng retry sau đúng 1 giây, chúng tạo ra các đợt request đồng bộ, làm nghẽn server và có thể khiến lỗi kéo dài. Trong sản phẩm thực tế có thể thêm jitter để các lần retry không trùng thời điểm.

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Bạn chọn persona gì cho trợ lý của mình? Viết lại system prompt đó và giải
thích 1–2 lựa chọn từ ngữ quan trọng trong prompt (ví dụ: vì sao yêu cầu
"trả lời ngắn gọn", vì sao chỉ định ngôn ngữ...):**
> Persona tôi chọn: “Bạn là trợ giảng thân thiện của khóa AI, trả lời ngắn gọn, chính xác bằng tiếng Việt; nếu khái niệm khó, hãy giải thích bằng ví dụ đơn giản và nói rõ khi không chắc chắn.” Cụm “bằng tiếng Việt” giữ ngôn ngữ nhất quán với người học, còn “ngắn gọn” giúp giảm thời gian đọc và chi phí token. Yêu cầu nói rõ khi không chắc chắn khuyến khích trợ lý không trình bày phỏng đoán như sự thật.

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn hiện có hạn chế lớn nhất là gì (ví dụ: history chỉ 3 lượt,
không có bộ nhớ dài hạn, không kiểm duyệt nội dung...)? Đề xuất một cải
thiện cụ thể và mô tả ngắn cách triển khai:**
> Hạn chế lớn nhất là history chỉ giữ ba lượt, nên các thông tin quan trọng ở đầu phiên có thể bị mất. Tôi sẽ thêm bộ nhớ tóm tắt: sau mỗi vài lượt, gửi history cũ cho một hàm tóm tắt, lưu bản tóm tắt vào trạng thái phiên rồi đưa nó vào system context cùng sáu message gần nhất. Cách này giữ được thông tin dài hạn mà vẫn giới hạn số token gửi lên API.

---

## Danh Sách Kiểm Tra Nộp Bài

- [ ] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [ ] Cả 4 checkpoint pytest đều pass
- [ ] Tất cả 9 câu trong file này đã được trả lời
- [ ] Đã copy bài làm vào folder `solution/`, push lên fork và dán link trên trang bài Lab ở VLearn trước 23:59 ngày 11/09/2026
