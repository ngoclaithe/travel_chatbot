from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2
from psycopg2.extras import RealDictCursor
import json

# Database connection configuration
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
    
    for idx, item in enumerate(results[:5], 1):  # Limit to 5 results
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
            # Extract number from star_rating (e.g., "5 sao" -> 5)
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