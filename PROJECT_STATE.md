# PROJECT STATE — HDH_UIT

## Project
**HDH_UIT — UIT IT007 Operating Systems Handbook**

## Current Phase
`PUBLISHED_TO_MAIN_READY_FOR_OPTIONAL_CODEX_FINAL_AUDIT`

## Completed
- [x] Khảo sát và đối chiếu các bản nguồn Antigravity/Codex liên quan.
- [x] Xác định canonical source tại `src/chapters/`, `src/styles/`, `src/vendor/mathjax/`.
- [x] Hoàn thiện cấu trúc repository công khai: `src/`, `dist/`, `docs/`, `scripts/`, `reports/`, `.github/`.
- [x] Tích hợp 12 chương, CSS chế bản, MathJax 3.2.2 offline và bộ build/validation.
- [x] Hoàn tất các precision fix đã ghi nhận: Priority convention, Memory Barrier, Swapping, Mode vs Context switch, printf/I/O convention.
- [x] Xuất bản deliverables cuối:
  - `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.html`
  - `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.pdf` — 56 trang A4.
- [x] README, preview assets, build docs, methodology, changelog, notice và QA reports đã có trên repository.
- [x] Nhánh `release/it007-handbook-v1` đã được hợp nhất lịch sử an toàn với `main` bằng merge commit giữ nguyên canonical release tree.
- [x] `main` đã được publish thành công lên GitHub.
- [x] `release/it007-handbook-v1` đã được đồng bộ cùng commit với `main` tại thời điểm publish.
- [x] GitHub Actions `Validate Handbook Repository` trên `main` đã chạy thành công sau lần publish.

## Canonical Source
- `src/chapters/`
- `src/styles/`
- `src/vendor/mathjax/`
- `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.html`
- `dist/IT007_CamNang_HeDieuHanh_UIT_VoTrongPhuc_FINAL.pdf`

## Git Remote
`https://github.com/Phuchello/HDH_UIT`

## Published Main Merge Commit
`772e674cf3541d45b34f7b21441ec000b1381908`

## Validation
- PRE-CODEX audit: PASS — 99.5/100
- Existing FINAL publication QA: PASS — 96/100
- GitHub Actions validation on published main: PASS
- Unresolved CRITICAL: 0
- Unresolved MAJOR: 0

## Last Safe Checkpoint
Canonical IT007 handbook repository has been published to `main`; GitHub Actions validation passed.

## Exact Next Action
Optional: run one final Codex repository audit, then create the Git tag / GitHub Release `v1.0.0` if desired. The current connected GitHub tool does not expose tag/release creation, so no tag has been fabricated.

## Git Status
- Default branch: `main`
- Release branch: `release/it007-handbook-v1`
- Public repository published and validated.
