# utils.py
import re
import hashlib


PHONE_REGEX = re.compile(
    r'\b(?:0|\+84|84)?(?:3[2-9]|5[2689]|7[06-9]|8[1-9]|9[0-4689])\d{7}\b'
)

EMAIL_REGEX = re.compile(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
)

# CCCD VN thường bắt đầu bằng mã tỉnh (001–096), giảm false-positive
ID_CARD_REGEX = re.compile(
    r'\b(0[0-9]{2}|09[0-6])\d{9}\b'
)


def detect_pii(text: str):
    """
    Phát hiện PII và trả về loại PII
    """
    if PHONE_REGEX.search(text):
        return "phone"
    if EMAIL_REGEX.search(text):
        return "email"
    if ID_CARD_REGEX.search(text):
        return "id_card"
    return None


def contains_pii(text: str) -> bool:
    return detect_pii(text) is not None


def mask_pii(text: str) -> str:
    """
    Ẩn thông tin PII trước khi gửi cho AI
    """
    text = PHONE_REGEX.sub("[SĐT_ĐÃ_ẨN]", text)
    text = EMAIL_REGEX.sub("[EMAIL_ĐÃ_ẨN]", text)
    text = ID_CARD_REGEX.sub("[CCCD_ĐÃ_ẨN]", text)
    return text


def hash_pii(text: str) -> str:
    """
    Hash nội dung (dùng nếu cần lưu)
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
