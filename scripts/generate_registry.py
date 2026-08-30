import os, sys, hashlib
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')

source_root = os.environ.get('HDH_SOURCE_ROOT', '')
slides_dir = os.path.join(source_root, 'slides')
q_dir = os.path.join(source_root, 'questions')
dl_dir = source_root

def get_file_info(p):
    if not os.path.exists(p):
        return '', 0
    with open(p, 'rb') as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    pages = 0
    if p.lower().endswith('.pdf'):
        try:
            pages = len(PdfReader(p).pages)
        except Exception:
            pages = 0
    return sha, pages

sources = [
    # Tier A - Course Outlines & Slides
    {
        'id': 'UIT-OUTLINE-2024',
        'tier': 'A',
        'type': 'official_outline',
        'title': 'Đề cương chi tiết môn Hệ điều hành IT007 (Năm học 2024–2025)',
        'exact_filename': 'De cuong.pdf',
        'path': os.path.join(slides_dir, 'De cuong.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề cương chính thức quy định chuẩn đầu ra môn học và nội dung 9 chương học phần.'
    },
    {
        'id': 'UIT-SLIDE-CH01-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 1 - Chương 1: Tổng quan về Hệ điều hành',
        'exact_filename': 'Week01-Chapter1 2024.pdf',
        'path': os.path.join(slides_dir, 'Week01-Chapter1 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 1 (57 trang).'
    },
    {
        'id': 'UIT-SLIDE-CH02-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 2 - Chương 2: Cấu trúc Hệ điều hành',
        'exact_filename': 'Week02-Chapter2 2024.pdf',
        'path': os.path.join(slides_dir, 'Week02-Chapter2 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 2 (57 trang).'
    },
    {
        'id': 'UIT-SLIDE-CH03-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 3 - Chương 3: Quản lý Tiến trình',
        'exact_filename': 'Week03-Chapter3 2024.pdf',
        'path': os.path.join(slides_dir, 'Week03-Chapter3 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 3 (64 trang).'
    },
    {
        'id': 'UIT-SLIDE-CH04-1-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 4 - Chương 4 (Phần 1): Định thời CPU',
        'exact_filename': 'Week04-Chapter4-1 2024.pdf',
        'path': os.path.join(slides_dir, 'Week04-Chapter4-1 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 4 Phần 1 (56 trang).'
    },
    {
        'id': 'UIT-SLIDE-CH04-2-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 5 - Chương 4 (Phần 2): Định thời CPU',
        'exact_filename': 'Week05-Chapter4-2 2024.pdf',
        'path': os.path.join(slides_dir, 'Week05-Chapter4-2 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 4 Phần 2 (34 trang).'
    },
    {
        'id': 'UIT-SLIDE-CH04-3-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 6 - Chương 4 (Phần 3): Định thời Đa xử lý & Real-Time',
        'exact_filename': 'Week06-Chapter4-3 2024.pdf',
        'path': os.path.join(slides_dir, 'Week06-Chapter4-3 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 4 Phần 3 (46 trang).'
    },
    {
        'id': 'UIT-SLIDE-CH05-1-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 7 - Chương 5 (Phần 1): Đồng bộ Tiến trình',
        'exact_filename': 'Week07-Chapter5-1 2024.pdf',
        'path': os.path.join(slides_dir, 'Week07-Chapter5-1 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 5 Phần 1 (58 trang).'
    },
    {
        'id': 'UIT-SLIDE-MIDTERM-REVIEW-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Ôn tập Giữa kỳ IT007 Tuần 8',
        'exact_filename': 'Week08-Midterm Review.pdf',
        'path': os.path.join(slides_dir, 'Week08-Midterm Review.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide Ôn tập giữa kỳ chính thức (16 trang).'
    },
    {
        'id': 'UIT-SLIDE-CH05-2-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 9 - Chương 5 (Phần 2): Đồng bộ Tiến trình',
        'exact_filename': 'Week09-Chapter5-2 2024.pdf',
        'path': os.path.join(slides_dir, 'Week09-Chapter5-2 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 5 Phần 2 (55 trang).'
    },
    {
        'id': 'UIT-SLIDE-CH05-3-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 10 - Chương 5 (Phần 3): Bài toán đồng bộ kinh điển',
        'exact_filename': 'Week10-Chapter5-3 2024.pdf',
        'path': os.path.join(slides_dir, 'Week10-Chapter5-3 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 5 Phần 3 (32 trang).'
    },
    {
        'id': 'UIT-SLIDE-CH06-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 11 - Chương 6: Bế tắc (Deadlock)',
        'exact_filename': 'Week11-Chapter6 2024.pdf',
        'path': os.path.join(slides_dir, 'Week11-Chapter6 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 6 (67 trang).'
    },
    {
        'id': 'UIT-SLIDE-CH07-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 12 - Chương 7: Quản lý Bộ nhớ',
        'exact_filename': 'Week12-Chapter7 2024.pdf',
        'path': os.path.join(slides_dir, 'Week12-Chapter7 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 7 (72 trang).'
    },
    {
        'id': 'UIT-SLIDE-CH08-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 13 - Chương 8: Bộ nhớ ảo',
        'exact_filename': 'Week13-Chapter8 2024.pdf',
        'path': os.path.join(slides_dir, 'Week13-Chapter8 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 8 (50 trang).'
    },
    {
        'id': 'UIT-SLIDE-CH09-2024',
        'tier': 'A',
        'type': 'official_slide',
        'title': 'Slide Bài giảng Tuần 14 - Chương 9: Nghiên cứu Linux & Windows',
        'exact_filename': 'Week14-Chapter9 2024.pdf',
        'path': os.path.join(slides_dir, 'Week14-Chapter9 2024.pdf'),
        'year': '2024',
        'author': 'Khoa Kỹ thuật Máy tính - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Slide chính thức Chương 9 (57 trang).'
    },
    # Official Question Banks
    {
        'id': 'UIT-QBANK-CH01-2024',
        'tier': 'A',
        'type': 'official_qbank',
        'title': 'Bộ câu hỏi ôn tập Chương 1: Tổng quan HDH',
        'exact_filename': 'Cau hoi chuong 1 HDH.docx',
        'path': os.path.join(q_dir, 'Cau hoi chuong 1 HDH.docx'),
        'year': '2024',
        'author': 'ThS. Phan Đình Duy',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': '11 câu hỏi tự luận lý thuyết chính thức Chương 1.'
    },
    {
        'id': 'UIT-QBANK-CH02-2024',
        'tier': 'A',
        'type': 'official_qbank',
        'title': 'Bộ câu hỏi ôn tập Chương 2: Cấu trúc HDH',
        'exact_filename': 'Cau hoi chuong 2 HDH.docx',
        'path': os.path.join(q_dir, 'Cau hoi chuong 2 HDH.docx'),
        'year': '2024',
        'author': 'ThS. Phan Đình Duy',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': '10 câu hỏi tự luận chính thức Chương 2.'
    },
    {
        'id': 'UIT-QBANK-CH03-2024',
        'tier': 'A',
        'type': 'official_qbank',
        'title': 'Bộ bài tập ôn tập Chương 3: Quản lý Tiến trình',
        'exact_filename': 'Bai tap chuong 3 HDH.docx',
        'path': os.path.join(q_dir, 'Bai tap chuong 3 HDH.docx'),
        'year': '2024',
        'author': 'ThS. Phan Đình Duy',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': '159 đoạn câu hỏi tự luận và bài tập mẫu Chương 3.'
    },
    {
        'id': 'UIT-QBANK-CH04-2024',
        'tier': 'A',
        'type': 'official_qbank',
        'title': 'Bộ bài tập ôn tập Chương 4: Định thời CPU',
        'exact_filename': 'Bai tap chuong 4 HDH.docx',
        'path': os.path.join(q_dir, 'Bai tap chuong 4 HDH.docx'),
        'year': '2024',
        'author': 'Khoa KTMT - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': '258 đoạn bài tập định thời CPU.'
    },
    {
        'id': 'UIT-QBANK-CH05-2024',
        'tier': 'A',
        'type': 'official_qbank',
        'title': 'Bộ bài tập ôn tập Chương 5: Đồng bộ Tiến trình',
        'exact_filename': 'Bai tap chuong 5 HDH.docx',
        'path': os.path.join(q_dir, 'Bai tap chuong 5 HDH.docx'),
        'year': '2024',
        'author': 'Khoa KTMT - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': '128 đoạn bài tập đồng bộ hóa Semaphore & Mutex.'
    },
    {
        'id': 'UIT-QBANK-CH06-2024',
        'tier': 'A',
        'type': 'official_qbank',
        'title': 'Bộ bài tập ôn tập Chương 6: Deadlock',
        'exact_filename': 'Bai tap chuong 6 HDH.docx',
        'path': os.path.join(q_dir, 'Bai tap chuong 6 HDH.docx'),
        'year': '2024',
        'author': 'Khoa KTMT - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': '560 đoạn bài tập thuật toán Banker và Deadlock.'
    },
    {
        'id': 'UIT-QBANK-CH07-2024',
        'tier': 'A',
        'type': 'official_qbank',
        'title': 'Bộ bài tập ôn tập Chương 7: Quản lý Bộ nhớ',
        'exact_filename': 'Bai tap chuong 7 HDH.docx',
        'path': os.path.join(q_dir, 'Bai tap chuong 7 HDH.docx'),
        'year': '2024',
        'author': 'Khoa KTMT - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': '92 đoạn bài tập phân vùng, phân trang và TLB EAT.'
    },
    {
        'id': 'UIT-QBANK-CH08-2024',
        'tier': 'A',
        'type': 'official_qbank',
        'title': 'Bộ bài tập ôn tập Chương 8: Bộ nhớ ảo',
        'exact_filename': 'Bai tap chuong 8 HDH.docx',
        'path': os.path.join(q_dir, 'Bai tap chuong 8 HDH.docx'),
        'year': '2024',
        'author': 'Khoa KTMT - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': '329 đoạn bài tập thay thế trang FIFO, OPT, LRU.'
    },
    {
        'id': 'UIT-QBANK-CH09-2024',
        'tier': 'A',
        'type': 'official_qbank',
        'title': 'Bộ câu hỏi ôn tập Chương 9: Linux & Windows Case Studies',
        'exact_filename': 'Cau hoi chuong 9 HDH.docx',
        'path': os.path.join(q_dir, 'Cau hoi chuong 9 HDH.docx'),
        'year': '2024',
        'author': 'Khoa KTMT - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': '7 câu hỏi tự luận so sánh Linux và Windows.'
    },
    # Lab Manuals
    {
        'id': 'UIT-LAB01-MANUAL-2023',
        'tier': 'A',
        'type': 'official_lab',
        'title': 'Tài liệu hướng dẫn Thực hành Lab 1: Linux Cơ bản',
        'exact_filename': 'Lab 1 v2023.pdf',
        'path': os.path.join(dl_dir, 'Lab 1 v2023.pdf'),
        'year': '2023',
        'author': 'Khoa KTMT - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Hướng dẫn thực hành Lab 1 (55 trang).'
    },
    {
        'id': 'UIT-LAB02-MANUAL-2023',
        'tier': 'A',
        'type': 'official_lab',
        'title': 'Tài liệu hướng dẫn Thực hành Lab 2: Shell Script',
        'exact_filename': 'Lab 2 v2023.pdf',
        'path': os.path.join(dl_dir, 'Lab 2 v2023.pdf'),
        'year': '2023',
        'author': 'Khoa KTMT - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Hướng dẫn thực hành Lab 2 (63 trang).'
    },
    {
        'id': 'UIT-LAB03-MANUAL-2023',
        'tier': 'A',
        'type': 'official_lab',
        'title': 'Tài liệu hướng dẫn Thực hành Lab 3: Quản lý Tiến trình',
        'exact_filename': 'Lab 3 v2023.pdf',
        'path': os.path.join(dl_dir, 'Lab 3 v2023.pdf'),
        'year': '2023',
        'author': 'Khoa KTMT - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Hướng dẫn thực hành Lab 3 (50 trang).'
    },
    {
        'id': 'UIT-LAB04-MANUAL-2023',
        'tier': 'A',
        'type': 'official_lab',
        'title': 'Tài liệu hướng dẫn Thực hành Lab 4: Đa luồng & IPC',
        'exact_filename': 'Lab 4 v2023.pdf',
        'path': os.path.join(dl_dir, 'Lab 4 v2023.pdf'),
        'year': '2023',
        'author': 'Khoa KTMT - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Hướng dẫn thực hành Lab 4 (21 trang).'
    },
    {
        'id': 'UIT-LAB05-MANUAL-2023',
        'tier': 'A',
        'type': 'official_lab',
        'title': 'Tài liệu hướng dẫn Thực hành Lab 5: Đồng bộ hóa',
        'exact_filename': 'Lab 5 v2023.pdf',
        'path': os.path.join(dl_dir, 'Lab 5 v2023.pdf'),
        'year': '2023',
        'author': 'Khoa KTMT - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Hướng dẫn thực hành Lab 5 (28 trang).'
    },
    {
        'id': 'UIT-LAB06-P19-1-2023',
        'tier': 'A',
        'type': 'official_lab',
        'title': 'Tài liệu hướng dẫn Thực hành Lab 6: Xây dựng Shell it007sh',
        'exact_filename': 'Lab 6 v2023.pdf',
        'path': os.path.join(dl_dir, 'Lab 6 v2023.pdf'),
        'year': '2023',
        'author': 'Khoa KTMT - UIT',
        'public_url': 'https://courses.uit.edu.vn',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đặc tả kỹ thuật chính thức xây dựng shell it007sh (8 trang).'
    },
    # Tier B - Technical Specifications
    {
        'id': 'SILBERSCHATZ-OSC10',
        'tier': 'B',
        'type': 'textbook',
        'title': 'Operating System Concepts (10th Edition)',
        'exact_filename': 'Silberschatz-OSC-10th.pdf',
        'path': '',
        'year': '2018',
        'author': 'Abraham Silberschatz, Peter B. Galvin, Greg Gagne',
        'public_url': 'https://www.os-book.com/OS10/',
        'status': 'VERIFIED_STANDARD',
        'notes': 'Giáo trình chuẩn quốc tế môn Hệ điều hành.'
    },
    {
        'id': 'POSIX-SPEC-2017',
        'tier': 'B',
        'type': 'technical_standard',
        'title': 'IEEE Std 1003.1-2017 / POSIX.1-2017 Standard',
        'exact_filename': 'posix-2017-standard.html',
        'path': '',
        'year': '2017',
        'author': 'The Open Group / IEEE',
        'public_url': 'https://pubs.opengroup.org/onlinepubs/9699919799/',
        'status': 'VERIFIED_STANDARD',
        'notes': 'Chuẩn đặc tả quốc tế về giao diện lập trình hệ thống POSIX C.'
    },
    {
        'id': 'POSIX-FORK',
        'tier': 'B',
        'type': 'man_page',
        'title': 'fork(2) - Linux manual page',
        'exact_filename': 'fork.2.html',
        'path': '',
        'year': '2023',
        'author': 'Michael Kerrisk et al.',
        'public_url': 'https://man7.org/linux/man-pages/man2/fork.2.html',
        'status': 'VERIFIED_STANDARD',
        'notes': 'Đặc tả hàm nhân bản tiến trình fork().'
    },
    {
        'id': 'POSIX-EXEC',
        'tier': 'B',
        'type': 'man_page',
        'title': 'exec(3) - Linux manual page',
        'exact_filename': 'exec.3.html',
        'path': '',
        'year': '2023',
        'author': 'Michael Kerrisk et al.',
        'public_url': 'https://man7.org/linux/man-pages/man3/exec.3.html',
        'status': 'VERIFIED_STANDARD',
        'notes': 'Đặc tả họ hàm nạp chương trình execvp/execlp.'
    },
    {
        'id': 'POSIX-WAITPID',
        'tier': 'B',
        'type': 'man_page',
        'title': 'waitpid(2) - Linux manual page',
        'exact_filename': 'waitpid.2.html',
        'path': '',
        'year': '2023',
        'author': 'Michael Kerrisk et al.',
        'public_url': 'https://man7.org/linux/man-pages/man2/waitpid.2.html',
        'status': 'VERIFIED_STANDARD',
        'notes': 'Đặc tả hàm đồng bộ chờ tiến trình con waitpid().'
    },
    {
        'id': 'POSIX-PIPE',
        'tier': 'B',
        'type': 'man_page',
        'title': 'pipe(2) - Linux manual page',
        'exact_filename': 'pipe.2.html',
        'path': '',
        'year': '2023',
        'author': 'Michael Kerrisk et al.',
        'public_url': 'https://man7.org/linux/man-pages/man2/pipe.2.html',
        'status': 'VERIFIED_STANDARD',
        'notes': 'Đặc tả hàm tạo đường ống truyền thông pipe().'
    },
    {
        'id': 'POSIX-DUP2',
        'tier': 'B',
        'type': 'man_page',
        'title': 'dup2(2) - Linux manual page',
        'exact_filename': 'dup2.2.html',
        'path': '',
        'year': '2023',
        'author': 'Michael Kerrisk et al.',
        'public_url': 'https://man7.org/linux/man-pages/man2/dup2.2.html',
        'status': 'VERIFIED_STANDARD',
        'notes': 'Đặc tả hàm nhân bản file descriptor dup2().'
    },
    {
        'id': 'POSIX-SIGACTION',
        'tier': 'B',
        'type': 'man_page',
        'title': 'sigaction(2) - Linux manual page',
        'exact_filename': 'sigaction.2.html',
        'path': '',
        'year': '2023',
        'author': 'Michael Kerrisk et al.',
        'public_url': 'https://man7.org/linux/man-pages/man2/sigaction.2.html',
        'status': 'VERIFIED_STANDARD',
        'notes': 'Đặc tả hàm bắt và xử lý tín hiệu Signal sigaction().'
    },
    {
        'id': 'POSIX-PTHREAD',
        'tier': 'B',
        'type': 'man_page',
        'title': 'pthread_create(3) - Linux manual page',
        'exact_filename': 'pthread_create.3.html',
        'path': '',
        'year': '2023',
        'author': 'Michael Kerrisk et al.',
        'public_url': 'https://man7.org/linux/man-pages/man3/pthread_create.3.html',
        'status': 'VERIFIED_STANDARD',
        'notes': 'Đặc tả hàm tạo luồng POSIX Threads.'
    },
    {
        'id': 'POSIX-SEMAPHORE',
        'tier': 'B',
        'type': 'man_page',
        'title': 'sem_init(3) - Linux manual page',
        'exact_filename': 'sem_init.3.html',
        'path': '',
        'year': '2023',
        'author': 'Michael Kerrisk et al.',
        'public_url': 'https://man7.org/linux/man-pages/man3/sem_init.3.html',
        'status': 'VERIFIED_STANDARD',
        'notes': 'Đặc tả họ hàm đồng bộ Semaphore không tên sem_init/wait/post.'
    },
    {
        'id': 'LINUX-MAN-PAGES',
        'tier': 'B',
        'type': 'manual_project',
        'title': 'The Linux man-pages project',
        'exact_filename': 'man7-index.html',
        'path': '',
        'year': '2024',
        'author': 'Michael Kerrisk et al.',
        'public_url': 'https://man7.org/linux/man-pages/',
        'status': 'VERIFIED_STANDARD',
        'notes': 'Tập hợp toàn bộ hướng dẫn tra cứu hàm hệ thống Linux.'
    },
    {
        'id': 'WINDOWS-INTERNALS-7TH',
        'tier': 'B',
        'type': 'textbook',
        'title': 'Windows Internals (7th Edition, Part 1 & Part 2)',
        'exact_filename': 'Windows-Internals-7th.pdf',
        'path': '',
        'year': '2021',
        'author': 'Pavel Yosifovich, Mark E. Russinovich, David A. Solomon, Alex Ionescu',
        'public_url': 'https://learn.microsoft.com/en-us/sysinternals/resources/windows-internals',
        'status': 'VERIFIED_STANDARD',
        'notes': 'Tài liệu chuẩn mực về kiến trúc bên trong nhân Windows.'
    },
    # Tier C - Real Exams (BHT CNPM UIT)
    {
        'id': 'BHT-EXAM-GK-2018-2019-HK1',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Giữa kỳ IT007 HK1 2018–2019 kèm đáp án',
        'exact_filename': '[BHT CNPM] HDH 2018-2019 GK1 (có đáp án).pdf',
        'path': os.path.join(dl_dir, '[BHT CNPM] HDH 2018-2019 GK1 (có đáp án).pdf'),
        'year': '2018-2019',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi tự luận 6 trang: User vs Kernel mode, fork tree, FCFS/SJF/RR.'
    },
    {
        'id': 'BHT-EXAM-GK-2020-2021-HK1',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Giữa kỳ IT007 HK1 2020–2021',
        'exact_filename': '[BHT CNPM] HDH 2020-2021 GK1.pdf',
        'path': os.path.join(dl_dir, '[BHT CNPM] HDH 2020-2021 GK1.pdf'),
        'year': '2020-2021',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 5 trang: 15 câu trắc nghiệm + Tự luận fork + SRTF/RR.'
    },
    {
        'id': 'BHT-EXAM-GK-2020-2021-HK2',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Giữa kỳ IT007 HK2 2020–2021',
        'exact_filename': '[BHT CNPM] HDH 2020-2021 GK2.pdf',
        'path': os.path.join(dl_dir, '[BHT CNPM] HDH 2020-2021 GK2.pdf'),
        'year': '2020-2021',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 3 trang: Trắc nghiệm cấu trúc lưu trữ và định thời.'
    },
    {
        'id': 'BHT-EXAM-GK-2022-2023-HK1',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Giữa kỳ IT007 HK1 2022–2023',
        'exact_filename': '[BHT CNPM] HDH 2022-2023 GK1.pdf',
        'path': os.path.join(dl_dir, '[BHT CNPM] HDH 2022-2023 GK1.pdf'),
        'year': '2022-2023',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 4 trang: 15 câu trắc nghiệm + Tự luận vòng lặp fork + Priority/RR.'
    },
    {
        'id': 'BHT-EXAM-GK-2022-2023-HK2',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Giữa kỳ IT007 HK2 2022–2023',
        'exact_filename': '[BHT CNPM] HDH 2022-2023 GK2.pdf',
        'path': os.path.join(dl_dir, '[BHT CNPM] HDH 2022-2023 GK2.pdf'),
        'year': '2022-2023',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 4 trang: 16 câu trắc nghiệm + Tự luận định thời.'
    },
    {
        'id': 'BHT-EXAM-GK-2023-2024-HK1',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Giữa kỳ IT007 HK1 2023–2024 có đáp án',
        'exact_filename': '[BHT CNPM] HDH 2023-2024 GK1 (Có đáp án).pdf',
        'path': os.path.join(dl_dir, '[BHT CNPM] HDH 2023-2024 GK1 (Có đáp án).pdf'),
        'year': '2023-2024',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 4 trang có đáp án: Lần vết fork + SRTF/RR.'
    },
    {
        'id': 'BHT-EXAM-GK-2023-2024-HK2',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Giữa kỳ IT007 HK2 2023–2024',
        'exact_filename': '[BHT CNPM] HDH 2023-2024 GK2.pdf',
        'path': os.path.join(dl_dir, '[BHT CNPM] HDH 2023-2024 GK2.pdf'),
        'year': '2023-2024',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 4 trang: 12 câu trắc nghiệm + Đúng/Sai + Điền từ tiếng Anh + Định thời.'
    },
    {
        'id': 'BHT-EXAM-GK-2024-2025-HK1',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Giữa kỳ IT007 HK1 2024–2025',
        'exact_filename': '[BHT CNPM] HDH 2024-2025 GK1.pdf',
        'path': os.path.join(dl_dir, '[BHT CNPM] HDH 2024-2025 GK1.pdf'),
        'year': '2024-2025',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 8 trang mới nhất: Điền từ tiếng Anh + Bài tập fork + SRTF.'
    },
    {
        'id': 'BHT-EXAM-CK-2017-2018-HK2',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Cuối kỳ IT007 HK2 2017–2018',
        'exact_filename': '[BHTCNPM] HDH 2017-2018 CK2.pdf',
        'path': os.path.join(dl_dir, '[BHTCNPM] HDH 2017-2018 CK2.pdf'),
        'year': '2017-2018',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 4 trang: 15 câu trắc nghiệm + Tự luận Banker 6 tiến trình + Phân trang.'
    },
    {
        'id': 'BHT-EXAM-CK-2018-2019-HK2',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Cuối kỳ IT007 HK2 2018–2019',
        'exact_filename': '[BHTCNPM] HDH 2018-2019 CK2.pdf',
        'path': os.path.join(dl_dir, '[BHTCNPM] HDH 2018-2019 CK2.pdf'),
        'year': '2018-2019',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 7 trang: 20 câu trắc nghiệm + Đồng bộ luồng + Banker + LRU 4 frames.'
    },
    {
        'id': 'BHT-EXAM-CK-2019-2020-HK1-DE1',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Cuối kỳ IT007 HK1 2019–2020 Đề 1',
        'exact_filename': '[BHTCNPM] HDH 2019-2020 CK1 De1.pdf',
        'path': os.path.join(dl_dir, '[BHTCNPM] HDH 2019-2020 CK1 De1.pdf'),
        'year': '2019-2020',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 5 trang: 20 câu trắc nghiệm + Tự luận bộ nhớ.'
    },
    {
        'id': 'BHT-EXAM-CK-2019-2020-HK1-DE2',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Cuối kỳ IT007 HK1 2019–2020 Đề 2',
        'exact_filename': '[BHTCNPM] HDH 2019-2020 CK1 De2.pdf',
        'path': os.path.join(dl_dir, '[BHTCNPM] HDH 2019-2020 CK1 De2.pdf'),
        'year': '2019-2020',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 5 trang: 20 câu trắc nghiệm + Tự luận bảng trang 3 cấp.'
    },
    {
        'id': 'BHT-EXAM-CK-2019-2020-HK1-DE3',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Cuối kỳ IT007 HK1 2019–2020 Đề 3',
        'exact_filename': '[BHTCNPM] HDH 2019-2020 CK1 De3.pdf',
        'path': os.path.join(dl_dir, '[BHTCNPM] HDH 2019-2020 CK1 De3.pdf'),
        'year': '2019-2020',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 5 trang: 20 câu trắc nghiệm + Tự luận địa chỉ ảo 32-bit.'
    },
    {
        'id': 'BHT-EXAM-CK-2020-2021-HK1',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Cuối kỳ IT007 HK1 2020–2021 có đáp án',
        'exact_filename': '[BHTCNPM] HDH 2020-2021 CK1 (đáp án).pdf',
        'path': os.path.join(dl_dir, '[BHTCNPM] HDH 2020-2021 CK1 (đáp án).pdf'),
        'year': '2020-2021',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 4 trang tự luận có đáp án: Đồng bộ xe qua cầu + Banker + First/Best/Worst fit.'
    },
    {
        'id': 'BHT-EXAM-CK-2022-2023-HK1',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Cuối kỳ IT007 HK1 2022–2023',
        'exact_filename': '[BHTCNPM] HDH 2022-2023 CK1.pdf',
        'path': os.path.join(dl_dir, '[BHTCNPM] HDH 2022-2023 CK1.pdf'),
        'year': '2022-2023',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 6 trang: 25 câu trắc nghiệm + Tự luận phân mảnh trong phân trang.'
    },
    {
        'id': 'BHT-EXAM-CK-2022-2023-HK2',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Cuối kỳ IT007 HK2 2022–2023',
        'exact_filename': '[BHTCNPM] HDH 2022-2023 CK2.pdf',
        'path': os.path.join(dl_dir, '[BHTCNPM] HDH 2022-2023 CK2.pdf'),
        'year': '2022-2023',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 5 trang: Trắc nghiệm + Tự luận đồng bộ & Banker.'
    },
    {
        'id': 'BHT-EXAM-CK-2023-2024-HK1',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Cuối kỳ IT007 HK1 2023–2024',
        'exact_filename': '[BHTCNPM] HDH 2023-2024 CK1.pdf',
        'path': os.path.join(dl_dir, '[BHTCNPM] HDH 2023-2024 CK1.pdf'),
        'year': '2023-2024',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 6 trang: 25 câu trắc nghiệm + Tự luận phân mảnh.'
    },
    {
        'id': 'BHT-EXAM-CK-2023-2024-HK2',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Cuối kỳ IT007 HK2 2023–2024',
        'exact_filename': '[BHTCNPM] HDH 2023-2024 CK2.pdf',
        'path': os.path.join(dl_dir, '[BHTCNPM] HDH 2023-2024 CK2.pdf'),
        'year': '2023-2024',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 6 trang: 15 câu trắc nghiệm + Đúng/Sai + Điền từ tiếng Anh + So sánh Dynamic linking/loading.'
    },
    {
        'id': 'BHT-EXAM-CK-2024-2025-HK1',
        'tier': 'C',
        'type': 'verified_exam',
        'title': 'Đề thi Cuối kỳ IT007 HK1 2024–2025',
        'exact_filename': '[BHTCNPM] HDH 2024-2025 CK1.pdf',
        'path': os.path.join(dl_dir, '[BHTCNPM] HDH 2024-2025 CK1.pdf'),
        'year': '2024-2025',
        'author': 'Ban Hỗ Trợ Học Tập CNPM UIT',
        'public_url': 'https://www.facebook.com/bht.cnpm.uit',
        'status': 'VERIFIED_LOCAL',
        'notes': 'Đề thi 5 trang mới nhất: 20 câu trắc nghiệm + Đúng/Sai + Điền từ tiếng Anh (Mutual Exclusion, Safe Sequence).'
    }
]

out_lines = [
    '# ==========================================================================',
    '# SỔ ĐĂNG KÝ NGUỒN TÀI LIỆU BẤT BIẾN TOÀN CỤC (GLOBAL SOURCE REGISTRY)',
    '# IT007 — CẨM NANG HỆ ĐIỀU HÀNH UIT',
    '# Single Source of Truth for all Source Citations & Locators',
    '# ==========================================================================\n',
    'sources:'
]

for s in sources:
    sha, pages = get_file_info(s['path']) if s['path'] else ('', 0)
    out_lines.append(f"  - id: \"{s['id']}\"")
    out_lines.append(f"    tier: \"{s['tier']}\"")
    out_lines.append(f"    type: \"{s['type']}\"")
    out_lines.append(f"    title: \"{s['title']}\"")
    out_lines.append(f"    exact_filename: \"{s['exact_filename']}\"")
    if sha:
        out_lines.append(f"    sha256: \"{sha}\"")
    if pages > 0:
        out_lines.append(f"    page_count: {pages}")
    out_lines.append(f"    year: \"{s['year']}\"")
    out_lines.append(f"    author: \"{s['author']}\"")
    out_lines.append(f"    public_url: \"{s['public_url']}\"")
    out_lines.append(f"    status: \"{s['status']}\"")
    out_lines.append(f"    notes: \"{s['notes']}\"")
    out_lines.append("")

reg_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'content', 'sources', 'registry.yaml'))
os.makedirs(os.path.dirname(reg_path), exist_ok=True)
with open(reg_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print(f"Generated registry with {len(sources)} unique immutable source IDs.")
