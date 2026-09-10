# LAB GUIDE — K4 Ngày 1: Khám Phá LLM API
## Hướng dẫn chi tiết từng bước | 4 tiếng

Mọi mốc dưới đây tính theo **phút kể từ lúc buổi lab bắt đầu**, không phải giờ đồng hồ — lớp sáng và lớp chiều dùng chung một nhịp.

Phiên bản hướng dẫn có giao diện đọc dễ hơn nằm trên VLearn:
[Lab 01 — Nền tảng LLM API](https://vlearn.dev/course/k4p1/reader?day=D01&part=codelab-81bf0ad781904d05a8b5e5b474a4060c-s01-doc).
Đăng nhập bằng email VinUni, mật khẩu là mã số sinh viên đã được kích hoạt;
link trên sẽ mở đúng bài sau khi bạn đăng nhập xong.

Tài liệu này dắt bạn qua từng bước của buổi lab. Mỗi block kết thúc bằng một
**CHECKPOINT** có mốc giờ — nếu đến giờ mà bạn chưa xong, đọc mục
**"Nếu bạn bị chậm"** để biết mức tối thiểu cần đạt trước khi đi tiếp.

Toàn bộ code viết trong `template.py`. Toàn bộ test chạy bằng mock —
**không tốn tiền API khi chạy pytest**.

> 💡 **Quy tắc quan trọng nhất của buổi lab:** import OpenAI **bên trong hàm**
> (`from openai import OpenAI` nằm trong thân hàm, không nằm đầu file).
> Lý do: các bài test thay thế (mock) `openai.OpenAI` — nếu bạn import ở đầu
> file, hàm của bạn giữ tham chiếu đến class thật và test sẽ gọi API thật
> → fail vì không có key.

---

# Trước Khi Bắt Đầu · Mỗi File Hoạt Động Như Thế Nào?

Bạn sẽ làm việc với nhiều file, nhưng **chỉ viết phần code chính trong
`template.py` và câu trả lời trong `exercises.md`**. Các file còn lại cung
cấp hướng dẫn, dependency, test và công cụ chấm điểm.

## Sơ đồ hoạt động của repo

```text
.env ───────────────────────────────┐
                                   ↓
requirements.txt ── cài thư viện → template.py ← bạn điền các TODO
                                      ↑   ↓
                                      │  phản hồi, token, chi phí,
                                      │  history và thống kê
                                      │
tests/test_part*.py ── mock API ─────┘
          ↑
          └──────── grade.py chạy test và tính điểm

LAB_GUIDE.md ── hướng dẫn cách làm từng bước
README.md ───── tổng quan, cài đặt, chạy test và nộp bài
exercises.md ── ghi lại quan sát và câu trả lời của bạn
```

## `README.md` — Bản đồ tổng quan

Đây là file nên đọc đầu tiên. README giải thích:

- Lab học gì và sản phẩm cuối cùng là gì.
- Bốn Part và những gì bạn xây trong mỗi Part.
- Các khái niệm nền: message role, temperature, top-p, token, chi phí,
  latency, streaming, persona.

README trả lời câu hỏi "mình đang xây cái gì và vì sao". Mọi bước thực hành —
cài môi trường, cấu hình API key, làm từng task, chạy test, chấm điểm, nộp bài
— đều nằm trong `LAB_GUIDE.md`, tức là file bạn đang đọc.

## `LAB_GUIDE.md` — Hướng dẫn thực hành từng bước

Đây là file bạn đang đọc. Nội dung được chia theo khung giờ và checkpoint.
Mỗi block có:

1. Mục tiêu kiến thức.
2. Đoạn code minh họa.
3. Các bước triển khai từng hàm trong `template.py`.
4. Lệnh test riêng cho block đó.
5. Phương án tối thiểu nếu bạn bị chậm tiến độ.

Guide không tự chạy code. Nó là tài liệu hướng dẫn để bạn biết phải sửa gì,
vì sao cần sửa và dùng lệnh nào để xác nhận kết quả.

## `template.py` — Chương trình chính bạn cần hoàn thiện

Đây là trung tâm của lab. File đã có sẵn:

- Import cơ bản và `load_dotenv()` để đọc cấu hình từ `.env`.
- Tên model và bảng giá ước tính.
- Chữ ký hàm, kiểu trả về, docstring và gợi ý cho từng task.
- Các dòng `raise NotImplementedError(...)` đánh dấu phần chưa làm.
- Entry point `if __name__ == "__main__"` để chạy demo thật.

Bạn hoàn thiện các hàm theo thứ tự:

| Part | Hàm | Chức năng |
|---|---|---|
| 1 | `call_openai()` | Gọi Chat Completions API, trả text và độ trễ. |
| 1 | `call_openai_mini()` | Tái sử dụng hàm trên với model nhỏ hơn. |
| 1 | `compare_models()` | So sánh phản hồi, latency và chi phí ước tính. |
| 2 | `chat_with_system_prompt()` | Gửi persona và câu hỏi với đúng message role. |
| 2 | `count_tokens()` | Đếm token bằng `tiktoken`, có phương án dự phòng. |
| 2 | `estimate_cost()` | Tính token và chi phí input/output. |
| 3 | `streaming_chatbot()` | Chat nhiều lượt và in dần phản hồi từ stream. |
| 3 | `retry_with_backoff()` | Thử lại khi thao tác gặp lỗi tạm thời. |
| 4 | `run_assistant()` | Ghép persona, history, stream, retry và thống kê. |
| Bonus | `batch_compare()` | So sánh model với nhiều prompt. |
| Bonus | `format_comparison_table()` | Trình bày kết quả so sánh thành bảng text. |

Khi chạy `python template.py`, Python thực thi phần demo ở cuối file. Demo
gọi API thật nên chỉ chạy được sau khi bạn đã hoàn thiện các hàm liên quan và
cấu hình API key hợp lệ.

## `.env.example` và `.env` — Cấu hình bí mật

`.env.example` là file mẫu an toàn để commit. Bạn copy nó thành một file mới, đặt tên là `.env`, rồi
điền API key thật và có thể đổi endpoint/model:

```text
.env.example ── copy ──> .env ── load_dotenv() ──> template.py
```

- `.env.example`: chỉ chứa placeholder và hướng dẫn cấu hình.
- `.env`: chứa key thật trên máy của bạn; không được commit hoặc nộp bài.
- `OPENAI_API_KEY`: khóa xác thực với nhà cung cấp API.
- `OPENAI_BASE_URL`: endpoint thay thế khi dùng dịch vụ tương thích OpenAI.
- `LAB_MODEL`, `LAB_MINI_MODEL`: ghi đè tên model mặc định.

Nếu chỉ chạy pytest, bạn không cần tạo `.env` vì test dùng mock.

## `requirements.txt` — Danh sách thư viện

Lệnh `python -m pip install -r requirements.txt` đọc file này và cài:

| Thư viện | Vai trò |
|---|---|
| `openai` | Cung cấp client để gọi API. |
| `tiktoken` | Mã hóa text và đếm token. |
| `pytest` | Tìm và chạy các bài kiểm thử. |
| `python-dotenv` | Đọc biến môi trường từ file `.env`. |

Bạn thường không cần sửa `requirements.txt` trong lab này.

## `tests/` — Đặc tả và kiểm tra tự động

Thư mục này chứa test tương ứng với từng part:

| File | Kiểm tra |
|---|---|
| `tests/test_part1.py` | Cách gọi API, tham số, latency và kết quả so sánh. |
| `tests/test_part2.py` | System prompt, token, fallback và công thức chi phí. |
| `tests/test_part3.py` | Streaming, giới hạn history và lịch retry. |
| `tests/test_part4.py` | Trợ lý CLI cơ bản và kịch bản hội thoại nhiều lượt. |
| `tests/_loader.py` | Chọn file lời giải để import vào test. |
| `tests/__init__.py` | Đánh dấu `tests` là một Python package. |

Khi chạy pytest, `_loader.py` ưu tiên nạp `solution/solution.py` nếu file đó
tồn tại; nếu chưa có, nó nạp `template.py`. Các test thay client OpenAI thật
bằng mock, kiểm tra tham số hàm nhận được và dựng response/chunk giả. Vì vậy:

- Test không gửi prompt ra Internet.
- Test không dùng API key và không tốn tiền.
- Kết quả test ổn định, không phụ thuộc nội dung ngẫu nhiên từ model.
- Bạn không nên sửa test để làm bài pass.

## `grade.py` — Chấm điểm tự động

Khi chạy `python grade.py`, chương trình:

1. Chọn `solution/solution.py` và `solution/exercises.md` nếu thư mục
   `solution/` đã tồn tại; nếu không, dùng file ở thư mục gốc.
2. Chạy 5 nhóm test bằng pytest.
3. Đếm số test pass trong từng nhóm và quy đổi thành điểm.
4. Kiểm tra 9 placeholder trong `exercises.md` đã được thay bằng câu trả lời.
5. In bảng điểm trên thang 100.

`grade.py` chỉ đọc và chấm bài; nó không tự sửa code của bạn.

Thang điểm của lab:

| Hạng mục | Cách kiểm tra | Điểm |
|---|---|---:|
| Part 1 — API cơ bản | `tests/test_part1.py` | 15 |
| Part 2 — System prompt và token | `tests/test_part2.py` | 15 |
| Part 3 — Streaming và retry | `tests/test_part3.py` | 15 |
| Part 4 — Trợ lý CLI cơ bản | `tests/test_part4.py -k Basic` | 15 |
| Demo — Kịch bản hội thoại | `tests/test_part4.py -k Scenario` | 15 |
| `exercises.md` — 9 câu trả lời | Kiểm tra mức độ hoàn thành | 25 |
| **Tổng** | | **100** |

Điểm test trong từng nhóm tỷ lệ với số test pass. Điểm `exercises.md` được
tính tự động theo số placeholder đã thay; giảng viên có thể đánh giá thêm
chất lượng nội dung khi chấm thủ công.

## `exercises.md` — Phiếu quan sát và phản ánh

File này có 9 câu hỏi, được chia theo bốn block. Sau mỗi checkpoint, bạn ghi
lại kết quả thí nghiệm và giải thích điều mình quan sát được. Để hệ thống ghi
nhận là đã trả lời, hãy thay dòng placeholder `*Câu trả lời của bạn*` bằng
nội dung thực tế.

Không nên đợi đến cuối buổi mới viết toàn bộ `exercises.md`, vì một số câu
hỏi cần bạn so sánh trực tiếp các kết quả vừa chạy.

## `.gitignore` — Ngăn commit file không nên chia sẻ

File này yêu cầu Git bỏ qua các nội dung như `.env`, môi trường ảo, cache
Python và file sinh tạm. Quan trọng nhất là `.env`: API key thật không được
đưa vào lịch sử Git.

## `solution/` — Thư mục bài làm được tạo ở cuối lab

Thư mục này chưa có sẵn lúc bắt đầu. Trước khi nộp, bạn tạo nó và copy bài làm
vào; nó được commit cùng repo và là thứ giảng viên chấm:

```text
solution/
├── solution.py       # bản hoàn thiện của template.py
└── exercises.md      # 9 câu đã trả lời
```

Sau khi `solution/solution.py` tồn tại, cả `tests/_loader.py` lẫn `grade.py`
đều ưu tiên chấm bản trong `solution/`. Vì vậy, nếu bạn tiếp tục sửa
`template.py`, nhớ copy lại bản mới nhất sang `solution/solution.py` trước
khi chấm lần cuối.

## Luồng làm việc khuyến nghị

```text
Đọc README.md
    ↓
Cài requirements.txt và tạo .env nếu cần gọi thật
    ↓
Đọc task trong LAB_GUIDE.md + docstring tương ứng trong template.py
    ↓
Sửa một TODO → chạy test_part tương ứng → sửa lỗi → test lại
    ↓
Ghi câu trả lời vào exercises.md
    ↓
Chạy toàn bộ tests → chạy grade.py
    ↓
Tạo solution/ → copy bản mới nhất → chấm lại → push fork → dán link
```

---

# 🕘 phút 0–60 · Mở Đầu & Setup

Giảng viên giới thiệu tổng quan (10'). Song song, bạn setup môi trường:

### Yêu cầu

- Python 3.10 trở lên.
- Terminal: PowerShell/Command Prompt trên Windows hoặc Terminal trên
  macOS/Linux.
- Kết nối mạng để cài các thư viện trong `requirements.txt`.
- API key OpenAI hoặc NVIDIA NIM nếu muốn chạy model thật. Pytest không cần
  API key vì toàn bộ lời gọi API đều được mock.

Kiểm tra phiên bản Python:

```bash
python --version
```

Trên macOS/Linux, dùng `python3 --version` nếu máy không nhận lệnh `python`.

**Bước 1.** Mở terminal tại thư mục lab, tạo môi trường ảo và cài thư viện.

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Dấu hiệu venv đã bật: đầu dòng lệnh hiện `(.venv)`. Nếu PowerShell chặn
script, chạy một lần `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
-Scope CurrentUser`, hoặc dùng Command Prompt: `.venv\Scripts\activate.bat`.

**Bước 2.** Thiết lập API key qua file `.env` (giảng viên cung cấp key dùng
chung của lớp):
```bash
cp .env.example .env             # Windows: copy .env.example .env
```
Mở file `.env` vừa tạo, thay `sk-your-key-here` bằng key thật. `template.py`
đã gọi sẵn `load_dotenv()` nên key được nạp tự động — không cần `export`.
Key chỉ cần cho phần **chạy thật** (demo, exercises); pytest không cần key.
`.env` đã nằm trong `.gitignore` — không bao giờ commit key.

> 🆓 **Không có key OpenAI?** Lấy key **miễn phí** từ NVIDIA NIM theo
> [Phụ lục B](#phụ-lục-b--lấy-api-key-miễn-phí-từ-nvidia-nim) — chỉ mất
> ~5 phút đăng ký, không cần thẻ tín dụng, và không phải sửa dòng code nào.

**Bước 3.** Làm nóng bộ mã hóa của `tiktoken` (chỉ cần chạy một lần, cần mạng):
```bash
python -c "import tiktoken; tiktoken.get_encoding('o200k_base'); print('tiktoken OK')"
```
Lần đầu, lệnh này tải khoảng 3–4 MB và có thể mất vài chục giây. Làm ngay bây
giờ để Block 2 không phải chờ: nếu để tới lúc đó, `pytest` sẽ đứng im rất lâu ở
lần gọi `count_tokens` đầu tiên và trông hệt như bị treo.

**Bước 4.** Chạy thử bộ test:
```bash
pytest tests/ -v
```

### ✅ CHECKPOINT 0 (phút 60)
Lệnh trên phải **chạy được và báo fail hàng loạt** với thông báo
`NotImplementedError` — đó là dấu hiệu môi trường đã đúng, chỉ còn thiếu code
của bạn. Con số chính xác khi chưa viết dòng nào:

```text
33 failed, 2 passed
```

(Hai test pass là hai test chỉ kiểm tra hàm có tồn tại.) Nếu gặp
`ModuleNotFoundError: No module named 'openai'` → môi trường ảo chưa activate
hoặc chưa `pip install`.

---

# 🕘 phút 60–100 · BLOCK 1: API Cơ Bản

### Mục tiêu
- Gọi Chat Completions API, đo độ trễ
- Hiểu tham số `model`, `temperature`, `top_p`, `max_tokens`
- So sánh GPT-4o với GPT-4o-mini về chất lượng / độ trễ / chi phí

### Kiến thức nền (giảng viên demo 10')

Một lời gọi Chat Completions cơ bản:

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Xin chào!"}],
    temperature=0.7,   # 0.0 = ổn định, càng cao càng "sáng tạo"
    top_p=0.9,         # nucleus sampling — thường chỉ chỉnh 1 trong 2
    max_tokens=256,    # chặn trần độ dài output (và chi phí!)
)
text = response.choices[0].message.content
```

Ví dụ chạy sẵn để tham khảo thêm: [Google Colab của khóa](https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing)

### Task 1.1 — `call_openai` (~20')

**Bước 1.** Mở `template.py`, tìm hàm `call_openai`. Đọc kỹ docstring —
chữ ký hàm và kiểu trả về là "hợp đồng" mà test sẽ kiểm tra, đừng sửa chúng.

**Bước 2.** Xóa dòng `raise NotImplementedError(...)`, viết phần thân:
```python
from openai import OpenAI          # import TRONG hàm — xem quy tắc ở đầu guide

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

**Bước 3.** Đo thời gian quanh lời gọi API — `latency` là thời gian **chỉ của
lời gọi mạng**, nên phép đo phải nằm sát trước và sau `create(...)`:
```python
start = time.perf_counter()
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": prompt}],
    temperature=temperature,
    top_p=top_p,
    max_tokens=max_tokens,
)
latency = time.perf_counter() - start
```
Dùng `time.perf_counter()` chứ không phải `time.time()`: đây là đồng hồ chuyên
để đo khoảng thời gian, độ phân giải cao trên mọi hệ điều hành. Trên Windows
với Python 3.12 trở xuống, `time.time()` chỉ nhích mỗi ~15,6 ms — lời gọi đã
được mock trong test chạy xong trong vài chục micro giây, nên hiệu số ra đúng
`0.0` và test `latency > 0` sẽ trượt dù code của bạn hoàn toàn đúng.

**Bước 4.** Trả về tuple `(text, latency)`:
```python
return response.choices[0].message.content, latency
```

**Bước 5.** Kiểm tra ngay (đừng đợi xong hết mới test):
```bash
pytest tests/test_part1.py -k "TestCallOpenAI and not Mini" -v
```
Kỳ vọng **3 passed**. Đừng dùng `-k CallOpenAI`: chuỗi đó khớp cả lớp
`TestCallOpenAIMini`, nên bạn sẽ chạy 6 test và thấy 3 test của Task 1.2 báo
đỏ trong khi bạn còn chưa làm tới nó.

### Task 1.2 — `call_openai_mini` (~5')

**Bước 1.** Hàm này chỉ là "phím tắt" gọi model rẻ hơn — tái sử dụng Task 1.1,
đừng copy-paste code:
```python
return call_openai(prompt, model=OPENAI_MINI_MODEL,
                   temperature=temperature, top_p=top_p, max_tokens=max_tokens)
```
Tái sử dụng nghĩa là: sau này sửa `call_openai` một chỗ, cả hai model đều
hưởng lợi.

### Task 1.3 — `compare_models` (~15')

**Bước 1.** Gọi lần lượt hai hàm trên với cùng `prompt`:
```python
gpt4o_text, gpt4o_latency = call_openai(prompt)
mini_text, mini_latency = call_openai_mini(prompt)
```

**Bước 2.** Ước tính chi phí output của GPT-4o. Ở block này ta dùng ước lượng
thô "0.75 từ ≈ 1 token" (Block 2 sẽ tính chính xác bằng tiktoken):
```python
cost = (len(gpt4o_text.split()) / 0.75) / 1000 \
       * PRICING_PER_1K_TOKENS["gpt-4o"]["output"]
```

**Bước 3.** Ghép dict đúng 5 key như docstring (`gpt4o_response`,
`mini_response`, `gpt4o_latency`, `mini_latency`, `gpt4o_cost_estimate`).
Tên key phải khớp từng ký tự — test so sánh chính xác.

### ✅ CHECKPOINT 1 (phút 100)
```bash
pytest tests/test_part1.py -v
```
Kỳ vọng: **10 passed** —
```
tests/test_part1.py::TestCallOpenAI::test_returns_non_empty_string PASSED
...
========================= 10 passed in ~1s =========================
```
Nếu có API key, chạy thử thật để cảm nhận độ trễ hai model:
```bash
python -c "from template import compare_models; \
           print(compare_models('Việt Nam có bao nhiêu tỉnh?'))"
```
Sau đó trả lời **Câu 1.1 → 1.3** trong `exercises.md`.

**Nếu bạn bị chậm:** tối thiểu Task 1.1 phải pass
(`-k "TestCallOpenAI and not Mini"`) rồi sang
Block 2 — Task 1.2/1.3 quay lại làm trong giờ wrap-up. Block 2 và 3 không
phụ thuộc Task 1.3.

---

# 🕘 phút 100–140 · BLOCK 2: System Prompt & Token

### Mục tiêu
- Dùng message role `system` để định persona cho model
- Đếm token thật bằng `tiktoken` thay vì đoán từ số từ
- Tính chi phí tách bạch input / output

### Kiến thức nền (giảng viên demo 10')

`messages` là một **danh sách hội thoại**, không chỉ một câu hỏi. Message đầu
tiên với `role: "system"` là "chỉ thị đạo diễn" — model sẽ bám theo nó trong
toàn bộ phản hồi:

```python
messages = [
    {"role": "system", "content": "Bạn là giáo viên tiểu học..."},
    {"role": "user", "content": "Giải thích blockchain là gì?"},
]
```

Chi phí API tính theo **token**, không theo từ, và giá input khác giá output
(xem `PRICING_PER_1K_TOKENS` trong template). `tiktoken` là thư viện chính
thức để đếm token đúng như OpenAI tính tiền.

### Task 2.1 — `chat_with_system_prompt` (~15')

**Bước 1.** Copy cấu trúc `call_openai` của bạn (import trong hàm, đo giờ,
trả tuple) — điểm khác duy nhất là `messages` có 2 phần tử:
```python
messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]
```

**Bước 2.** Chạy `pytest tests/test_part2.py -k SystemPrompt -v`. Test sẽ
kiểm tra cả việc nội dung `system_prompt` thực sự được gửi lên — nếu bạn quên
truyền hoặc đảo role, test chỉ tên lỗi rất rõ.

### Task 2.2 — `count_tokens` (~10')

**Bước 1.** Viết phần "đường vui" (happy path):
```python
import tiktoken
enc = tiktoken.encoding_for_model(model)
return len(enc.encode(text))
```

**Bước 2.** Bọc try/except. `tiktoken` cần mạng lần đầu để tải bảng mã hóa và
sẽ raise nếu gặp tên model lạ — hàm tiện ích không được crash vì chuyện đó:
```python
try:
    import tiktoken
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))
except Exception:
    return max(1, len(text) // 4)   # ước lượng: 1 token ≈ 4 ký tự
```
Test có một case truyền model không tồn tại — chính là để kiểm tra fallback này.

### Task 2.3 — `estimate_cost` (~15')

**Bước 1.** Đếm token hai chiều bằng hàm vừa viết:
```python
input_tokens = count_tokens(prompt, model)
output_tokens = count_tokens(response, model)
```

**Bước 2.** Tra bảng giá và tính. Lưu ý đơn vị là **USD trên 1000 token**:
```python
pricing = PRICING_PER_1K_TOKENS.get(model, PRICING_PER_1K_TOKENS["gpt-4o"])
input_cost = input_tokens / 1000 * pricing["input"]
output_cost = output_tokens / 1000 * pricing["output"]
```
Phải dùng `.get(...)` có giá trị dự phòng, đừng viết `PRICING_PER_1K_TOKENS[model]`.
`PRICING_PER_1K_TOKENS` chỉ liệt kê hai model OpenAI, nên nếu bạn dùng key
NVIDIA NIM (Phụ lục B) thì `model` mặc định là `meta/llama-...` và dấu ngoặc
vuông sẽ ném `KeyError`. Lỗi đó làm trượt 3 test của Part 2 **và** cả 5 test
kịch bản của Part 4 — tổng cộng gần 20 điểm, mà thông báo lỗi lại hiện ra ở
Part 4 nên rất khó lần về đúng nguyên nhân.

**Bước 3.** Trả dict 5 key: `input_tokens`, `output_tokens`, `input_cost`,
`output_cost`, `total_cost` (= input + output).

### ✅ CHECKPOINT 2 (phút 140)
```bash
pytest tests/test_part2.py -v
```
Kỳ vọng: **10 passed**. Thử nhanh với Python REPL:
```python
>>> from template import count_tokens, estimate_cost
>>> count_tokens("Xin chào Việt Nam")
7        # con số có thể khác chút tùy encoding
>>> estimate_cost("câu hỏi dài...", "câu trả lời dài...")["total_cost"]
0.000123...
```
Trả lời **Câu 2.1 → 2.2** trong `exercises.md` (cần API key để chạy so sánh
persona thật).

**Nếu bạn bị chậm:** ưu tiên Task 2.2 và 2.3 — Block 4 gọi thẳng
`count_tokens` và `estimate_cost` để cộng dồn thống kê, thiếu chúng là
`run_assistant` không chạy. `count_tokens` tạm chỉ dùng nhánh dự phòng
`len(text) // 4` cũng được, hoàn thiện tiktoken sau. Task 2.1
(`chat_with_system_prompt`) đứng riêng: Block 4 tự ghép system prompt vào
`messages` chứ không gọi lại hàm này, nên nếu hết giờ thì để nó sau cùng.

---

# ☕ phút 140–150 · GIẢI LAO

Đứng dậy, rời màn hình. Block 3 cần não tươi.

---

# 🕘 phút 150–190 · BLOCK 3: Streaming & Độ Bền

### Mục tiêu
- Stream phản hồi token-by-token cho UX tức thời
- Duy trì lịch sử hội thoại có giới hạn
- Retry với exponential backoff khi API lỗi tạm thời

### Kiến thức nền (giảng viên demo 10')

Với `stream=True`, API trả về **iterator các chunk** thay vì một response
trọn vẹn — in ra đến đâu người dùng đọc đến đó:

```python
stream = client.chat.completions.create(model=..., messages=..., stream=True)
reply = ""
for chunk in stream:
    delta = chunk.choices[0].delta.content or ""   # chunk cuối là None → or ""
    print(delta, end="", flush=True)
    reply += delta
```

API thật thỉnh thoảng lỗi tạm thời (quá tải, mạng chập chờn). Chiến lược
chuẩn: thử lại với thời gian chờ **tăng gấp đôi** sau mỗi lần
(0.1s → 0.2s → 0.4s...) để không dồn dập đánh vào server đang nghẽn.

### Task 3.1 — `streaming_chatbot` (~25')

**Bước 1.** Dựng khung vòng lặp trước, chưa cần API:
```python
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
history = []
while True:
    user_msg = input("Bạn: ")
    if user_msg.strip().lower() in ("quit", "exit"):
        break
```

**Bước 2.** Trong vòng lặp, ghép messages = history + tin nhắn mới rồi gọi
API với `stream=True`:
```python
messages = history + [{"role": "user", "content": user_msg}]
stream = client.chat.completions.create(
    model=OPENAI_MODEL, messages=messages, stream=True,
)
```

**Bước 3.** In từng chunk và gom lại thành `reply` (dùng mẫu ở phần kiến
thức nền — nhớ `or ""` cho chunk cuối).

**Bước 4.** Cập nhật history sau mỗi lượt và **cắt còn 3 lượt cuối**. Một
lượt = 1 message user + 1 message assistant, nên 3 lượt = 6 message:
```python
history.append({"role": "user", "content": user_msg})
history.append({"role": "assistant", "content": reply})
history = history[-6:]
```
Vì sao phải cắt? History dài ra mãi thì mỗi lượt sau càng tốn token input —
chi phí tăng theo thời gian trò chuyện.

### Task 3.2 — `retry_with_backoff` (~15')

**Bước 1.** Viết vòng lặp `max_retries + 1` lần thử (lần đầu + các lần retry):
```python
for attempt in range(max_retries + 1):
    try:
        return fn()
    except Exception:
        if attempt == max_retries:
            raise                          # hết lượt → ném lỗi cuối cùng ra
        time.sleep(base_delay * (2 ** attempt))
```
Lưu ý `raise` trần (không tham số) giữ nguyên exception gốc — người gọi biết
chính xác lỗi gì.

### ✅ CHECKPOINT 3 (phút 190)
```bash
pytest tests/test_part3.py -v
```
Kỳ vọng: **6 passed**. Nếu có API key, chạy chatbot thật:
```bash
python -c "from template import streaming_chatbot; streaming_chatbot()"
```
Hỏi 2–3 câu liên tiếp và để ý: câu sau có "nhớ" ngữ cảnh câu trước không?
Trả lời **Câu 3.1 → 3.2** trong `exercises.md`.

**Nếu bạn bị chậm:** ưu tiên Task 3.2 (`retry_with_backoff` — ngắn và Block 4
cần nó), phần streaming trong Task 3.1 có thể hoàn thiện ngay trong Block 4
vì mini-project dùng lại đúng kỹ thuật đó.

---

# 🕘 phút 190–230 · BLOCK 4: MINI-PROJECT — Trợ Lý CLI Hoàn Chỉnh

### Mục tiêu
Ghép **tất cả** những gì đã xây thành một hàm `run_assistant`: persona qua
system prompt + streaming + history + retry + thống kê token/chi phí.

### Thiết kế trước khi code (5')

Đọc docstring `run_assistant` trong `template.py` — nó có sẵn khung sườn.
Ba điểm khác với `streaming_chatbot`:

1. **Đầu vào tiêm được:** đọc input qua tham số `get_input` (mặc định là
   `input`). Nhờ đó test tự động "gõ phím hộ" bạn được — đây là kỹ thuật
   dependency injection bạn sẽ gặp lại suốt khóa.
2. **System prompt cố định:** mọi lời gọi API đều bắt đầu bằng
   `{"role": "system", "content": persona}` — persona không bị trôi mất khi
   history bị cắt.
3. **Trả về thống kê** thay vì None — sản phẩm thật cần đo được chi phí.

### Các bước (25')

**Bước 1.** Khởi tạo trạng thái phiên:
```python
if get_input is None:
    get_input = input
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
history, num_turns, total_tokens, total_cost = [], 0, 0, 0.0
```

**Bước 2.** Vòng lặp chính — kiểm tra `max_turns` **trước khi** đọc input
(để `max_turns=0` thoát ngay không chờ gõ phím):
```python
while True:
    if max_turns is not None and num_turns >= max_turns:
        break
    user_msg = get_input()
    if user_msg.strip().lower() in ("quit", "exit"):
        break
```

**Bước 3.** Ghép messages **có system prompt đứng đầu**:
```python
messages = ([{"role": "system", "content": persona}]
            + history + [{"role": "user", "content": user_msg}])
```

**Bước 4.** Gọi API qua retry — bọc lời gọi trong lambda để
`retry_with_backoff` gọi lại được khi lỗi:
```python
stream = retry_with_backoff(
    lambda: client.chat.completions.create(
        model=OPENAI_MODEL, messages=messages, stream=True,
    )
)
```

**Bước 5.** Gom reply từ stream (như Block 3), rồi cập nhật history + cắt
còn 6 message.

**Bước 6.** Cộng dồn thống kê mỗi lượt:
```python
num_turns += 1
total_tokens += count_tokens(user_msg) + count_tokens(reply)
total_cost += estimate_cost(user_msg, reply)["total_cost"]
```

**Bước 7.** Trả về dict 4 key: `num_turns`, `total_tokens`, `total_cost`,
`history`.

### Kiểm tra & demo (10')

```bash
pytest tests/test_part4.py -v          # cả basic + scenario
python template.py                     # demo thật (cần API key)
```

Nhóm test `Scenario` chính là "demo tự động": nó giả lập một cuộc hội thoại
nhiều lượt và kiểm tra stats, history, stream — đây là 15 điểm demo của bạn.

### ✅ CHECKPOINT 4 (phút 230)
```bash
pytest tests/test_part4.py -v
```
Kỳ vọng: **9 passed** (4 Basic + 5 Scenario).
Trả lời **Câu 4.1 → 4.2** trong `exercises.md`.

**Nếu bạn bị chậm:** làm đúng thứ tự Bước 1 → 2 → 7 trước (vòng lặp + thoát
+ trả dict) — chỉ vậy đã pass nhóm Basic (15đ). Phần API/stream (Bước 3–6)
thêm sau để lấy nhóm Scenario.

---


# 🕘 phút 230–240 · WRAP-UP & NỘP BÀI

Bài nộp của bạn là **link tới fork GitHub của chính bạn**, dán trên trang bài
Lab ở VLearn. Không nén zip, không upload file lên LMS.

### Bước 1 — Kiểm tra bản làm việc lần cuối

Rà lại các phần bắt buộc:

- `template.py`: đã triển khai các hàm Part 1–4 và không đổi chữ ký hàm.
- `exercises.md`: cả 9 dòng `> *Câu trả lời của bạn*` đã được thay bằng câu
  trả lời thật. Thay nguyên dòng, đừng viết thêm bên dưới mà giữ lại dòng cũ —
  bộ chấm nhìn đúng dòng đó để biết câu nào đã làm.

Chạy toàn bộ test từ thư mục gốc của lab:

```bash
pytest tests/ -v
```

Kỳ vọng: **35 passed**.

### Bước 2 — Tạo thư mục `solution/`

Khi `solution/solution.py` tồn tại, cả `tests/_loader.py` lẫn `grade.py` đều ưu
tiên bản trong `solution/` thay vì `template.py` ở thư mục gốc.

#### macOS/Linux

```bash
mkdir -p solution
cp template.py solution/solution.py
cp exercises.md solution/exercises.md
```

#### Windows — PowerShell

```powershell
New-Item -ItemType Directory -Force solution
Copy-Item template.py solution\solution.py -Force
Copy-Item exercises.md solution\exercises.md -Force
```

Lưu ý tên file code phải đổi từ `template.py` thành **`solution.py`**.

### Bước 3 — Chấm lại chính bản sẽ nộp

```bash
pytest tests/ -v
python grade.py
```

Hai dòng đầu `grade.py` in ra cho biết chính xác nó đang chấm file nào — đọc
kỹ hai dòng đó:

```text
Đang chấm code:      solution/solution.py
Đang chấm exercises: solution/exercises.md
```

Nếu vẫn thấy `template.py` thì thư mục `solution/` chưa được tạo đúng.

> Từ thời điểm này, nếu tiếp tục sửa `template.py` hoặc `exercises.md` ở thư
> mục gốc, bạn phải copy lại sang `solution/` trước khi chấm và nộp.

### Bước 4 — Kiểm tra không có API key trong bài

Fork của bạn là **repo công khai**. Một API key lọt vào lịch sử Git là key bị
lộ ra Internet; xoá commit sau đó cũng không thu hồi được key đã lộ.

```bash
git status
```

`.env` phải **không** xuất hiện trong danh sách file sẽ được commit — repo đã
có sẵn `.gitignore` chặn nó. Nếu bạn thấy `.env` trong danh sách, dừng lại và
báo giảng viên trước khi commit. Cũng đừng dán key vào `template.py`,
`exercises.md` hay ảnh chụp màn hình.

### Bước 5 — Đẩy bài lên fork của bạn

```bash
git add -A
git commit -m "Hoan thanh Lab 01"
git push
```

Nếu bạn clone từ repo gốc thay vì từ fork của mình, `git push` sẽ bị từ chối vì
bạn không có quyền ghi. Khi đó: fork repo trên GitHub, rồi trỏ `origin` sang
fork của bạn:

```bash
git remote set-url origin https://github.com/<tên-github-của-bạn>/K4-L3-Day1-AI-LLM-Foundation.git
git push -u origin main
```

### Bước 6 — Dán link trên trang bài Lab ở VLearn

> **Hạn nộp: 23:59 thứ Sáu 11/09/2026 (giờ Việt Nam).**
>
> Sau mốc đó hệ thống **không nhận bài nữa** — bấm nút nộp sẽ báo lỗi, chứ không
> phải nộp trễ rồi trừ điểm. Trang nộp bài không hiển thị hạn này, nên hãy tự
> ghi lại.
>
> Nộp sớm một bản chạy được, rồi vẫn sửa và nộp lại được trước hạn: mỗi lab chỉ
> giữ bản mới nhất.

Mở [phần nộp bài của Lab 01](https://vlearn.dev/course/k4p1/reader?day=D01&part=codelab-81bf0ad781904d05a8b5e5b474a4060c-submit),
dán **link fork GitHub của bạn** và chọn rating. Bấm
**Xác nhận đã nộp bài** — chỉ nút này mới đánh dấu Lab hoàn thành.

Ô nhập có chữ gợi ý "Dán link GitHub, Drive hoặc LMS" — đó là chữ chung của nền
tảng. Lab này chỉ nhận **link fork GitHub**; đừng nộp link Drive.

Trước khi dán, mở link fork trong một cửa sổ trình duyệt ẩn danh để chắc chắn
người khác xem được. Fork private thì giảng viên không chấm được bài.

### Checklist nộp bài nhanh

- [ ] `pytest tests/ -v` cho **35 passed**.
- [ ] Cả 9 dòng `> *Câu trả lời của bạn*` trong `exercises.md` đã được thay.
- [ ] `python grade.py` hiển thị đúng điểm mong đợi và đang chấm bản trong
      `solution/`.
- [ ] `git status` không có `.env`, không có API key trong file nào đã commit.
- [ ] Fork đã push lên GitHub và mở được bằng cửa sổ ẩn danh.
- [ ] Đã dán link fork và bấm **Xác nhận đã nộp bài** trên trang bài Lab ở VLearn,
      trước **23:59 ngày 11/09/2026**.


## Phụ Lục A — Lỗi Thường Gặp

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Test fail dù code "chạy thật" được | Import `OpenAI` ở đầu file | Chuyển `from openai import OpenAI` vào **trong** hàm |
| `AuthenticationError` khi chạy pytest | Code đang gọi API thật thay vì mock | Cùng nguyên nhân trên — mock không "bắt" được import đầu file |
| `KeyError: 'gpt4o_response'` | Tên key trong dict gõ sai | So từng ký tự với docstring |
| Chunk cuối làm crash (`TypeError: ... NoneType`) | Quên `or ""` khi đọc `delta.content` | `delta = chunk.choices[0].delta.content or ""` |
| History phình to, chi phí tăng dần | Quên cắt history | `history = history[-6:]` sau mỗi lượt |
| `StopIteration` trong test scenario | Đọc input nhiều hơn số lượt kịch bản | Kiểm tra `max_turns` **trước** khi `get_input()` |
| tiktoken treo/lỗi khi offline | Lần đầu cần mạng để tải encoding | Fallback `max(1, len(text) // 4)` trong try/except |
| `KeyError: 'meta/llama-...'` ở Part 4 | `estimate_cost` tra bảng giá bằng `[model]` khi dùng NIM | `PRICING_PER_1K_TOKENS.get(model, PRICING_PER_1K_TOKENS["gpt-4o"])` |
| `latency` bằng `0.0` trên Windows | `time.time()` chỉ nhích mỗi ~15,6 ms (Python ≤ 3.12) | Dùng `time.perf_counter()` để đo khoảng thời gian |

---

## Phụ Lục B — Lấy API Key MIỄN PHÍ từ NVIDIA NIM

NVIDIA NIM cung cấp endpoint **tương thích chuẩn OpenAI** với hàng nghìn
lượt gọi miễn phí — đủ dư cho cả buổi lab. Code của bạn **không phải sửa
dòng nào**: OpenAI SDK tự đọc `OPENAI_BASE_URL` từ `.env`, còn tên model
đã được `template.py` đọc qua biến `LAB_MODEL` / `LAB_MINI_MODEL`.

### Bước 1 — Đăng ký tài khoản (miễn phí, không cần thẻ)

1. Mở [build.nvidia.com](https://build.nvidia.com)
2. Bấm **Login** (góc phải trên) → chọn **Create Account** nếu chưa có.
   Dùng email trường hoặc email cá nhân đều được.
3. Xác nhận email là xong.

### Bước 2 — Tạo API key

1. Sau khi đăng nhập, mở một model bất kỳ trong catalog — ví dụ
   [meta/llama-3.1-8b-instruct](https://build.nvidia.com/meta/llama-3_1-8b-instruct)
2. Ở panel code bên phải, bấm **Get API Key** → **Generate Key**
3. Copy key dạng `nvapi-...` — **lưu ngay**, key chỉ hiện một lần

### Bước 3 — Cấu hình `.env`

Mở `.env` và thay bằng (mẫu có sẵn trong `.env.example`):

```bash
OPENAI_API_KEY=nvapi-key-cua-ban
OPENAI_BASE_URL=https://integrate.api.nvidia.com/v1
LAB_MODEL=meta/llama-3.3-70b-instruct
LAB_MINI_MODEL=meta/llama-3.1-8b-instruct
```

Cặp model trên thay vai GPT-4o (model lớn) và GPT-4o-mini (model nhỏ) —
bài so sánh 70B vs 8B của Block 1 vẫn nguyên giá trị: bạn sẽ thấy đúng
sự đánh đổi chất lượng / tốc độ giữa model lớn và nhỏ.

### Bước 4 — Kiểm tra key hoạt động

```bash
python -c "
from template import call_openai
text, latency = call_openai('Chào bạn, hãy trả lời bằng 1 câu tiếng Việt.')
print(f'[{latency:.2f}s] {text}')
"
```

Thấy câu trả lời tiếng Việt in ra là xong — làm tiếp lab như bình thường.

### Lưu ý khi dùng NIM

- **pytest và `python grade.py` không cần key** — mọi test đều mock, nên
  điểm số không phụ thuộc bạn dùng OpenAI hay NIM.
- `count_tokens` không có bảng mã cho model Llama → tự động rơi về ước
  lượng `len(text) // 4` (đúng như thiết kế fallback ở Task 2.2).
- `estimate_cost` với model lạ dùng giá gpt-4o làm **tham chiếu học tập**
  (NIM thực tế miễn phí) — xem gợi ý `.get(...)` trong docstring Task 2.3.
- Nếu gặp lỗi 429 (hết hạn mức tạm thời) — chính là lúc `retry_with_backoff`
  của Task 3.2 tỏa sáng.
