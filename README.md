# OWASP Top 10 & Reconnaissance Labs

## Giới thiệu chung
Các bài lab và kịch bản khai thác trong 3 session được thực hiện trên ứng dụng web Pygoat có chứa các lỗ hổng **OWASP Top 10 (2021)** và một số bài lab trên PortSwigger, bao phủ toàn bộ quy trình từ giai đoạn Trinh sát (Reconnaissance/OSINT) đến đánh giá, khai thác lỗ hổng và đề xuất phương án khắc phục. 

## Công cụ sử dụng
* **Proxy & Tương tác Web:** Burp Suite (Proxy, Repeater, Intruder, Decoder).
* **Thu thập thông tin (Recon/OSINT):** Nmap, DNSdumpster, Subfinder, Assetfinder, dnsenum, Whois, Dig, nslookup.
* **Dò quét thư mục & Tệp tin:** Dirsearch, Gobuster, Dirb.
* **Dịch ngược & Bẻ khóa (Cracking):** Hashcat, md5online.
* **OSINT & Dorking:** Google Dorks, Github Dorking, Wayback Machine.
* **Lập trình & Tự động hóa:** Python (Sử dụng `requests`, `BeautifulSoup`, `itertools`, regex).

## Danh mục lỗ hổng đã phân tích và khai thác (OWASP Top 10)

### 1. Broken Access Control (A01)
* **Thao túng Cookie & User-Agent:** Giả mạo Cookie và User-Agent (pygoat_admin browser) để leo thang đặc quyền lên tài khoản Admin.
* **Path Traversal via HTTP Method Bypass:** Lợi dụng lỗ hổng không kiểm tra đầu vào của phương thức HTTP `CONNECT` (so với `GET`) để đọc tệp tin hệ thống (`/etc/passwd`).
* **Symlink Attack via File Upload:** Upload tệp tin nén `.tar` chứa liên kết mềm (symlink) để đọc tệp mã nguồn (`admin.html`) và tệp cấu hình hệ thống.
* **Multi-step Process Bypass:** Bỏ qua bước xác thực cuối cùng bằng cách hoán đổi Session Cookie trong quy trình nâng quyền nhiều bước.

### 2. Cryptographic Failures (A02)
* **Weak Hashing Algorithms:** Dịch ngược mật khẩu bị mã hóa bằng thuật toán MD5 lỗi thời.
* **Custom Hash Function Reversing:** Phân tích mã nguồn và bẻ khóa thuật toán mã hóa SHA-256 không sử dụng Salt bằng từ điển thông qua `Hashcat`.
* **Plaintext Data in Cookie:** Phân tích lỗi ứng dụng lưu trữ thông tin định danh (Session/Username) dưới dạng bản rõ.

### 3. Injection (A03)
* **SQL Injection (SQLi):** Vượt qua cơ chế đăng nhập bằng Tautology, sử dụng Error-based và Union-based (bypass mệnh đề `LIMIT` bằng `/**/`) để trích xuất cấu trúc cơ sở dữ liệu (`information_schema`).
* **Command Injection:** Chèn lệnh hệ điều hành Linux thông qua chức năng tra cứu DNS (`; cat /etc/shadow`).
* **Server-Side Template Injection (SSTI):** Khai thác template engine của Django (`{% load log %}`) để lấy dữ liệu nội bộ.

### 4. Insecure Design (A04)
* **Logic Flaws / Sybil Attack:** Trục lợi quy trình đăng ký không xác thực danh tính để tạo hàng loạt tài khoản ảo, vắt kiệt tài nguyên hệ thống (Resource Exhaustion).

### 5. Security Misconfiguration (A05)
* **HTTP Header Manipulation:** Thao túng HTTP Header (`X-Host`) để truy cập chức năng quản trị.
* **Debug Mode Exposure:** Khai thác tính năng Debug bật sai quy định (500 Error Page) để lấy Secret Key và biến môi trường.
* **JWT Forging:** Bắt gói tin, lấy Secret Key có cấu hình yếu từ các lỗ hổng trước đó để tự mã hóa và giả mạo JSON Web Token (JWT).
* **Backup & Database Exposure:** Lợi dụng lỗi Directory Listing (`/backup`) để tải tệp `.bak`, làm lộ lọt mã nguồn Java và thông tin tài khoản Database PostgreSQL (Hardcoded credentials).

### 6. Vulnerable and Outdated Components (A06)
* **RCE via Pillow Library:** Khai thác lỗ hổng từ thư viện Pillow cũ của Python (CVE-2022-22817) để thực thi mã từ xa thông qua hàm `exec()`.
* **Business Logic DoS:** Lợi dụng cơ chế khóa tài khoản lỏng lẻo để Brute-force và khóa vĩnh viễn tài khoản quản trị Admin.

### 7. Identification and Authentication Failures (A07)
* **Username Enumeration:** Dò tìm tài khoản hợp lệ thông qua sự khác biệt về độ dài phản hồi (Response Length) và thời gian xử lý (Response Timing) của máy chủ.
* **2FA Bypass (Direct Object Reference):** Vượt qua lớp bảo mật 2FA bằng cách ép buộc điều hướng URL trực tiếp đến trang account sau khi hoàn thành lớp xác thực thứ nhất.

### 8. Software and Data Integrity Failures (A08)
* **Insecure Deserialization:** Chỉnh sửa đối tượng lưu trong Cookie, serialize bằng thư viện `Pickle` và mã hóa Base64 để leo thang đặc quyền.
* **DOM-based XSS & Clickjacking:** Lừa người dùng click vào Iframe ẩn để trigger XSS; kết hợp Content Injection 404 để bypass cấu hình Content Security Policy (CSP) và đánh cắp Cookie.

### 9. Security Logging and Monitoring Failures (A09)
* **Log Leakage:** Dò quét bằng `Dirb` và phát hiện mật khẩu người dùng bị ghi đè dạng plaintext vào endpoint nhật ký (`/debug`) không yêu cầu xác thực.

### 10. Server-Side Request Forgery - SSRF (A10)
* **Local File Read:** Cấu hình payload ép máy chủ đọc các tệp tin hệ thống nội bộ (`/etc/passwd`).
* **SSRF TOCTOU (DNS Rebinding):** Vượt qua các bộ lọc Whitelist/Blacklist IP của máy chủ bằng kỹ thuật **DNS Rebinding** (khai thác khoảng hở thời gian TOCTOU - Time of Check to Time of Use).

