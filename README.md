# K4 — Day 01: Khám Phá LLM API

Lab nhập môn cách một ứng dụng Python giao tiếp với mô hình ngôn ngữ lớn
(LLM) thông qua API. Nội dung đi từ một lời gọi model đơn giản đến một trợ lý
hội thoại chạy trong terminal.

Tài liệu này chỉ giới thiệu **nội dung và kiến thức của bài lab**. Hướng dẫn
cài đặt môi trường, cấu hình API key, thực hiện từng task, chạy test, chấm
điểm và nộp bài nằm trong [LAB_GUIDE.md](LAB_GUIDE.md).

---

## Bắt Đầu

Bản hướng dẫn có giao diện đọc dễ hơn nằm trên VLearn:
[Lab 01 — Nền tảng LLM API](https://vlearn.dev/course/k4p1/reader?day=D01&part=codelab-81bf0ad781904d05a8b5e5b474a4060c-s01-doc).
Nội dung giống nhau; chọn bản nào bạn thấy dễ theo hơn. Bài nộp cũng nộp ở đó.

**1. Fork repo này** trên GitHub (nút **Fork** góc phải trên), rồi clone bản
fork của bạn về máy — bài nộp cuối buổi là link tới fork đó:

```bash
git clone https://github.com/<tên-github-của-bạn>/K4-L3-Day1-AI-LLM-Foundation.git
cd K4-L3-Day1-AI-LLM-Foundation
```

Nếu bạn đã clone từ trước, lấy bản mới nhất trước khi bắt đầu:

```bash
git pull
```

**2. Tạo môi trường ảo và cài thư viện:**

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**3. Chạy thử bộ test** — phải fail hàng loạt, đó là dấu hiệu đúng:

```bash
pytest tests/ -v
```

Kỳ vọng `33 failed, 2 passed`: môi trường đã sẵn sàng, chỉ còn thiếu code của
bạn. Sau đó mở [LAB_GUIDE.md](LAB_GUIDE.md) và làm theo từng block. Bạn viết
code trong `template.py` và câu trả lời trong `exercises.md`; những file còn
lại là giàn giáo.

Pytest dùng mock nên **không cần API key và không tốn tiền**. Key chỉ cần khi
bạn muốn gọi model thật ở phần demo và hai câu trong `exercises.md`.

---

## Mục Tiêu Bài Lab

Sau khi hoàn thành, bạn có thể:

- Gọi Chat Completions API từ Python.
- Điều chỉnh cách model sinh nội dung bằng các tham số quan trọng.
- So sánh model theo chất lượng phản hồi, độ trễ và chi phí.
- Dùng system prompt để định hình vai trò và cách trả lời của model.
- Hiểu token, đếm token và ước tính chi phí input/output.
- Hiển thị phản hồi theo thời gian thực bằng streaming.
- Duy trì ngữ cảnh của cuộc hội thoại bằng message history.
- Thử lại an toàn khi API gặp lỗi tạm thời.
- Kết hợp các kỹ thuật trên thành một trợ lý CLI hoàn chỉnh.

---

## Bức Tranh Tổng Thể

Một ứng dụng LLM trong lab hoạt động theo luồng sau:

```text
Người dùng nhập câu hỏi
        ↓
Ứng dụng tạo danh sách messages
        ↓
System prompt + lịch sử hội thoại + câu hỏi mới
        ↓
Gửi request tới LLM API
        ↓
Model sinh phản hồi
        ↓
Ứng dụng hiển thị nội dung và cập nhật history
        ↓
Đếm token, ước tính chi phí và chờ câu hỏi tiếp theo
```

Lab tập trung vào lớp ứng dụng nằm giữa người dùng và model: cách tạo
request, xử lý response, quản lý trạng thái hội thoại và làm chương trình ổn
định hơn khi có lỗi.

---

## Nội Dung Chính

### Part 1 — Gọi API Và So Sánh Model

Phần đầu xây dựng lời gọi API cơ bản. Một request gồm:

- Model cần sử dụng.
- Danh sách message gửi tới model.
- Các tham số điều khiển quá trình sinh nội dung.
- Giới hạn độ dài của output.

Bạn sẽ làm việc với hai model để quan sát sự đánh đổi giữa:

- Chất lượng câu trả lời.
- Tốc độ phản hồi.
- Chi phí sử dụng.

Ba chức năng chính của phần này là:

| Chức năng | Ý nghĩa |
|---|---|
| Gọi model chính | Gửi prompt, nhận text và đo độ trễ. |
| Gọi model nhỏ | Tái sử dụng cùng logic với một model nhanh và rẻ hơn. |
| So sánh model | Đặt kết quả của hai model cạnh nhau để phân tích. |

Mục tiêu quan trọng không phải tìm ra model “tốt nhất” trong mọi trường hợp,
mà là hiểu rằng lựa chọn model phụ thuộc vào yêu cầu của sản phẩm.

### Part 2 — System Prompt, Token Và Chi Phí

Phần hai bổ sung khả năng điều khiển hành vi của model và đo lượng tài nguyên
mỗi lượt gọi sử dụng.

Bạn sẽ tìm hiểu:

- Cách system prompt định nghĩa persona, giọng điệu và nguyên tắc trả lời.
- Sự khác nhau giữa từ, ký tự và token.
- Vì sao input và output thường có đơn giá khác nhau.
- Cách ước tính chi phí của một request.

Ví dụ danh sách messages:

```python
messages = [
    {
        "role": "system",
        "content": "Bạn là trợ giảng thân thiện, trả lời ngắn gọn bằng tiếng Việt.",
    },
    {
        "role": "user",
        "content": "Giải thích token là gì.",
    },
]
```

Trong ví dụ này, system message định hướng cách model trả lời; user message
là yêu cầu thực tế cần xử lý.

### Part 3 — Streaming, History Và Retry

Phần ba chuyển từ một request độc lập sang trải nghiệm hội thoại có trạng
thái và có khả năng chịu lỗi.

Ba kỹ thuật chính gồm:

1. **Streaming:** nhận phản hồi thành nhiều chunk nhỏ và hiển thị ngay khi
   chúng được sinh ra.
2. **History:** gửi lại các message trước đó để model hiểu ngữ cảnh của câu
   hỏi mới.
3. **Retry:** thử lại sau một khoảng chờ nếu API gặp lỗi tạm thời.

History không nên tăng vô hạn. Trong lab, ứng dụng chỉ giữ ba lượt hội thoại
gần nhất. Một lượt gồm một message `user` và một message `assistant`, vì vậy
history có tối đa sáu message.

Retry sử dụng exponential backoff, nghĩa là thời gian chờ tăng gấp đôi sau
mỗi lần thất bại:

```text
Lần gọi đầu → lỗi
Chờ 0.1 giây → thử lại → lỗi
Chờ 0.2 giây → thử lại → lỗi
Chờ 0.4 giây → thử lại
```

Cách tiếp cận này giúp ứng dụng không gửi request dồn dập khi server đang
quá tải hoặc kết nối đang không ổn định.

### Part 4 — Mini-Project Trợ Lý CLI

Phần cuối kết hợp toàn bộ kiến thức thành một trợ lý dòng lệnh có:

- Persona cố định trong suốt phiên trò chuyện.
- Phản hồi được stream theo thời gian thực.
- Lịch sử ba lượt hội thoại gần nhất.
- Retry khi lời gọi API gặp lỗi.
- Điều kiện thoát bằng `quit`, `exit` hoặc giới hạn số lượt.
- Thống kê số lượt, tổng token và tổng chi phí ước tính.

Luồng xử lý của một lượt hội thoại:

```text
Đọc câu hỏi
    ↓
Kiểm tra điều kiện thoát
    ↓
Ghép persona + history + câu hỏi mới
    ↓
Gọi API qua cơ chế retry
    ↓
In từng streaming chunk và ghép reply hoàn chỉnh
    ↓
Cập nhật history
    ↓
Cập nhật token và chi phí
```

Mini-project thể hiện cấu trúc cơ bản của nhiều ứng dụng chatbot thực tế,
dù giao diện trong lab chỉ là terminal.

---

## Các Khái Niệm Cần Hiểu

### Message Roles

Mỗi message có một `role` thể hiện nguồn và mục đích của nội dung:

| Role | Vai trò |
|---|---|
| `system` | Định nghĩa cách model nên hành xử trong phiên làm việc. |
| `user` | Chứa câu hỏi hoặc yêu cầu của người dùng. |
| `assistant` | Chứa câu trả lời trước đó của model. |

Thứ tự messages có ý nghĩa. System prompt thường đứng đầu, tiếp theo là
history và cuối cùng là câu hỏi mới nhất.

### Temperature

`temperature` điều chỉnh mức ngẫu nhiên khi model chọn token tiếp theo:

- Giá trị thấp thường tạo phản hồi ổn định và dễ lặp lại hơn.
- Giá trị cao thường tạo phản hồi đa dạng hơn.

Temperature thấp phù hợp với các tác vụ cần tính nhất quán; temperature cao
có thể hữu ích với tác vụ sáng tạo. Đây là xu hướng chứ không phải cam kết
tuyệt đối về kết quả.

### Top-p

`top_p` sử dụng nucleus sampling. Model chỉ cân nhắc một nhóm token có tổng
xác suất đạt ngưỡng đã chọn.

`temperature` và `top_p` đều ảnh hưởng đến cách lấy mẫu. Khi thử nghiệm,
thường nên thay đổi một tham số tại một thời điểm để dễ giải thích nguyên
nhân của sự khác biệt.

### Max Tokens

`max_tokens` đặt giới hạn trên cho số token model được phép sinh. Tham số này
giúp kiểm soát:

- Độ dài tối đa của câu trả lời.
- Thời gian sinh phản hồi.
- Chi phí output có thể phát sinh.

Giới hạn quá thấp có thể khiến câu trả lời bị dừng giữa chừng.

### Token

Token là đơn vị văn bản model xử lý. Một token không nhất thiết tương ứng với
một từ. Cách tách token phụ thuộc vào bộ mã hóa và model.

Ví dụ, dấu câu, khoảng trắng, từ tiếng Việt có dấu hoặc một từ tiếng Anh dài
có thể được tách thành những số lượng token khác nhau. Vì vậy, đếm từ chỉ là
ước lượng thô; thư viện tokenizer cho kết quả phù hợp hơn.

### Chi Phí Input Và Output

Chi phí được ước tính riêng cho hai chiều:

```text
input_cost  = input_tokens  / 1000 × đơn giá input
output_cost = output_tokens / 1000 × đơn giá output
total_cost  = input_cost + output_cost
```

Khi history dài hơn, toàn bộ phần history được gửi lại có thể làm số input
token tăng theo từng lượt. Đây là một lý do cần giới hạn lịch sử hội thoại.

Bảng giá trong bài chỉ phục vụ mục đích học tập và có thể thay đổi theo thời
gian. Một sản phẩm thực tế phải dùng bảng giá hiện hành của nhà cung cấp.

### Latency Và Streaming

Latency là khoảng thời gian từ khi gửi request đến khi nhận kết quả. Trong
lab, bạn đo thời gian quanh lời gọi API để so sánh model.

Streaming không nhất thiết làm giảm tổng thời gian model xử lý, nhưng cải
thiện cảm nhận của người dùng vì nội dung đầu tiên xuất hiện sớm hơn.

### Persona

Persona là tập chỉ dẫn mô tả model nên đóng vai ai và trả lời như thế nào.
Một persona có thể quy định:

- Vai trò chuyên môn.
- Đối tượng người đọc.
- Ngôn ngữ và giọng điệu.
- Mức độ chi tiết.
- Những nguyên tắc hoặc giới hạn phải tuân theo.

Persona rõ ràng giúp phản hồi nhất quán hơn, nhưng không thay thế việc kiểm
tra chất lượng và tính chính xác của nội dung.

---

## Sản Phẩm Cuối Cùng

Kết quả của lab là một trợ lý CLI có thể trò chuyện nhiều lượt. Về mặt chức
năng, trợ lý sẽ:

```text
Nhận persona khi khởi động
        ↓
Nhận nhiều câu hỏi từ người dùng
        ↓
Gửi đúng ngữ cảnh cho model
        ↓
Stream câu trả lời ra terminal
        ↓
Duy trì history có giới hạn
        ↓
Trả về thống kê của toàn bộ phiên chat
```

Ví dụ trải nghiệm mong đợi:

```text
Bạn: Giải thích API bằng một ví dụ đơn giản.
Trợ lý: API giống như người phục vụ nhận yêu cầu của bạn...

Bạn: Cho mình một ví dụ trong ứng dụng thời tiết.
Trợ lý: Khi ứng dụng cần biết nhiệt độ hiện tại...

Bạn: quit
```

Câu hỏi thứ hai có thể dựa vào câu hỏi đầu tiên vì ứng dụng gửi lại lịch sử
hội thoại cho model.

---

## Kết Quả Học Tập Mong Đợi

Lab không chỉ yêu cầu code chạy được. Sau khi hoàn thành, bạn nên giải thích
được:

- Một request Chat Completions được cấu tạo như thế nào.
- System prompt ảnh hưởng đến phản hồi ra sao.
- Khi nào nên ưu tiên model lớn hoặc model nhỏ.
- Vì sao token quan trọng đối với giới hạn ngữ cảnh và chi phí.
- Streaming cải thiện trải nghiệm người dùng như thế nào.
- Vì sao history cần được giới hạn.
- Exponential backoff giúp ứng dụng ổn định hơn ra sao.
- Cách các thành phần kết hợp thành một vòng lặp chatbot hoàn chỉnh.

Toàn bộ hướng dẫn thực hành bắt đầu tại [LAB_GUIDE.md](LAB_GUIDE.md).
