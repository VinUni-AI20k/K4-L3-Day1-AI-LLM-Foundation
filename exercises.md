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
> *Ở temp thấp (từ 0 đến 0.5), câu trả lời thường có tính tương đồng cao, và sẽ trả lời dựa trên các thông tin phổ biến, và ở temp cao (từ 1 đến 1.5), câu trả lời có xu hướng trở nên sáng tạo hơn.*

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> *Cho một chatbot hỗ trợ khách hàng, mình sẽ để temperature quanh 0.5, để đủ đảm bảo rằng câu trả lời của Chatbot trả lời đúng theo yêu cầu và các chính sách có sẵn của cửa hàng, nhưng vẫn có đủ sự tự nhiên trong câu trả lời mà không bị sai lệch hay "sáng tạo" quá.*

### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 3 lần,
mỗi lần trung bình ~350 token đầu ra.

**Ước tính GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này? Nêu một
trường hợp GPT-4o xứng đáng với chi phí và một trường hợp nên dùng mini:**
> *Chỉ dựa vào chi phí đầu ra, đầu vào của hai model, GPT-4o sẽ đắt hơn GPT-4o-mini khoảng 16 lần. Nếu vẫn lấy ví dụ là cho Chatbot CSKH, thì chỉ nên dùng GPT-4o khi xử lý các vấn đề khiếu nại có tính phức tạp cao; và các vấn đề tạp vụ như truy vấn Database và phản hồi đơn giản thì chỉ nên dùng GPT-4o-mini để tiết kiệm chi phí.*

---

## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích blockchain là gì?"** nhưng hai system prompt khác nhau:
- "Bạn là giáo viên tiểu học, giải thích thật đơn giản cho trẻ 8 tuổi."
- "Bạn là chuyên gia tài chính, trả lời chuyên sâu bằng thuật ngữ kỹ thuật."

**Hai phản hồi khác nhau như thế nào (độ dài, từ vựng, ví dụ)? System prompt
ảnh hưởng đến hành vi model ra sao?** (3–4 câu)
> *Với System Prompt role Giáo viên tiểu học, câu trả lời ngắn gọn và sử dụng từ ngữ đơn giản, cùng với phép ẩn dụ để đơn giản hóa Concept của blockchain, còn với Role Chuyên gia Tài chính, câu trả lời thường đi sâu vào phần lý thuyết của Blockchain, cũng như sử dụng vốn từ thuật ngữ chuyên sâu liên quan đến chủ đề. Từ đó có thể rút ra rằng System prompt có thể ảnh hưởng đến một vài yếu tố của câu trả lời như sau: Mức độ phức tạp của kiến trúc câu trả lời, vốn từ sử dụng trong câu trả lời, và scope kiến thức được sử dụng trong câu trả lời.*

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~100 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Vì sao tiếng Việt thường tốn
nhiều token hơn tiếng Anh cùng độ dài?**
> *Số token được ghi nhận bởi tiktoken cao hơn khoảng 30% so với ước lượng còn lại. Tiếng Việt thường tốn nhiều token hơn Tiếng Anh mặc dù cùng độ dài, thường là do các tokenizer của các LLM thường được tối ưu cho Tiếng Anh hơn, và do sự khác biệt về bảng chữ cái và từ điển của Tiếng Việt, khiến cho các từ Tiếng Việt thường có thể bị tách ra thành nhiều sub-word tokens hơn.*

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì
non-streaming lại phù hợp hơn?** (1 đoạn văn)
> *Streaming thường sẽ chỉ quan trọng cho các tác vụ tương tác trực tiếp với người dùng, như là Chatbot hoặc trợ lý ảo AI. Non-streaming thì sẽ phù hợp cho các tác vụ không cần ngay lập tức phải đưa ra câu trả lời cho người dùng, ví dụ như các Process và Data trung gian như Agent Tool Call, hoặc Back-end processes.*

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**So với delay cố định (ví dụ luôn chờ 1 giây), exponential backoff có lợi
thế gì khi API bị quá tải? Điều gì xảy ra nếu hàng nghìn client cùng retry
với delay cố định giống nhau?**
> *Exponential Backoff giúp giảm thiểu nguy cơ quá tải API bằng cách phân tán thời gian retry của Client, tránh việc tất cả các Request gửi lại cùng một thời điểm, gây quá tải cho Server. Trong trường hợp hàng nghìn client cùng retry với delay cố định giống nhau, tình huống hàng nghìn client đồng loạt retry cùng lúc sau thời gian chết rất dễ xảy ra, khiến hệ thống API quá tải và dẫn đến lỗi dây chuyền cho hệ thống lân cận.*

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Bạn chọn persona gì cho trợ lý của mình? Viết lại system prompt đó và giải
thích 1–2 lựa chọn từ ngữ quan trọng trong prompt (ví dụ: vì sao yêu cầu
"trả lời ngắn gọn", vì sao chỉ định ngôn ngữ...):**
> *Cho trợ lý của mình, mình đã đặt persona/system prompt là: "Bạn là một trợ lý lập trình AI giàu kinh nghiệm nhưng gần gũi, chuyên hỗ trợ sinh viên và người mới bắt đầu (fresher). Nhiệm vụ của bạn là giải thích các khái niệm kỹ thuật (như API, Docker, LLM) một cách dễ hiểu, sử dụng ví dụ thực tế và code minh họa ngắn gọn. Luôn trả lời bằng tiếng Việt, giữ thái độ khuyến khích và kiên nhẫn.". Lựa chọn từ ngữ quan trọng với mình là "giải thích... một cách dễ hiểu" do mục tiêu của mình là được giải thích phần code mà AI đã làm để mình có thể hiểu một cách hiệu quả nhất.*

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn hiện có hạn chế lớn nhất là gì (ví dụ: history chỉ 3 lượt,
không có bộ nhớ dài hạn, không kiểm duyệt nội dung...)? Đề xuất một cải
thiện cụ thể và mô tả ngắn cách triển khai:**
> *Hiện tại Context Window bị giới hạn chỉ nhớ 6 message cuối cùng. Đề xuất cải thiện: Sử dụng Tóm tắt Ngữ cảnh Dynamic để tóm tắt phần lịch sử hội thoại đã qua cho cuộc hội thoại tương lai.*

---

## Danh Sách Kiểm Tra Nộp Bài

- [ ] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [ ] Cả 4 checkpoint pytest đều pass
- [ ] Tất cả 9 câu trong file này đã được trả lời
- [ ] Đã copy bài làm vào folder `solution/`, push lên fork và dán link trên trang bài Lab ở VLearn trước 23:59 ngày 11/09/2026
