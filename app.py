import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
from typing import List, Dict, Set

CAC_COT = ['ma_kh', 'ho_ten', 'sdt', 'email', 'cccd', 'dia_phuong', 'loai_kh', 'so_du', 'ngay_dang_ky']

# ============================================================
# 2. CLASS
# ============================================================
class KhachHang:
    def __init__(self, ma_kh, ho_ten, sdt, email, cccd, dia_phuong, loai_kh, so_du, ngay_dang_ky):
        self.ma_kh = ma_kh
        self.ho_ten = ho_ten
        self.sdt = sdt
        self.email = email
        self.cccd = cccd
        self.dia_phuong = dia_phuong
        self.loai_kh = loai_kh
        self.so_du = float(so_du)
        self.ngay_dang_ky = ngay_dang_ky

class HeThong:
    def __init__(self):
        self.danh_sach_kh: List[KhachHang] = []
        self.tu_dien_kh: Dict[str, KhachHang] = {}
        self.tap_hop_cccd: Set[str] = set()
        self.tap_hop_email: Set[str] = set()
        self.tap_hop_sdt: Set[str] = set()

    def them_khach_hang(self, kh: KhachHang):
        if kh.cccd in self.tap_hop_cccd or kh.email in self.tap_hop_email or kh.sdt in self.tap_hop_sdt:
            return False
        self.danh_sach_kh.append(kh)
        self.tu_dien_kh[kh.ma_kh] = kh
        self.tap_hop_cccd.add(kh.cccd)
        self.tap_hop_email.add(kh.email)
        self.tap_hop_sdt.add(kh.sdt)
        return True

def khoi_tao_du_lieu_mau(he_thong):
    ds_mau = [
        KhachHang("KH001", "Nguyen Van An",    "0901234567", "an.nguyen@gmail.com",  "001099000001", "Ha Noi",     "VIP",         150000000.0, "2023-01-15"),
        KhachHang("KH002", "Tran Thi Binh",    "0912345678", "binh.tran@gmail.com",  "001099000002", "TP.HCM",     "Standard",    2500000.0,   "2026-05-20"),
        KhachHang("KH003", "Le Minh Cuong",    "0923456789", "cuong.le@gmail.com",   "001099000003", "Da Nang",    "Doanh nghiep", 500000000.0, "2026-11-10"),
        KhachHang("KH004", "Pham Minh Duc",    "0934567890", "duc.pham@gmail.com",   "001099000004", "Ha Noi",     "Standard",    12000000.0,  "2024-02-01"),
        KhachHang("KH005", "Vu Thi Kha En",    "0945678901", "en.vu@gmail.com",      "001099000005", "Can Tho",    "VIP",         85000000.0,  "2025-08-12"),
        KhachHang("KH006", "Dang Quoc Kha",    "0956789012", "khanh.dang@gmail.com", "001099000006", "TP.HCM",     "Standard",    5500000.0,   "2024-01-10"),
        KhachHang("KH007", "Nguyen Thi Mai",   "0967890123", "mai.bui@gmail.com",    "001099000007", "Hai Phong",  "Standard",    45000000.0,  "2026-03-30"),
        KhachHang("KH008", "Do Nam Phong",     "0978901234", "phong.do@gmail.com",   "001099000008", "Da Nang",    "VIP",         230000000.0, "2022-09-05"),
        KhachHang("KH009", "Ho Quang Vinh",    "0989012345", "vinh.ho@gmail.com",    "001099000009", "TP.HCM",     "Doanh nghiep", 990000000.0, "2021-12-01"),
        KhachHang("KH010", "Nong Van Giang",   "0990123456", "giang.nong@gmail.com", "001099000010", "Can Tho",    "Standard",    1500000.0,   "2025-03-15"),
        KhachHang("KH011", "Trinh Thao Nhi",   "0909998877", "nhi.trinh@gmail.com",  "001099000011", "Ha Noi",     "VIP",         120000000.0, "2023-10-05"),
        KhachHang("KH012", "Luong Hai Yen",    "0918887766", "yen.luong@gmail.com",  "001099000012", "Hai Phong",  "Standard",    8000000.0,   "2024-02-18"),
        KhachHang("KH013", "Cao Van Tuan",     "0927776655", "tuan.cao@gmail.com",   "001099000013", "Da Nang",    "Standard",    3000000.0,   "2025-07-22"),
        KhachHang("KH014", "Duong Kim Anh",    "0936665544", "anh.duong@gmail.com",  "001099000014", "TP.HCM",     "Doanh nghiep", 450000000.0, "2022-04-11"),
        KhachHang("KH015", "Phan Van Long",    "0945554433", "long.phan@gmail.com",  "001099000015", "Ha Noi",     "Standard",    18000000.0,  "2023-12-01")
    ]
    for kh in ds_mau:
        he_thong.them_khach_hang(kh)

if 'ngan_hang' not in st.session_state:
    st.session_state.ngan_hang = HeThong()
    khoi_tao_du_lieu_mau(st.session_state.ngan_hang)

ht = st.session_state.ngan_hang

# ============================================================
# 3. CÁC HÀM XỬ LÝ
# ============================================================
def tim_tuan_tu(he_thong, ma_kh):
    phep_so_sanh = 0
    for kh in he_thong.danh_sach_kh:
        phep_so_sanh += 1
        if kh.ma_kh == ma_kh:
            return kh, phep_so_sanh
    return None, phep_so_sanh

def tim_bang_dictionary(he_thong, ma_kh):
    return he_thong.tu_dien_kh.get(ma_kh, None)

def sort_theo_ten(danh_sach, tu_A_den_Z=True):
    return sorted(danh_sach, key=lambda kh: kh.ho_ten.strip().split()[-1].lower(), reverse=not tu_A_den_Z)

def sort_theo_so_du(danh_sach, cao_den_thap=True):
    return sorted(danh_sach, key=lambda kh: kh.so_du, reverse=cao_den_thap)

def sort_theo_ngay_dang_ky(danh_sach, cu_den_moi=True):
    return sorted(danh_sach, key=lambda kh: datetime.strptime(kh.ngay_dang_ky, "%Y-%m-%d"), reverse=not cu_den_moi)

def chuyen_doi_dataframe(danh_sach):
    if not danh_sach:
        return pd.DataFrame(columns=CAC_COT)
    data = [{
        "ma_kh": kh.ma_kh, "ho_ten": kh.ho_ten, "sdt": kh.sdt, "email": kh.email,
        "cccd": kh.cccd, "dia_phuong": kh.dia_phuong, "loai_kh": kh.loai_kh,
        "so_du": kh.so_du, "ngay_dang_ky": kh.ngay_dang_ky
    } for kh in danh_sach]
    return pd.DataFrame(data)

# ============================================================
# 4. GIAO DIỆN STREAMLIT (DẠNG TAB NGANG Y HỆT ẢNH MẪU)
# ============================================================
st.set_page_config(page_title="Quản lý và tra cứu hồ sơ khách hàng tại ngân hàng", page_icon="🏦", layout="wide")
st.title("🏦 QUẢN LÝ VÀ TRA CỨU HỒ SƠ KHÁCH HÀNG TẠI NGÂN HÀNG")
st.markdown("---")

# Tạo thanh menu ngang bằng st.tabs y hệt hình mẫu yêu cầu
tab_ds, tab_them, tab_sua, tab_xoa, tab_tim, tab_hieu_nang, tab_sap_xep, tab_thong_ke, tab_csv = st.tabs([
    "📋 Danh sách", 
    "➕ Thêm mới", 
    "✏️ Sửa", 
    "❌ Xóa khách hàng", 
    "🔍 Tra Cứu", 
    "⚡ Hiệu năng", 
    "📊 Sắp xếp",
    "📈 Thống Kê", 
    "📁 Quản Lý CSV"
])

# ----------------- TAB 1: HIỂN THỊ DANH SÁCH -----------------
with tab_ds:
    st.subheader("📋 Danh sách khách hàng")
    if st.button("🔄 Làm mới danh sách"):
        st.rerun()
    st.metric("Tổng khách hàng", len(ht.danh_sach_kh))
    st.dataframe(chuyen_doi_dataframe(ht.danh_sach_kh), use_container_width=True)

# ----------------- TAB 2: THÊM KHÁCH HÀNG MỚI -----------------
with tab_them:
    st.subheader("➕ Thêm khách hàng")
    with st.form("form_them"):
        col1, col2 = st.columns(2)
        with col1:
            ma_kh = st.text_input("Mã khách hàng (VD: KH001)").strip().upper()
            ho_ten = st.text_input("Họ và tên").strip()
            sdt = st.text_input("Số điện thoại").strip()
            email = st.text_input("Email").strip().lower()
            cccd = st.text_input("CCCD").strip()
        with col2:
            dia_phuong = st.text_input("Địa phương").strip()
            loai_kh = st.selectbox("Phân hạng khách hàng", ["Standard", "VIP", "Doanh nghiep"])
            so_du = st.number_input("Số dư ban đầu (VND)", min_value=0.0, step=1000000.0)
            ngay_dang_ky = datetime.today().strftime("%Y-%m-%d")

        if st.form_submit_button("Xác nhận thêm"):
            if not ma_kh or not ho_ten:
                st.error("[LỖI] Mã KH và Họ tên không được để trống!")
            elif ma_kh in ht.tu_dien_kh:
                st.error("[LỖI] Mã khách hàng đã tồn tại!")
            else:
                kh = KhachHang(ma_kh, ho_ten, sdt, email, cccd, dia_phuong, loai_kh, so_du, ngay_dang_ky)
                if ht.them_khach_hang(kh):
                    st.success("[THÀNH CÔNG] Đã thêm khách hàng mới!")
                else:
                    st.error("[LỖI] Trùng thông tin (CCCD/Email/SĐT)!")

# ----------------- TAB 3: SỬA THÔNG TIN KHÁCH HÀNG -----------------
with tab_sua:
    st.subheader("✏️ Cập nhật thông tin khách hàng")
    ma_sua = st.selectbox("Chọn mã khách hàng cần sửa", [""] + list(ht.tu_dien_kh.keys()), key="select_sua")
    if ma_sua:
        kh = ht.tu_dien_kh[ma_sua]
        with st.form("form_sua"):
            email_moi = st.text_input("Email mới", value=kh.email)
            sdt_moi = st.text_input("SĐT mới", value=kh.sdt)
            cccd_moi = st.text_input("CCCD mới", value=kh.cccd)
            dia_phuong_moi = st.text_input("Địa phương mới", value=kh.dia_phuong)
            loai_kh_moi = st.selectbox("Phân hạng KH", ["Standard", "VIP", "Doanh nghiep"], index=["Standard", "VIP", "Doanh nghiep"].index(kh.loai_kh) if kh.loai_kh in ["Standard", "VIP", "Doanh nghiep"] else 0)

            if st.form_submit_button("Lưu thay đổi"):
                kh.email = email_moi.strip().lower()
                kh.sdt = sdt_moi.strip()
                kh.cccd = cccd_moi.strip()
                kh.dia_phuong = dia_phuong_moi.strip()
                kh.loai_kh = loai_kh_moi
                st.success("[THÀNH CÔNG] Cập nhật thành công!")

# ----------------- TAB 4: XÓA KHÁCH HÀNG -----------------
with tab_xoa:
    st.subheader("🗑️ Xóa khách hàng")
    ma_xoa = st.selectbox("Chọn mã khách hàng cần xóa", [""] + list(ht.tu_dien_kh.keys()), key="select_xoa")
    if ma_xoa and st.button("Xác nhận xóa"):
        kh = ht.tu_dien_kh[ma_xoa]
        ht.tap_hop_cccd.remove(kh.cccd)
        ht.tap_hop_email.remove(kh.email)
        ht.tap_hop_sdt.remove(kh.sdt)
        ht.danh_sach_kh.remove(kh)
        del ht.tu_dien_kh[ma_xoa]
        st.success("Đã xóa khách hàng!")
        st.rerun()

# ----------------- TAB 5: TRA CỨU -----------------
with tab_tim:
    st.subheader("🔍 Tra Cứu")
    loai_tim = st.selectbox("Chọn phương thức tra cứu:", [
        "1. Tìm theo mã khách hàng",
        "2. Tìm theo tên",
        "3. Tìm theo địa phương",
        "4. Tìm theo phân hạng"
    ], key="select_loai_tim")

    if "1. Tìm theo mã khách hàng" in loai_tim:
        ma = st.text_input("Nhập mã (VD: KH003):", key="tim_ma").strip().upper()
        if st.button("Tìm kiếm", key="btn_tim_ma"):
            kh = tim_bang_dictionary(ht, ma)
            if kh: st.dataframe(chuyen_doi_dataframe([kh]), use_container_width=True)
            else: st.error("Không tìm thấy.")
    elif "2. Tìm theo tên" in loai_tim:
        ten = st.text_input("Nhập tên:", key="tim_ten").strip().lower()
        if st.button("Tìm kiếm", key="btn_tim_ten"):
            ket_qua = [kh for kh in ht.danh_sach_kh if ten in kh.ho_ten.lower()]
            st.dataframe(chuyen_doi_dataframe(ket_qua), use_container_width=True)
    elif "3. Tìm theo địa phương" in loai_tim:
        dp = st.text_input("Nhập địa phương:", key="tim_dp").strip().lower()
        if st.button("Tìm kiếm", key="btn_tim_dp"):
            ket_qua = [kh for kh in ht.danh_sach_kh if dp in kh.dia_phuong.lower()]
            st.dataframe(chuyen_doi_dataframe(ket_qua), use_container_width=True)
    elif "4. Tìm theo loại KH" in loai_tim:
        lkh = st.selectbox("Chọn phân hạng:", ["Standard", "VIP", "Doanh nghiep"], key="chon_lkh")
        if st.button("Tìm kiếm", key="btn_tim_lkh"):
            ket_qua = [kh for kh in ht.danh_sach_kh if kh.loai_kh.lower() == lkh.lower()]
            st.dataframe(chuyen_doi_dataframe(ket_qua), use_container_width=True)

# ----------------- TAB 6: HIỆU NĂNG -----------------
with tab_hieu_nang:
    st.subheader("⚡ So sánh hiệu năng")
    ma = st.text_input("Nhập mã khách hàng:", key="hn_ma").strip().upper()
    if st.button("Chạy đo đạc tốc độ", key="btn_hn"):
        if ma:
            t1 = time.perf_counter_ns()
            _, so_ss = tim_tuan_tu(ht, ma)
            t2 = time.perf_counter_ns()
            dt_seq = t2 - t1

            t3 = time.perf_counter_ns()
            tim_bang_dictionary(ht, ma)
            t4 = time.perf_counter_ns()
            dt_dict = t4 - t3

            col1, col2 = st.columns(2)
            col1.metric("Tìm Tuần tự", f"{dt_seq:,} ns", f"{so_ss} phép so sánh")
            col2.metric("Tìm Dictionary", f"{dt_dict:,} ns", "O(1)")
            if dt_dict > 0:
                st.success(f"🚀 Dictionary nhanh hơn khoảng {dt_seq / dt_dict:.1f} lần!")
        else:
            st.warning("Vui lòng nhập mã khách hàng.")

# ----------------- TAB 7: SẮP XẾP DANH SÁCH -----------------
with tab_sap_xep:
    st.subheader("📊 Sắp xếp danh sách")
    tieu_chi = st.selectbox("Chọn tiêu chí:", [
        "Sort theo tên A -> Z",
        "Sort theo số dư cao -> thấp",
        "Sort theo ngày đăng ký cũ -> mới"
    ], key="select_sort")
    ds = list(ht.danh_sach_kh)
    if "A -> Z" in tieu_chi: ds = sort_theo_ten(ds, True)
    elif "cao -> thấp" in tieu_chi: ds = sort_theo_so_du(ds, True)
    elif "cũ -> mới" in tieu_chi: ds = sort_theo_ngay_dang_ky(ds, True)
    st.dataframe(chuyen_doi_dataframe(ds), use_container_width=True)

# ----------------- TAB 8: THỐNG KÊ KHÁCH HÀNG -----------------
with tab_thong_ke:
    st.subheader("📈 Thống kê")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Theo phân hạng")
        tk_loai = {}
        for kh in ht.danh_sach_kh: tk_loai[kh.loai_kh] = tk_loai.get(kh.loai_kh, 0) + 1
        st.bar_chart(pd.DataFrame(list(tk_loai.items()), columns=["Loại", "SL"]).set_index("Loại"))
    with c2:
        st.markdown("### Theo địa phương")
        tk_dp = {}
        for kh in ht.danh_sach_kh: tk_dp[kh.dia_phuong] = tk_dp.get(kh.dia_phuong, 0) + 1
        st.bar_chart(pd.DataFrame(list(tk_dp.items()), columns=["Địa phương", "SL"]).set_index("Địa phương"))

# ----------------- TAB 9: QUẢN LÝ CSV (IMPORT / EXPORT) -----------------
with tab_csv:
    st.subheader("📁 Quản lý CSV")
    
    st.markdown("### 📥 Nhập danh sách từ file CSV (Import)")
    up
