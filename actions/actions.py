from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from rasa_sdk import FormValidationAction
from rasa_sdk.types import DomainDict

DB_CONFIG = {
    'host': 'localhost',
    'database': 'travel_chatbot',
    'user': 'postgres',
    'password': 'test1234',
    'port': 5432
}

def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_CONFIG)

def format_results(results, entity_type):
    """Format database results into readable text"""
    if not results:
        return "Xin lỗi, tôi không tìm thấy kết quả phù hợp."
    
    response = f"Tôi tìm thấy {len(results)} kết quả:\n\n"
    
    for idx, item in enumerate(results[:5], 1):  
        if entity_type == 'destination':
            response += f"{idx}. {item['name']} - {item['province']}\n"
            response += f"   Loại: {item['category']}\n"
            response += f"   Đánh giá: {item['rating']}/5\n"
            response += f"   {item['description'][:100]}...\n\n"
        
        elif entity_type == 'hotel':
            response += f"{idx}. {item['name']}\n"
            response += f"   Địa chỉ: {item['address']}\n"
            response += f"   Hạng sao: {item['star_rating']} sao\n"
            response += f"   Giá: {item['price_range']}\n\n"
        
        elif entity_type == 'restaurant':
            response += f"{idx}. {item['name']}\n"
            response += f"   Loại: {item['cuisine_type']}\n"
            response += f"   Giá: {item['price_range']}\n"
            response += f"   Đánh giá: {item['rating']}/5\n\n"
        
        elif entity_type == 'activity':
            response += f"{idx}. {item['name']}\n"
            response += f"   Loại: {item['type']}\n"
            response += f"   Giá: {item['price']:,} VNĐ\n"
            response += f"   Thời gian: {item['duration']}\n\n"
        
        elif entity_type == 'tour':
            response += f"{idx}. {item['name']}\n"
            response += f"   Thời gian: {item['duration_days']} ngày\n"
            response += f"   Giá: {item['price']:,} VNĐ\n\n"
    
    return response


class ActionSearchDestination(Action):
    def name(self) -> Text:
        return "action_search_destination"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        province = tracker.get_slot("province")
        region = tracker.get_slot("region")
        category = tracker.get_slot("category")
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = "SELECT * FROM destinations WHERE 1=1"
        params = []
        
        if province:
            query += " AND LOWER(province) LIKE LOWER(%s)"
            params.append(f"%{province}%")
        
        if region:
            query += " AND LOWER(region) LIKE LOWER(%s)"
            params.append(f"%{region}%")
        
        if category:
            query += " AND LOWER(category) LIKE LOWER(%s)"
            params.append(f"%{category}%")
        
        query += " ORDER BY rating DESC LIMIT 5"
        
        cur.execute(query, params)
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        message = format_results(results, 'destination')
        dispatcher.utter_message(text=message)
        
        return []


class ActionSearchHotel(Action):
    def name(self) -> Text:
        return "action_search_hotel"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        star_rating = tracker.get_slot("star_rating")
        price_range = tracker.get_slot("price_range")
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT h.* FROM hotels h
            JOIN destinations d ON h.destination_id = d.id
            WHERE 1=1
        """
        params = []
        
        if destination:
            query += " AND LOWER(d.name) LIKE LOWER(%s)"
            params.append(f"%{destination}%")
        
        if star_rating:
            try:
                rating_num = int(''.join(filter(str.isdigit, star_rating)))
                query += " AND h.star_rating = %s"
                params.append(rating_num)
            except:
                pass
        
        if price_range:
            query += " AND LOWER(h.price_range) LIKE LOWER(%s)"
            params.append(f"%{price_range}%")
        
        query += " ORDER BY h.star_rating DESC LIMIT 5"
        
        cur.execute(query, params)
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        message = format_results(results, 'hotel')
        dispatcher.utter_message(text=message)
        
        return []


class ActionSearchRestaurant(Action):
    def name(self) -> Text:
        return "action_search_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        cuisine_type = tracker.get_slot("cuisine_type")
        price_range = tracker.get_slot("price_range")
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT r.* FROM restaurants r
            JOIN destinations d ON r.destination_id = d.id
            WHERE 1=1
        """
        params = []
        
        if destination:
            query += " AND LOWER(d.name) LIKE LOWER(%s)"
            params.append(f"%{destination}%")
        
        if cuisine_type:
            query += " AND LOWER(r.cuisine_type) LIKE LOWER(%s)"
            params.append(f"%{cuisine_type}%")
        
        if price_range:
            query += " AND LOWER(r.price_range) LIKE LOWER(%s)"
            params.append(f"%{price_range}%")
        
        query += " ORDER BY r.rating DESC LIMIT 5"
        
        cur.execute(query, params)
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        message = format_results(results, 'restaurant')
        dispatcher.utter_message(text=message)
        
        return []


class ActionSearchActivity(Action):
    def name(self) -> Text:
        return "action_search_activity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        activity_type = tracker.get_slot("activity_type")
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT a.* FROM activities a
            JOIN destinations d ON a.destination_id = d.id
            WHERE 1=1
        """
        params = []
        
        if destination:
            query += " AND LOWER(d.name) LIKE LOWER(%s)"
            params.append(f"%{destination}%")
        
        if activity_type:
            query += " AND LOWER(a.type) LIKE LOWER(%s)"
            params.append(f"%{activity_type}%")
        
        query += " ORDER BY a.price ASC LIMIT 5"
        
        cur.execute(query, params)
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        message = format_results(results, 'activity')
        dispatcher.utter_message(text=message)
        
        return []


class ActionSearchTour(Action):
    def name(self) -> Text:
        return "action_search_tour"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        duration = tracker.get_slot("duration")
        price_range = tracker.get_slot("price_range")
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = "SELECT * FROM tours WHERE 1=1"
        params = []
        
        if destination:
            query += " AND destinations::text LIKE %s"
            params.append(f"%{destination}%")
        
        if duration:
            try:
                days = int(''.join(filter(str.isdigit, duration)))
                query += " AND duration_days = %s"
                params.append(days)
            except:
                pass
        
        query += " ORDER BY price ASC LIMIT 5"
        
        cur.execute(query, params)
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        message = format_results(results, 'tour')
        dispatcher.utter_message(text=message)
        
        return []


class ActionGetWeather(Action):
    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        month = tracker.get_slot("month")
        
        if not destination:
            dispatcher.utter_message(text="Bạn muốn biết thời tiết ở đâu?")
            return []
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT w.*, d.name as destination_name FROM weather w
            JOIN destinations d ON w.destination_id = d.id
            WHERE LOWER(d.name) LIKE LOWER(%s)
        """
        params = [f"%{destination}%"]
        
        if month:
            try:
                month_num = int(''.join(filter(str.isdigit, month)))
                query += " AND w.month = %s"
                params.append(month_num)
            except:
                pass
        
        cur.execute(query, params)
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        if not results:
            dispatcher.utter_message(text=f"Xin lỗi, tôi không có thông tin thời tiết cho {destination}.")
            return []
        
        response = f"Thời tiết tại {results[0]['destination_name']}:\n\n"
        for item in results:
            response += f"Tháng {item['month']}: {item['description']}, "
            response += f"nhiệt độ trung bình {item['avg_temp']}°C\n"
        
        dispatcher.utter_message(text=response)
        
        return []


class ActionGetTransportation(Action):
    def name(self) -> Text:
        return "action_get_transportation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        from_location = tracker.get_slot("from_location")
        to_location = tracker.get_slot("to_location")
        
        if not from_location or not to_location:
            dispatcher.utter_message(text="Bạn muốn đi từ đâu đến đâu?")
            return []
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT t.*, d1.name as from_name, d2.name as to_name 
            FROM transportation t
            JOIN destinations d1 ON t.from_destination_id = d1.id
            JOIN destinations d2 ON t.to_destination_id = d2.id
            WHERE LOWER(d1.name) LIKE LOWER(%s)
            AND LOWER(d2.name) LIKE LOWER(%s)
        """
        
        cur.execute(query, [f"%{from_location}%", f"%{to_location}%"])
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        if not results:
            dispatcher.utter_message(text=f"Xin lỗi, tôi không tìm thấy thông tin di chuyển từ {from_location} đến {to_location}.")
            return []
        
        response = f"Các phương tiện từ {results[0]['from_name']} đến {results[0]['to_name']}:\n\n"
        for item in results:
            response += f"• {item['type'].capitalize()}: "
            response += f"Thời gian ~{item['duration']}, "
            response += f"Giá {item['price_range']}\n"
        
        dispatcher.utter_message(text=response)
        
        return []


class ActionGetReviews(Action):
    def name(self) -> Text:
        return "action_get_reviews"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        if not destination:
            dispatcher.utter_message(text="Bạn muốn xem đánh giá về địa điểm nào?")
            return []
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get destination reviews
        query = """
            SELECT r.*, d.name as destination_name 
            FROM reviews r
            JOIN destinations d ON r.entity_id = d.id
            WHERE r.entity_type = 'destination'
            AND LOWER(d.name) LIKE LOWER(%s)
            ORDER BY r.created_at DESC
            LIMIT 5
        """
        
        cur.execute(query, [f"%{destination}%"])
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        if not results:
            dispatcher.utter_message(text=f"Chưa có đánh giá về {destination}.")
            return []
        
        avg_rating = sum(r['rating'] for r in results) / len(results)
        response = f"Đánh giá về {results[0]['destination_name']}:\n"
        response += f"Điểm trung bình: {avg_rating:.1f}/5 ({len(results)} đánh giá)\n\n"
        
        for idx, item in enumerate(results[:3], 1):
            response += f"{idx}. {item['rating']}/5 - {item['comment'][:100]}...\n"
        
        dispatcher.utter_message(text=response)
        
        return []


class ActionRecommendBudget(Action):
    def name(self) -> Text:
        return "action_recommend_budget"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        duration = tracker.get_slot("duration")
        
        if not destination:
            dispatcher.utter_message(text="Bạn muốn đi đâu để tôi tính ngân sách giúp bạn?")
            return []
        
        # Default duration
        days = 3
        if duration:
            try:
                days = int(''.join(filter(str.isdigit, duration)))
            except:
                pass
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get average hotel and restaurant prices
        query = """
            SELECT 
                d.name as destination_name,
                AVG(CASE 
                    WHEN h.price_range = 'rẻ' THEN 500000
                    WHEN h.price_range = 'trung bình' THEN 1000000
                    WHEN h.price_range = 'cao cấp' THEN 2500000
                    ELSE 1000000
                END) as avg_hotel_price,
                AVG(CASE 
                    WHEN r.price_range = 'rẻ' THEN 100000
                    WHEN r.price_range = 'trung bình' THEN 250000
                    WHEN r.price_range = 'cao cấp' THEN 500000
                    ELSE 200000
                END) as avg_restaurant_price
            FROM destinations d
            LEFT JOIN hotels h ON h.destination_id = d.id
            LEFT JOIN restaurants r ON r.destination_id = d.id
            WHERE LOWER(d.name) LIKE LOWER(%s)
            GROUP BY d.name
        """
        
        cur.execute(query, [f"%{destination}%"])
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not result:
            dispatcher.utter_message(text=f"Xin lỗi, tôi không có đủ thông tin về {destination} để tính ngân sách.")
            return []
        
        hotel_per_night = result['avg_hotel_price'] or 1000000
        food_per_day = (result['avg_restaurant_price'] or 200000) * 3  # 3 meals
        activities_per_day = 300000
        transport = 500000
        
        total_budget = (hotel_per_night * days) + (food_per_day * days) + (activities_per_day * days) + transport
        
        response = f"Ngân sách dự kiến cho chuyến đi {result['destination_name']} ({days} ngày):\n\n"
        response += f"• Khách sạn: {hotel_per_night:,} VNĐ/đêm × {days} đêm = {hotel_per_night * days:,} VNĐ\n"
        response += f"• Ăn uống: {food_per_day:,} VNĐ/ngày × {days} ngày = {food_per_day * days:,} VNĐ\n"
        response += f"• Hoạt động/Tham quan: {activities_per_day:,} VNĐ/ngày × {days} ngày = {activities_per_day * days:,} VNĐ\n"
        response += f"• Di chuyển: {transport:,} VNĐ\n"
        response += f"\n💰 Tổng cộng: {total_budget:,} VNĐ\n"
        response += f"(Ước tính cho 1 người, chưa bao gồm vé máy bay)\n"
        
        dispatcher.utter_message(text=response)
        
        return []
    
class ActionGetBestTime(Action):
    def name(self) -> Text:
        return "action_get_best_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        if not destination:
            dispatcher.utter_message(text="Bạn muốn biết thời điểm tốt nhất để đi đâu?")
            return []
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT d.name, d.best_time_to_visit, w.month, w.description
            FROM destinations d
            LEFT JOIN weather w ON w.destination_id = d.id
            WHERE LOWER(d.name) LIKE LOWER(%s)
            AND w.is_best_time = true
            ORDER BY w.month
        """
        
        cur.execute(query, [f"%{destination}%"])
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        if not results:
            dispatcher.utter_message(text=f"Xin lỗi, tôi không có thông tin về thời điểm tốt nhất để đi {destination}.")
            return []
        
        response = f"Thời điểm tốt nhất để đi {results[0]['name']}:\n\n"
        response += f"📅 {results[0]['best_time_to_visit']}\n\n"
        
        if len(results) > 0:
            response += "Chi tiết:\n"
            for item in results:
                response += f"• Tháng {item['month']}: {item['description']}\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionCompareDestinations(Action):
    def name(self) -> Text:
        return "action_compare_destinations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get all destination entities from the latest message
        entities = tracker.latest_message.get('entities', [])
        destinations = [e['value'] for e in entities if e['entity'] == 'destination']
        
        if len(destinations) < 2:
            dispatcher.utter_message(text="Bạn muốn so sánh những địa điểm nào? Vui lòng cho tôi biết ít nhất 2 địa điểm.")
            return []
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT name, province, category, rating, description, best_time_to_visit
            FROM destinations
            WHERE LOWER(name) LIKE LOWER(%s) OR LOWER(name) LIKE LOWER(%s)
            ORDER BY rating DESC
        """
        
        cur.execute(query, [f"%{destinations[0]}%", f"%{destinations[1]}%"])
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        if len(results) < 2:
            dispatcher.utter_message(text="Xin lỗi, tôi không tìm thấy đủ thông tin để so sánh.")
            return []
        
        response = f"So sánh giữa {results[0]['name']} và {results[1]['name']}:\n\n"
        
        for idx, dest in enumerate(results[:2], 1):
            response += f"{idx}. {dest['name']} ({dest['province']})\n"
            response += f"   • Loại: {dest['category']}\n"
            response += f"   • Đánh giá: {dest['rating']}/5\n"
            response += f"   • Thời điểm tốt nhất: {dest['best_time_to_visit']}\n"
            response += f"   • Mô tả: {dest['description'][:100]}...\n\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetTravelTips(Action):
    def name(self) -> Text:
        return "action_get_travel_tips"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        traveler_type = tracker.get_slot("traveler_type")
        
        tips = "🎒 Mẹo du lịch hữu ích:\n\n"
        
        if traveler_type and "nữ" in traveler_type.lower():
            tips += "👩 Dành cho nữ du khách:\n"
            tips += "• Chia sẻ lịch trình với người thân\n"
            tips += "• Tránh đi về khuya một mình\n"
            tips += "• Giữ liên lạc thường xuyên\n"
            tips += "• Chọn nơi ở có đánh giá tốt về an toàn\n\n"
        
        tips += "💡 Mẹo chung:\n"
        tips += "• Mua bảo hiểm du lịch\n"
        tips += "• Sao lưu giấy tờ quan trọng\n"
        tips += "• Mang theo thuốc cần thiết\n"
        tips += "• Học vài câu tiếng Việt cơ bản\n"
        tips += "• Tải bản đồ offline\n"
        tips += "• Mang theo tiền mặt (nhiều nơi chưa nhận thẻ)\n"
        
        if destination:
            tips += f"\n📍 Đặc biệt cho {destination}:\n"
            tips += "• Kiểm tra thời tiết trước khi đi\n"
            tips += "• Đặt chỗ trước trong mùa cao điểm\n"
            tips += "• Tìm hiểu phong tục địa phương\n"
        
        dispatcher.utter_message(text=tips)
        return []


class ActionGetTravelDocuments(Action):
    def name(self) -> Text:
        return "action_get_travel_documents"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = "📋 Giấy tờ cần thiết khi du lịch trong nước:\n\n"
        response += "✅ Bắt buộc:\n"
        response += "• CMND/CCCD hoặc Hộ chiếu\n"
        response += "• Giấy khai sinh (cho trẻ em dưới 14 tuổi)\n\n"
        response += "📝 Nên mang theo:\n"
        response += "• Bảo hiểm y tế\n"
        response += "• Bảo hiểm du lịch (nếu có)\n"
        response += "• Thẻ ATM/tín dụng\n"
        response += "• Sổ tiêm chủng (nếu có yêu cầu)\n\n"
        response += "💳 Thanh toán:\n"
        response += "• Tiền mặt (VNĐ)\n"
        response += "• Thẻ ngân hàng\n"
        response += "• Ví điện tử (MoMo, ZaloPay, ...)\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetSpecialRequirements(Action):
    def name(self) -> Text:
        return "action_get_special_requirements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        special_need = tracker.get_slot("special_need")
        
        response = "♿ Hỗ trợ cho du khách có nhu cầu đặc biệt:\n\n"
        
        if special_need and "khuyết tật" in special_need.lower():
            response += "🦽 Dành cho người khuyết tật:\n"
            response += "• Tìm khách sạn có thang máy và phòng tiếp cận\n"
            response += "• Liên hệ trước về xe di chuyển phù hợp\n"
            response += "• Chọn điểm tham quan có đường dốc/thang máy\n"
            response += "• Mang theo giấy tờ y tế và thuốc cần thiết\n\n"
        
        response += "👴 Người cao tuổi:\n"
        response += "• Chọn tour nhịp độ chậm\n"
        response += "• Nghỉ ngơi đầy đủ\n"
        response += "• Mang thuốc thường dùng\n\n"
        
        response += "👶 Trẻ em:\n"
        response += "• Chuẩn bị đồ chơi, đồ ăn vặt\n"
        response += "• Chọn nơi ở thân thiện với trẻ em\n"
        response += "• Lên kế hoạch linh hoạt\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetPackingList(Action):
    def name(self) -> Text:
        return "action_get_packing_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        season = tracker.get_slot("season")
        
        response = "🎒 Danh sách đồ cần mang:\n\n"
        response += "👕 Quần áo:\n"
        
        if season and "đông" in season.lower():
            response += "• Áo khoác ấm, áo len\n"
            response += "• Quần dài\n"
            response += "• Khăn quàng cổ, găng tay\n"
        elif season and "hè" in season.lower():
            response += "• Quần áo mỏng, thoáng mát\n"
            response += "• Áo tắm\n"
            response += "• Nón/mũ chống nắng\n"
        else:
            response += "• Quần áo phù hợp thời tiết\n"
            response += "• Áo khoác nhẹ\n"
        
        response += "\n🔋 Đồ dùng:\n"
        response += "• Sạc điện thoại, pin dự phòng\n"
        response += "• Thuốc cá nhân\n"
        response += "• Kem chống nắng\n"
        response += "• Đồ vệ sinh cá nhân\n"
        response += "• Túi đựng rác\n\n"
        
        response += "📱 Công nghệ:\n"
        response += "• Điện thoại + sạc\n"
        response += "• Camera (nếu có)\n"
        response += "• Tai nghe\n"
        
        if destination:
            if "biển" in destination.lower() or "nha trang" in destination.lower() or "phú quốc" in destination.lower():
                response += "\n🏖️ Đặc biệt cho du lịch biển:\n"
                response += "• Đồ bơi\n"
                response += "• Kính bơi\n"
                response += "• Dép lào\n"
                response += "• Túi chống nước\n"
            elif "sapa" in destination.lower() or "đà lạt" in destination.lower():
                response += "\n⛰️ Đặc biệt cho du lịch núi:\n"
                response += "• Giày trekking\n"
                response += "• Áo ấm\n"
                response += "• Đèn pin\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetLocalCulture(Action):
    def name(self) -> Text:
        return "action_get_local_culture"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        if not destination:
            dispatcher.utter_message(text="Bạn muốn tìm hiểu văn hóa của địa phương nào?")
            return []
        
        response = f"🏮 Văn hóa địa phương tại {destination}:\n\n"
        
        # General Vietnamese culture
        response += "🙏 Phong tục chung:\n"
        response += "• Chào hỏi lịch sự\n"
        response += "• Cởi giày khi vào nhà\n"
        response += "• Ăn uống bằng đũa\n"
        response += "• Tôn trọng người lớn tuổi\n\n"
        
        # Specific destinations
        if "huế" in destination.lower():
            response += "👑 Đặc trưng Huế:\n"
            response += "• Kinh đô cổ\n"
            response += "• Ẩm thực cung đình\n"
            response += "• Nhã nhạc cung đình\n"
            response += "• Lễ hội truyền thống\n"
        elif "hội an" in destination.lower():
            response += "🏮 Đặc trưng Hội An:\n"
            response += "• Phố cổ\n"
            response += "• Lồng đèn\n"
            response += "• May đo áo dài\n"
            response += "• Ẩm thực đa văn hóa\n"
        elif "sài gòn" in destination.lower() or "tp hcm" in destination.lower():
            response += "🌆 Đặc trưng Sài Gòn:\n"
            response += "• Nhịp sống năng động\n"
            response += "• Văn hóa cà phê\n"
            response += "• Ẩm thực đường phố\n"
            response += "• Đa dạng văn hóa\n"
        else:
            response += "🎭 Hoạt động văn hóa:\n"
            response += "• Tham quan di tích lịch sử\n"
            response += "• Thưởng thức ẩm thực địa phương\n"
            response += "• Tìm hiểu nghề thủ công truyền thống\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetPhotographySpots(Action):
    def name(self) -> Text:
        return "action_get_photography_spots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        if not destination:
            dispatcher.utter_message(text="Bạn muốn tìm địa điểm chụp ảnh ở đâu?")
            return []
        
        response = f"📸 Địa điểm chụp ảnh đẹp tại {destination}:\n\n"
        
        if "hội an" in destination.lower():
            response += "1. Phố cổ Hội An (golden hour)\n"
            response += "2. Cầu Nhật Bản\n"
            response += "3. Cửa Đại beach\n"
            response += "4. Ruộng rau Trà Quế\n"
            response += "5. Chùa Cầu về đêm\n"
        elif "đà nẵng" in destination.lower():
            response += "1. Cầu Rồng\n"
            response += "2. Bà Nà Hills\n"
            response += "3. Bán đảo Sơn Trà\n"
            response += "4. Ngũ Hành Sơn\n"
            response += "5. Bãi biển Mỹ Khê\n"
        elif "đà lạt" in destination.lower():
            response += "1. Hồ Tuyền Lâm\n"
            response += "2. Ga Đà Lạt\n"
            response += "3. Đồi chè Cầu Đất\n"
            response += "4. Thiền viện Trúc Lâm\n"
            response += "5. Thác Datanla\n"
        else:
            response += "• Tìm kiếm địa danh nổi tiếng\n"
            response += "• Chụp lúc bình minh/hoàng hôn\n"
            response += "• Khám phá góc ảnh độc đáo\n"
            response += "• Tương tác với người dân địa phương\n"
        
        response += "\n💡 Tips:\n"
        response += "• Chụp vào golden hour (sáng sớm/chiều tà)\n"
        response += "• Tôn trọng nơi công cộng\n"
        response += "• Xin phép trước khi chụp người\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetNightlife(Action):
    def name(self) -> Text:
        return "action_get_nightlife"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        if not destination:
            dispatcher.utter_message(text="Bạn muốn tìm hiểu về nightlife ở đâu?")
            return []
        
        response = f"🌃 Nightlife tại {destination}:\n\n"
        
        if "sài gòn" in destination.lower() or "tp hcm" in destination.lower():
            response += "🍺 Bar/Pub:\n"
            response += "• Bùi Viện (backpacker street)\n"
            response += "• Đường Nguyễn Huệ\n"
            response += "• Khu Thảo Điền\n\n"
            response += "🎵 Club/Disco:\n"
            response += "• Khu vực Q1, Q2\n"
            response += "• Rooftop bars\n"
        elif "hà nội" in destination.lower():
            response += "🍺 Khu vui chơi:\n"
            response += "• Phố Tạ Hiện\n"
            response += "• Phố cổ Hà Nội\n"
            response += "• Khu Trúc Bạch\n"
        elif "đà nẵng" in destination.lower():
            response += "🌊 Ven biển:\n"
            response += "• Mỹ Khê beach bars\n"
            response += "• Cầu Rồng về đêm\n"
            response += "• Phố Tây An Thượng\n"
        else:
            response += "🌙 Hoạt động buổi tối:\n"
            response += "• Dạo chợ đêm\n"
            response += "• Thưởng thức ẩm thực đường phố\n"
            response += "• Tản bộ quanh thành phố\n"
        
        response += "\n⚠️ Lưu ý:\n"
        response += "• Giữ đồ cẩn thận\n"
        response += "• Không uống quá mức\n"
        response += "• Đi nhóm an toàn hơn\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetFamilyActivities(Action):
    def name(self) -> Text:
        return "action_get_family_activities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        if not destination:
            dispatcher.utter_message(text="Bạn muốn tìm hoạt động cho gia đình ở đâu?")
            return []
        
        response = f"👨‍👩‍👧‍👦 Hoạt động cho gia đình tại {destination}:\n\n"
        
        if "đà nẵng" in destination.lower():
            response += "1. Asia Park (công viên giải trí)\n"
            response += "2. Bà Nà Hills\n"
            response += "3. Bảo tàng 3D\n"
            response += "4. Bãi biển Mỹ Khê\n"
            response += "5. Ngũ Hành Sơn\n"
        elif "nha trang" in destination.lower():
            response += "1. Vinpearl Land\n"
            response += "2. Thủy cung Trí Nguyên\n"
            response += "3. Đảo Hòn Mun\n"
            response += "4. Tắm bùn I-Resort\n"
            response += "5. Công viên Biển Đông\n"
        elif "phú quốc" in destination.lower():
            response += "1. VinWonders Phú Quốc\n"
            response += "2. Safari Phú Quốc\n"
            response += "3. Bãi Sao\n"
            response += "4. Grand World\n"
            response += "5. Sunset Sanato Beach Club\n"
        else:
            response += "🎯 Gợi ý:\n"
            response += "• Công viên giải trí\n"
            response += "• Bảo tàng\n"
            response += "• Vườn thú\n"
            response += "• Bãi biển\n"
            response += "• Hoạt động ngoài trời\n"
        
        response += "\n💡 Tips:\n"
        response += "• Lên kế hoạch linh hoạt\n"
        response += "• Mang đồ ăn vặt cho trẻ\n"
        response += "• Nghỉ ngơi đầy đủ\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetAdventureActivities(Action):
    def name(self) -> Text:
        return "action_get_adventure_activities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        if not destination:
            dispatcher.utter_message(text="Bạn muốn tìm hoạt động mạo hiểm ở đâu?")
            return []
        
        response = f"🏃 Hoạt động mạo hiểm tại {destination}:\n\n"
        
        if "đà lạt" in destination.lower():
            response += "1. Canyoning\n"
            response += "2. Zipline\n"
            response += "3. Trekking\n"
            response += "4. Đua xe ATV\n"
            response += "5. Paragliding\n"
        elif "nha trang" in destination.lower():
            response += "1. Lặn biển\n"
            response += "2. Lướt ván\n"
            response += "3. Dù lượn trên biển\n"
            response += "4. Jet ski\n"
            response += "5. Flyboard\n"
        elif "sapa" in destination.lower():
            response += "1. Trekking Fansipan\n"
            response += "2. Chinh phục đỉnh núi\n"
            response += "3. Đi xe máy qua đèo\n"
            response += "4. Cắm trại\n"
        else:
            response += "⚡ Các hoạt động:\n"
            response += "• Thể thao dưới nước\n"
            response += "• Leo núi/trekking\n"
            response += "• Thể thao mạo hiểm\n"
            response += "• Khám phá hang động\n"
        
        response += "\n⚠️ An toàn:\n"
        response += "• Sử dụng thiết bị bảo hộ\n"
        response += "• Đi với hướng dẫn viên\n"
        response += "• Kiểm tra sức khỏe trước\n"
        response += "• Mua bảo hiểm\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetRomanticSpots(Action):
    def name(self) -> Text:
        return "action_get_romantic_spots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = "💑 Địa điểm lãng mạn cho cặp đôi:\n\n"
        response += "🏖️ Biển:\n"
        response += "• Phú Quốc - Bãi Sao\n"
        response += "• Nha Trang - Vinpearl\n"
        response += "• Đà Nẵng - Mỹ Khê\n\n"
        
        response += "🏔️ Núi:\n"
        response += "• Đà Lạt - thành phố tình yêu\n"
        response += "• Sapa - ruộng bậc thang\n"
        response += "• Tam Đảo\n\n"
        
        response += "🏛️ Văn hóa:\n"
        response += "• Hội An - phố cổ\n"
        response += "• Huế - kinh đô\n"
        response += "• Ninh Bình - Tràng An\n\n"
        
        response += "💡 Hoạt động lãng mạn:\n"
        response += "• Ngắm hoàng hôn\n"
        response += "• Dinner on the beach\n"
        response += "• Spa couple\n"
        response += "• Chụp ảnh cưới\n"
        response += "• Dạo phố cổ\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetFoodTour(Action):
    def name(self) -> Text:
        return "action_get_food_tour"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        if not destination:
            dispatcher.utter_message(text="Bạn muốn khám phá ẩm thực ở đâu?")
            return []
        
        response = f"🍜 Tour ẩm thực tại {destination}:\n\n"
        
        if "hà nội" in destination.lower():
            response += "🥖 Món phải thử:\n"
            response += "1. Phở Hà Nội\n"
            response += "2. Bún chả\n"
            response += "3. Bánh cuốn\n"
            response += "4. Chả cá Lã Vọng\n"
            response += "5. Cà phê trứng\n\n"
            response += "📍 Khu vực:\n"
            response += "• Phố cổ Hà Nội\n"
            response += "• Chợ Đồng Xuân\n"
            response += "• Phố Tạ Hiện\n"
        elif "sài gòn" in destination.lower() or "tp hcm" in destination.lower():
            response += "🍲 Món phải thử:\n"
            response += "1. Bánh mì\n"
            response += "2. Hủ tiếu\n"
            response += "3. Cơm tấm\n"
            response += "4. Bánh xèo\n"
            response += "5. Bún riêu\n\n"
            response += "📍 Khu vực:\n"
            response += "• Chợ Bến Thành\n"
            response += "• Khu Bùi Viện\n"
            response += "• Chợ Cư xá Đô Thành\n"
        elif "huế" in destination.lower():
            response += "🍛 Món phải thử:\n"
            response += "1. Bún bò Huế\n"
            response += "2. Bánh bèo, bánh nậm\n"
            response += "3. Cơm hến\n"
            response += "4. Nem lụi\n"
            response += "5. Chè Huế\n\n"
            response += "📍 Khu vực:\n"
            response += "• Phố đi bộ Huế\n"
            response += "• Chợ Đông Ba\n"
        elif "đà nẵng" in destination.lower():
            response += "🐟 Món phải thử:\n"
            response += "1. Mì Quảng\n"
            response += "2. Bánh tráng cuốn thịt heo\n"
            response += "3. Bún chả cá\n"
            response += "4. Hải sản tươi sống\n"
            response += "5. Bánh xèo Đà Nẵng\n\n"
            response += "📍 Khu vực:\n"
            response += "• Chợ Cồn\n"
            response += "• Đường Hoàng Diệu\n"
        elif "hội an" in destination.lower():
            response += "🥘 Món phải thử:\n"
            response += "1. Cao lầu\n"
            response += "2. Bánh mì Phượng\n"
            response += "3. Cơm gà\n"
            response += "4. Bánh vạc (White Rose)\n"
            response += "5. Hoành thánh\n\n"
            response += "📍 Khu vực:\n"
            response += "• Phố cổ Hội An\n"
            response += "• Chợ Hội An\n"
        else:
            response += "🍴 Khám phá ẩm thực:\n"
            response += "• Thử món đặc sản địa phương\n"
            response += "• Ăn ở quán ăn bình dân\n"
            response += "• Tham gia food tour\n"
            response += "• Ghé chợ địa phương\n"
            response += "• Học nấu ăn\n"
        
        response += "\n💡 Tips:\n"
        response += "• Ăn ở nơi đông khách\n"
        response += "• Hỏi người địa phương\n"
        response += "• Thử món đường phố\n"
        response += "• Mang tiền mặt\n"
        
        dispatcher.utter_message(text=response)
        return []


class ValidateSearchDestinationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_search_destination_form"

    def validate_destination(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate destination value."""
        
        if slot_value and len(slot_value) > 2:
            return {"destination": slot_value}
        else:
            dispatcher.utter_message(text="Vui lòng nhập tên điểm đến hợp lệ (ít nhất 3 ký tự).")
            return {"destination": None}


class ValidateSearchHotelForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_search_hotel_form"

    def validate_destination(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate destination value."""
        
        if slot_value and len(slot_value) > 2:
            return {"destination": slot_value}
        else:
            dispatcher.utter_message(text="Vui lòng nhập tên điểm đến hợp lệ (ít nhất 3 ký tự).")
            return {"destination": None}