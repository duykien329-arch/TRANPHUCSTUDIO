ADD STUDIO VIDEO LAB PRO
========================

TÍNH NĂNG
- Chạy trên Windows bằng Python, xuất MP4 dọc 540x960.
- Bản HTML dùng Safari/iPhone và trình duyệt máy tính để xem trước, thử ghi video.
- Tạo video từ nhiều ảnh + tiêu đề + nội dung theo từng cảnh.
- 5 mẫu: cyber, anime, matrix, pink, cinema.
- 4 chuyển cảnh: fade, slide, zoom, glitch.
- Hiệu ứng phát sáng, lưới số, hạt chuyển động, thanh tiến trình.
- Bản Python ghép nhạc nền vào MP4, điều chỉnh âm lượng.

A. WINDOWS — XUẤT MP4 CÓ NHẠC
1. Cài Python 3.10+ từ https://www.python.org/downloads/
   Khi cài, bật "Add Python to PATH".
2. Giải nén ZIP vào một thư mục, ví dụ Downloads\ADD_STUDIO_VIDEO_GENERATOR_PRO.
3. Mở CMD tại thư mục đó.
4. Cài thư viện:
   py -m pip install pillow imageio-ffmpeg
5. Tạo video chữ/hiệu ứng:
   py add_video.py --title "ADD STUDIO" --subtitle "NEON WORLD" --text "Xin chào|ADD STUDIO|Video của bạn" --duration 15 --theme anime --transition glitch --output "video.mp4"
6. Tạo video từ ảnh:
   py add_video.py --images "C:\DuongDan\anh1.jpg" "C:\DuongDan\anh2.png" --title "ADD STUDIO" --text "Cảnh đầu|Cảnh tiếp theo|Kết thúc" --duration 15 --theme cyber --transition fade --output "video.mp4"
7. Ghép nhạc:
   py add_video.py --images "C:\DuongDan\anh1.jpg" --title "ADD STUDIO" --text "Welcome|Let's create" --music "C:\DuongDan\nhac.mp3" --volume 0.30 --duration 15 --theme pink --output "video.mp4"

LƯU Ý ĐƯỜNG DẪN:
- Thay C:\DuongDan\... bằng đường dẫn thật trên máy.
- Để dễ chạy, có thể chép ảnh và nhạc cùng thư mục với add_video.py, rồi dùng --images "anh1.jpg" --music "nhac.mp3".
- Nội dung sau --text phân cách bằng dấu |. Nên đặt giá trị có khoảng trắng trong dấu ngoặc kép.
- Dùng nhạc mà bạn có quyền sử dụng.

B. IPHONE / SAFARI
1. Tải ZIP, mở ứng dụng Files, chạm ZIP để giải nén.
2. Mở index.html bằng Safari. Nếu mở trực tiếp từ Files mà chức năng không hoạt động, tải index.html lên hosting tĩnh HTTPS (ví dụ GitHub Pages hoặc Netlify) rồi mở link trên Safari.
3. Chọn nhiều ảnh, sửa chữ, chọn mẫu, chọn chuyển cảnh và thời lượng.
4. Chọn nhạc tùy chọn rồi nhấn XEM TRƯỚC.
5. Nhấn DỰNG VIDEO TRÊN TRÌNH DUYỆT, chờ xong rồi nhấn TẢI VIDEO WEBM.

GIỚI HẠN IPHONE:
- Khả năng ghi video/âm thanh phụ thuộc phiên bản iOS và Safari; có thể chỉ xuất WEBM hoặc không ghi được nhạc. Nếu cần MP4 có âm thanh ổn định, hãy dùng bản Windows Python.
- Nếu file HTML mở trực tiếp không cho tải ảnh hoặc ghi video, dùng HTTPS hosting.
- Đây là công cụ dựng video mẫu từ ảnh và chữ; không tự trích xuất video gốc, không tự tạo hình anime mới và không bao gồm nhạc bản quyền.

C. TÙY CHỌN
--theme cyber|anime|matrix|pink|cinema
--transition fade|slide|zoom|glitch
--motion slow|medium|fast
--duration 15
--fps 24
--volume 0.35
--output "video.mp4"
