---
id: "lab01-linux-basics"
title: "Lab 1: Giới thiệu Linux, Quản trị Tệp tin & Lệnh Cơ Bản"
book: "lab"
lab_number: 1
order: 1
slug: "lab01-linux-basics"
summary: "Làm quen với môi trường Linux Ubuntu, cấu trúc cây thư mục FHS, hệ thống phân quyền tệp tin (chmod/chown), quản lý tiến trình cơ bản (ps/top/kill) và các thao tác dòng lệnh thiết yếu."
prerequisites:
  - "00-environment"
related:
  - "lab02-shell-scripting"
  - "lab03-process-management"
sources:
  - "SRC-A11 (Lab 1 v2023.pdf)"
  - "SRC-B03 (Linux Man-Pages)"
last_updated: "2026-08-30"
---

# Lab 1: Giới thiệu Linux & Quản trị Hệ Thống Tệp

## 1. Mục Tiêu Học Thuật & Chuẩn Đầu Ra
- Nắm vững kiến trúc cây thư mục chuẩn Filesystem Hierarchy Standard (FHS) của Linux.
- Sử dụng thành thạo các lệnh điều hướng, thao tác tệp tin và tìm kiếm (`cd`, `ls`, `mkdir`, `cp`, `mv`, `rm`, `find`, `grep`).
- Hiểu rõ cơ chế phân quyền người dùng (User/Group/Other) và thay đổi thuộc tính tệp tin bằng `chmod`, `chown`.
- Thực hiện giám sát và điều khiển tiến trình cơ bản qua Terminal (`ps`, `top`, `kill`).

---

## 2. Phân Định Yêu Cầu Chính Thức vs Khuyến Nghị Cẩm Nang

> [!IMPORTANT]
> **YÊU CẦU CHÍNH THỨC CỦA BỘ MÔN (OFFICIAL UIT REQUIREMENTS):**
> 1. Thực hiện đầy đủ các bài tập điều hướng và thao tác tệp theo hướng dẫn trong `Lab 1 v2023.pdf`.
> 2. Thiết lập đúng quyền truy xuất cho tệp tin theo mã bát phân (Octal notation) hoặc ký hiệu (Symbolic notation).
> 3. Nộp báo cáo thực hành (PDF) chứa ảnh chụp màn hình terminal có kèm dấu nhắc lệnh hiển thị Họ tên và MSSV.

> [!TIP]
> **KHUYẾN NGHỊ CỦA CẨM NANG (HANDBOOK BEST PRACTICES):**
> - Sử dụng phím `Tab` để tự động hoàn thành đường dẫn (Tab-completion), hạn chế tối đa việc gõ nhầm.
> - Luôn kiểm tra kết quả thao tác bằng `ls -la` hoặc `echo $?` để xác nhận lệnh đã thực thi thành công.
> - Tuyệt đối không dùng lệnh `sudo rm -rf /` hoặc xóa nhầm thư mục gốc `/etc`, `/bin`.

---

## 3. Hệ Thống Cây Thư Mục Linux (Filesystem Hierarchy Standard)

Khác với Windows sử dụng các ổ đĩa riêng biệt (`C:\`, `D:\`), hệ thống Linux tổ chức toàn bộ dữ liệu dưới dạng **một cây phân cấp duy nhất** bắt đầu từ thư mục gốc `/` (Root directory):

```
/ (Root)
├── bin/      -> Chứa các tệp thực thi nhị phân cơ bản (ls, cp, rm, bash)
├── sbin/     -> Chứa các lệnh quản trị hệ thống dành cho Superuser (reboot, fdisk)
├── etc/      -> Chứa toàn bộ tệp cấu hình hệ thống (passwd, fstab, network)
├── home/     -> Thư mục người dùng cá nhân (/home/sinhvien/)
├── root/     -> Thư mục cá nhân của quản trị viên root
├── var/      -> Dữ liệu biến đổi trong quá trình chạy (log files, mail spool)
├── tmp/      -> Thư mục chứa tệp tạm thời (tự động dọn dẹp khi khởi động lại)
├── dev/      -> Các tệp đại diện cho thiết bị phần cứng (dev/sda, dev/null, dev/zero)
└── proc/     -> Hệ thống tệp ảo ánh xạ trực tiếp trạng thái nhân Linux (proc/cpuinfo)
```

---

## 4. Cơ Chế Phân Quyền Tệp Tin (File Permissions)

Khi gõ lệnh `ls -l`, mỗi dòng xuất ra sẽ có định dạng:

```
-rwxr-xr-- 1 lyle3 students 4096 Aug 30 20:00 script.sh
^ ^^^ ^^^ ^^^
|  |   |   |
|  |   |   +--> Quyền của Người khác (Others): r-- (chỉ đọc)
|  |   +------> Quyền của Nhóm (Group): r-x (đọc + thực thi)
|  +----------> Quyền của Chủ sở hữu (User/Owner): rwx (đọc + ghi + thực thi)
+-------------> Loại tệp (-: file thông thường, d: directory, l: symlink)
```

### Bảng Giá Trị Quyền Bát Phân (Octal Values)
| Quyền | Ký hiệu | Giá trị nhị phân | Giá trị bát phân | Ý nghĩa đối với File | Ý nghĩa đối với Directory |
| :---: | :---: | :---: | :---: | :--- | :--- |
| **Read** | `r` | `100` | **4** | Đọc nội dung file | Liệt kê danh sách file bên trong (`ls`) |
| **Write** | `w` | `010` | **2** | Sửa đổi/ghi nội dung file | Tạo mới, đổi tên hoặc xóa file bên trong |
| **Execute** | `x` | `001` | **1** | Chạy file như chương trình | Truy cập / đi vào thư mục (`cd`) |

### Ví dụ Thực Hành Phân Quyền
```bash
# Gán quyền: Owner=rwx (7), Group=rx (5), Others=r (4)
chmod 754 script.sh

# Gán quyền thực thi thêm cho User:
chmod u+x script.sh

# Đổi chủ sở hữu file sang user 'sinhvien':
sudo chown sinhvien script.sh
```

---

## 5. Các Câu Hỏi Vấn Đáp Thực Hành Chuẩn Bị (Viva Questions)

> [!STUDYCARD] id="viva-lab01-hardlink-symlink"
> **Câu hỏi Vấn đáp:** Phân biệt Hard Link và Symbolic Link (Soft Link) trong Linux. Điều gì xảy ra khi ta xóa file gốc?
> <!-- hint -->
> Gợi ý: Hãy nghĩ về số hiệu Inode và bảng quản lý tệp trên đĩa.
> <!-- keypoints -->
> - [ ] Hard link trỏ trực tiếp đến cùng một chỉ số Inode trên đĩa; xóa file gốc thì file hard link vẫn đọc được bình thường.
> - [ ] Soft link (Symlink) là file riêng chứa chuỗi đường dẫn trỏ tới file gốc; xóa file gốc thì soft link bị hỏng (Broken link).
> - [ ] Hard link không thể liên kết xuyên qua các phân vùng đĩa khác nhau (Cross-filesystem) và không thể liên kết thư mục.
> <!-- answer -->
> Hard Link tạo ra một tên gọi mới trỏ cùng vào một Inode và dữ liệu vật lý trên đĩa. Dung lượng và số inode của hard link hoàn toàn trùng với file gốc. Khi xóa file gốc, chỉ số đếm liên kết giảm đi 1, dữ liệu chỉ thực sự bị giải phóng khi mọi hard link bị xóa hết. Soft Link là một tệp con trỏ chứa đường dẫn của tệp gốc. Nếu tệp gốc bị xóa hoặc đổi tên, Soft Link sẽ trở thành liên kết chết (Dangling/Broken Link).

---

## 6. Bài Tập Thực Hành Lab 1

### Bài 1: Quản trị cấu trúc thư mục
Tạo cấu trúc thư mục dự án sau chỉ bằng một lệnh duy nhất:
```
project/
├── src/
│   ├── core/
│   └── utils/
├── include/
└── build/
```

**Lệnh giải quyết:**
```bash
mkdir -p project/src/{core,utils} project/include project/build
```

### Bài 2: Tìm kiếm tệp tin & Lọc chuỗi
Tìm tất cả các tệp có đuôi `.c` trong thư mục hiện tại có dung lượng lớn hơn `10KB` và chứa chuỗi từ khóa `fork`:
```bash
find . -type f -name "*.c" -size +10k -exec grep -H "fork" {} +
```
