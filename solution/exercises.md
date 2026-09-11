# K4 — Ngày 1: Bài Tập &amp; Phản Ánh

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

> *Temperature càng nhỏ thì văn phong, thông tin trong kết quả trả về khá an toàn, nội dung ngắn, sát nhất với chủ đề. Temperature càng lớn thì kết quả trả về nội dung dài hơn, văn phong sáng tạo hơn.*

### Câu 1.2 — Chọn temperature cho sản phẩm

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**

> *Bối cảnh là chatbot hỗ trợ khách hàng =&gt; đặt temperature giá trị thấp, &lt;= 0.5 để chatbot có thể đưa ra kết quả sát nhất, chính xác nhất cho khách hàng. Nếu để temperature &gt; 0.5 chatbot có thể đưa ra những thông tin sai lệnh, tự suy luận những thông tin không chính xác tới khách hàng.*  

### Câu 1.3 — Đánh đổi chi phí

Kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 3 lần,
mỗi lần trung bình ~350 token đầu ra.

**Ước tính GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này? Nêu một
trường hợp GPT-4o xứng đáng với chi phí và một trường hợp nên dùng mini:**

> Với workload bạn đưa ra, GPT-4o đắt hơn GPT-4o mini khoảng 16,7 lần nếu chỉ xét output tokens.
>
> Ví dụ trường hợp GPT-4o xứng đáng: Phân tích toàn bộ thông tin khách hàng + lịch sử giao dịch + yêu cầu hiện tại → đề xuất package/offer phù hợp.
>
> Ví dụ trường hợp GPT-4o-mini: Những task đơn giản, có cấu trúc, volume rất lớn như translate, generate tags, summarize **ngắn,** rewrite đơn giản...

---

## Block 2 — System Prompt &amp; Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona

Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích blockchain là gì?"** nhưng hai system prompt khác nhau:

- "Bạn là giáo viên tiểu học, giải thích thật đơn giản cho trẻ 8 tuổi."
- "Bạn là chuyên gia tài chính, trả lời chuyên sâu bằng thuật ngữ kỹ thuật."

**Hai phản hồi khác nhau như thế nào (độ dài, từ vựng, ví dụ)? System prompt
ảnh hưởng đến hành vi model ra sao?** (3–4 câu)

> *Kết quả lần gọi 1:* 539 ký tự, 115 từ
>
> Kêt quả lần gọi 2: rất nhiều ký tự và từ vựng
>
> Phản hồi lần 2 giải thích chi tiết hơn lần 1
>
> System prompt nếu phân role càng cao cấp và yêu cầu trả lời chi tiết hoặc chuyên sâu thì kết quả phản hồi càng chi tiết

### Câu 2.2 — tiktoken vs đếm từ

Chọn một đoạn văn tiếng Việt ~100 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Vì sao tiếng Việt thường tốn
nhiều token hơn tiếng Anh cùng độ dài?**

> *Số lượng token cho đoạn văn tiếng việt ~100 từ = 115-120 token.*
>
> Số lượng token cho đoạn văn tiếng Anh ~ 100 từ = 100 token.
>
> Chênh lệch nhau khoảng từ 15-20%. Nguyên nhân là do cách tokenizer chia văn bản thành token. 

---

## Block 3 — Streaming &amp; Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming

**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì
non-streaming lại phù hợp hơn?** (1 đoạn văn)

> Streaming quan trọng khi người dùng phải chờ model tạo ra nhiều nội dung.
>
> Non-streaming phù hợp khi ứng dụng cần toàn bộ kết quả trước khi xử lý tiếp

### Câu 3.2 — Vì sao backoff theo cấp số nhân?

**So với delay cố định (ví dụ luôn chờ 1 giây), exponential backoff có lợi
thế gì khi API bị quá tải? Điều gì xảy ra nếu hàng nghìn client cùng retry
với delay cố định giống nhau?**

> *Trong trường hợp hàng nghìn client cùng retry với delay cố định giống nhau(vd: khoảng cách giữa các lần retry = 1s) thì hệ thống sẽ phải chịu áp lực rất lớn khi xử lý hàng nghin request cùng lúc mỗi giây. Cơ chế Exponential Backoff hiểu đơn giản sẽ làm giãn khoảng thời gian delay mỗi lần retry ra lâu hơn, không cố định, giúp cho hệ thống giảm tải và tránh xử lý hàng nghìn request cùng lúc. Ví dụ: có 5 lượt retry sau khi áp dụng cơ chế Exponential Backoff là 1s, 2s, 4s, 8s, 16s thay vì 5 lượt retry 1s, 1s, 1s, 1s, 1s.*

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona

**Bạn chọn persona gì cho trợ lý của mình? Viết lại system prompt đó và giải
thích 1–2 lựa chọn từ ngữ quan trọng trong prompt (ví dụ: vì sao yêu cầu
"trả lời ngắn gọn", vì sao chỉ định ngôn ngữ...):**

> Tôi chọn persona là trợ lý tổng hợp tin tức.
>
> - Tìm kiếm Internet để cập nhật tin mới và xác minh thông tin.
> - Ưu tiên nguồn chính thống, uy tín và nhiều nguồn độc lập.
> - Phân biệt rõ sự thật, thông tin được báo cáo và suy đoán.
> - Tóm tắt ngắn gọn, khách quan, tập trung vào thông tin quan trọng.
> - Nêu nguồn khi cần và không trình bày thông tin chưa xác minh như sự thật.
> - Trả lời bằng ngôn ngữ của người dùng.
>
> Lý do chọn hai điểm chính:
>
> - “Tìm kiếm Internet”: tin tức thay đổi liên tục, nên cần dữ liệu mới thay vì chỉ dựa vào kiến thức có sẵn.
> - “Phân biệt sự thật và suy đoán”: giúp hạn chế việc biến tin đồn hoặc nhận định thành thông tin chính thức.

### Câu 4.2 — Hạn chế &amp; cải thiện

**Trợ lý của bạn hiện có hạn chế lớn nhất là gì (ví dụ: history chỉ 3 lượt,
không có bộ nhớ dài hạn, không kiểm duyệt nội dung...)? Đề xuất một cải
thiện cụ thể và mô tả ngắn cách triển khai:**

> Với trợ lý tổng hợp tin tức này, tôi cho rằng hạn chế lớn nhất là thiếu bộ nhớ ngữ cảnh dài hạn. Sau một vài lượt hội thoại, trợ lý có thể không còn nhớ người dùng đang theo dõi chủ đề nào, nguồn nào họ ưu tiên hoặc các tin tức đã trao đổi trước đó.
>
> Cải thiện đề xuất: xây dựng conversation memory.
>
> Cách triển khai ngắn gọn:
>
> - Lưu lịch sử hội thoại và các thông tin quan trọng như chủ đề quan tâm, từ khóa, nguồn tin ưu tiên.
> - Khi có câu hỏi mới, lấy các thông tin liên quan từ memory đưa vào context của LLM.
> - Giới hạn dung lượng bằng cách tóm tắt các cuộc hội thoại cũ thay vì gửi toàn bộ lịch sử.
> - Có thể dùng database + vector database để lưu và tìm lại các thông tin liên quan.
>
> Kết quả là trợ lý có thể hiểu các câu hỏi nối tiếp như **“**Còn diễn biến mới của vụ này thì sao?**”** mà không cần người dùng nhắc lại toàn bộ bối cảnh.

---

## Danh Sách Kiểm Tra Nộp Bài

- [x] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [x] Cả 4 checkpoint pytest đều pass
- [x] Tất cả 9 câu trong file này đã được trả lời
- [ ] Đã copy bài làm vào folder `solution/`, push lên fork và dán link trên trang bài Lab ở VLearn trước 23:59 ngày 11/09/2026

