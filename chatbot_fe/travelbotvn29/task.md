# 📋 Travelbot Frontend Tasks

## 1. Cấu hình dự án
- [ ] Tạo project **Next.js + TypeScript + TailwindCSS**
- [ ] Cấu hình **ShadCN UI** (Button, Input, Card, Modal, Table)
- [ ] Thiết lập alias `@/components`, `@/hooks`, `@/store`, `@/lib`, `@/types`
- [ ] Tạo file `axiosClient.ts` trong `/lib` (để gọi API REST phụ trợ)
- [ ] Cấu hình font & theme màu du lịch (xanh dương – trắng – vàng)

---

## 2. Giao diện Chatbot (Public)
- [ ] Tạo component `ChatWidget.tsx` (khung chat popup)
- [ ] Tạo `MessageInput.tsx` (gửi message qua socket)
- [ ] Hiển thị hội thoại user ↔ bot (`ChatMessage.tsx`)
- [ ] Tích hợp **WebSocket** event listener (nhận phản hồi từ bot)
- [ ] Hiển thị gợi ý nhanh (quick replies / card list / hình ảnh nếu có)
- [ ] Giữ state hội thoại trong `chatStore` (Zustand)
- [ ] Xử lý intent cơ bản (ví dụ: `show_destinations`, `get_hotels`, `get_tours`) và hiển thị card tương ứng

---

## 3. Trang Public
- [ ] `/destinations`: danh sách điểm đến (ảnh, tên, vùng, rating)
- [ ] `/tours`: danh sách tour (tên, số ngày, giá)
- [ ] `/hotels`: danh sách khách sạn (sao, giá, tiện nghi)
- [ ] `/restaurants`: danh sách nhà hàng (ẩm thực, giá, rating)
- [ ] `/about`: giới thiệu Travelbot, mục tiêu dự án
- [ ] Thiết kế responsive + hiển thị dữ liệu từ backend REST API

---

## 4. Trang Admin
- [ ] `/admin/login`: đăng nhập (JWT hoặc session cookie)
- [ ] `/admin/dashboard`: tổng quan số lượng dữ liệu (destinations, hotels, tours, v.v.)
- [ ] `/admin/destinations`: CRUD địa điểm  
  - Trường: `name`, `province`, `region`, `rating`, `best_time_to_visit`, `description`
- [ ] `/admin/hotels`: CRUD khách sạn  
  - Trường: `name`, `destination_id`, `star_rating`, `price_range`, `rating`, `amenities`
- [ ] `/admin/restaurants`: CRUD nhà hàng  
  - Trường: `name`, `destination_id`, `cuisine_type`, `price_range`, `rating`
- [ ] `/admin/tours`: CRUD tour  
  - Trường: `name`, `destinations`, `duration_days`, `price`, `description`
- [ ] `/admin/activities`: CRUD hoạt động (type, price, duration, description)
- [ ] `/admin/weather`: CRUD thời tiết (destination_id, month, avg_temp, description, is_best_time)
- [ ] `/admin/transportation`: CRUD phương tiện di chuyển (from/to destination, type, duration, price_range)
- [ ] `/admin/reviews`: CRUD đánh giá (entity_type, entity_id, rating, comment)
- [ ] Reuse `DataTable` component để hiển thị danh sách CRUD
- [ ] Validate form với **React Hook Form + Zod**

---

## 5. Hooks & Store
- [ ] `useChat.ts`: quản lý logic gửi/nhận tin nhắn, kết nối WebSocket
- [ ] `useAuth.ts`: login/logout, lưu token
- [ ] `useAdminCRUD.ts`: lấy + thao tác CRUD với API
- [ ] `chatStore.ts`: lưu hội thoại
- [ ] `authStore.ts`: lưu trạng thái đăng nhập admin
- [ ] `uiStore.ts`: lưu trạng thái modal, loading, v.v.

---

## 6. UI/UX & Testing
- [ ] Áp dụng phong cách du lịch (tone xanh biển, cam nhạt)
- [ ] Thiết kế responsive, tối ưu cho mobile
- [ ] Loading state / Empty state / Error state
- [ ] Kiểm tra UI cơ bản (component hoạt động đúng)
