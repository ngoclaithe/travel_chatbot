from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import logging

logger = logging.getLogger(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'database': 'travel_chatbot',
    'user': 'postgres',
    'password': 'test1234',
    'port': 5432
}

def get_db_connection():
    """Create database connection"""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

def format_results(results, entity_type):
    """Format database results into readable text"""
    if not results:
        return "Xin lỗi, tôi không tìm thấy kết quả phù hợp. Bạn có thể thử tìm kiếm khác không?"
    
    response = f"Tôi tìm thấy {len(results)} kết quả:\n\n"
    
    for idx, item in enumerate(results[:5], 1):
        if entity_type == 'destination':
            response += f"{idx}. 📍 {item['name']}"
            if item.get('province'):
                response += f" - {item['province']}"
            response += f"\n   ⭐ Đánh giá: {item.get('rating', 'N/A')}/5\n"
            if item.get('category'):
                response += f"   🏷️ Loại: {item['category']}\n"
            if item.get('description'):
                desc = item['description'][:100] + "..." if len(item['description']) > 100 else item['description']
                response += f"   📝 {desc}\n"
            response += "\n"
        
        elif entity_type == 'hotel':
            response += f"{idx}. 🏨 {item['name']}\n"
            if item.get('address'):
                response += f"   📍 {item['address']}\n"
            if item.get('star_rating'):
                response += f"   ⭐ {item['star_rating']} sao\n"
            if item.get('price_range'):
                response += f"   💰 Giá: {item['price_range']}\n"
            if item.get('amenities'):
                try:
                    amenities = json.loads(item['amenities']) if isinstance(item['amenities'], str) else item['amenities']
                    if amenities and isinstance(amenities, list):
                        response += f"   🎯 Tiện ích: {', '.join(amenities[:3])}\n"
                except:
                    pass
            response += "\n"
        
        elif entity_type == 'restaurant':
            response += f"{idx}. 🍽️ {item['name']}\n"
            if item.get('cuisine_type'):
                response += f"   🍜 Loại: {item['cuisine_type']}\n"
            if item.get('price_range'):
                response += f"   💰 Giá: {item['price_range']}\n"
            if item.get('rating'):
                response += f"   ⭐ Đánh giá: {item['rating']}/5\n"
            if item.get('specialties'):
                response += f"   🌟 Đặc sản: {item['specialties']}\n"
            response += "\n"
        
        elif entity_type == 'activity':
            response += f"{idx}. 🎯 {item['name']}\n"
            if item.get('type'):
                response += f"   🏷️ Loại: {item['type']}\n"
            if item.get('price'):
                response += f"   💰 Giá: {item['price']:,} VNĐ\n"
            if item.get('duration'):
                response += f"   ⏱️ Thời gian: {item['duration']}\n"
            if item.get('description'):
                desc = item['description'][:80] + "..." if len(item['description']) > 80 else item['description']
                response += f"   📝 {desc}\n"
            response += "\n"
        
        elif entity_type == 'tour':
            response += f"{idx}. 🎫 {item['name']}\n"
            if item.get('duration_days'):
                response += f"   📅 Thời gian: {item['duration_days']} ngày\n"
            if item.get('price'):
                response += f"   💰 Giá: {item['price']:,} VNĐ\n"
            if item.get('destinations'):
                try:
                    dests = json.loads(item['destinations']) if isinstance(item['destinations'], str) else item['destinations']
                    if dests:
                        response += f"   📍 Điểm đến: {', '.join(dests)}\n"
                except:
                    pass
            response += "\n"
    
    if len(results) > 5:
        response += f"\n... và {len(results) - 5} kết quả khác.\n"
    
    return response

class ActionSearchDestination(Action):
    def name(self) -> Text:
        return "action_search_destination"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("\n" + "="*80)
        print("🔍 ACTION: ActionSearchDestination")
        print("="*80)
        
        destination = tracker.get_slot("destination")
        province = tracker.get_slot("province")
        region = tracker.get_slot("region")
        
        print("\n📦 SLOTS EXTRACTED:")
        print(f"   destination: '{destination}'")
        print(f"   province: '{province}'")
        print(f"   region: '{region}'")
        
        entities = tracker.latest_message.get('entities', [])
        print(f"\n🏷️  ENTITIES IN MESSAGE:")
        for entity in entities:
            print(f"   - {entity['entity']}: '{entity['value']}' (confidence: {entity.get('confidence', 'N/A')})")
        
        user_text = tracker.latest_message.get('text', '')
        print(f"\n💬 USER MESSAGE: '{user_text}'")
        
        conn = get_db_connection()
        if not conn:
            print("❌ DATABASE CONNECTION FAILED!")
            dispatcher.utter_message(text="Xin lỗi, hiện tại hệ thống đang gặp sự cố. Vui lòng thử lại sau.")
            return []
        
        print("✅ DATABASE CONNECTION OK")
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = "SELECT * FROM destinations WHERE 1=1"
            params = []
            
            if destination:
                query += " AND LOWER(name) LIKE LOWER(%s)"
                params.append(f"%{destination}%")
                print(f"\n   Added filter: name LIKE '%{destination}%'")
            
            if province:
                query += " AND LOWER(province) LIKE LOWER(%s)"
                params.append(f"%{province}%")
                print(f"   Added filter: province LIKE '%{province}%'")
            
            if region:
                query += " AND LOWER(region) LIKE LOWER(%s)"
                params.append(f"%{region}%")
                print(f"   Added filter: region LIKE '%{region}%'")
            
            query += " ORDER BY rating DESC LIMIT 10"
            
            print(f"\n🔧 SQL QUERY:")
            print(f"   {query}")
            print(f"\n📝 PARAMS:")
            print(f"   {params}")
            
            try:
                actual_query = cur.mogrify(query, params).decode('utf-8')
                print(f"\n✨ ACTUAL QUERY:")
                print(f"   {actual_query}")
            except:
                pass
            
            print(f"\n⚙️  EXECUTING QUERY...")
            cur.execute(query, params)
            results = cur.fetchall()
            
            print(f"\n📊 QUERY RESULTS:")
            print(f"   Found {len(results)} result(s)")
            
            if results:
                print(f"\n📋 RESULTS:")
                for idx, result in enumerate(results[:5], 1):
                    print(f"   {idx}. {result.get('name', 'N/A')} - {result.get('province', 'N/A')} ({result.get('category', 'N/A')})")
            else:
                print("   ⚠️  No results found!")
            
            message = format_results(results, 'destination')
            dispatcher.utter_message(text=message)
            
            print("\n✅ ACTION COMPLETED")
            print("="*80 + "\n")
            
        except Exception as e:
            print(f"\n❌ EXCEPTION: {type(e).__name__}")
            print(f"   Message: {str(e)}")
            import traceback
            traceback.print_exc()
            print("="*80 + "\n")
            
            logger.error(f"Error in ActionSearchDestination: {e}")
            dispatcher.utter_message(text="Đã xảy ra lỗi khi tìm kiếm. Vui lòng thử lại.")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
        return []

class ActionSearchDestinationFuzzy(Action):
    """Search với fuzzy matching cho tên địa điểm (xử lý typo, tên gần giống)"""
    
    def name(self) -> Text:
        return "action_search_destination_fuzzy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("\nACTION: ActionSearchDestinationFuzzy")
        
        destination = tracker.get_slot("destination")
        
        if not destination:
            dispatcher.utter_message(text="Bạn muốn tìm địa điểm nào?")
            return []
        
        conn = get_db_connection()
        if not conn:
            dispatcher.utter_message(text="Lỗi kết nối database")
            return []
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Fuzzy search using PostgreSQL similarity functions
            # enable extension pg_trgm: CREATE EXTENSION IF NOT EXISTS pg_trgm;
            query = """
                SELECT *, 
                    similarity(LOWER(name), LOWER(%s)) as sim_score
                FROM destinations 
                WHERE similarity(LOWER(name), LOWER(%s)) > 0.3
                ORDER BY sim_score DESC
                LIMIT 5
            """
            
            cur.execute(query, [destination, destination])
            results = cur.fetchall()
            
            print(f"Fuzzy search for '{destination}': found {len(results)} results")
            
            if results:
                for r in results:
                    print(f"  - {r['name']} (similarity: {r['sim_score']:.2f})")
            
            message = format_results(results, 'destination')
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            print(f"ERROR: {e}")
            query = "SELECT * FROM destinations WHERE LOWER(name) LIKE LOWER(%s) LIMIT 5"
            cur.execute(query, [f"%{destination}%"])
            results = cur.fetchall()
            message = format_results(results, 'destination')
            dispatcher.utter_message(text=message)
            
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
        return []


class ActionSearchByCity(Action):
    """Tìm TẤT CẢ địa điểm du lịch trong một thành phố"""
    
    def name(self) -> Text:
        return "action_search_by_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("\nACTION: ActionSearchByCity")
        
        province = tracker.get_slot("province")
        
        if not province:
            dispatcher.utter_message(text="Bạn muốn tìm ở thành phố nào?")
            return []
        
        conn = get_db_connection()
        if not conn:
            dispatcher.utter_message(text="Lỗi kết nối database")
            return []
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT * FROM destinations 
                WHERE LOWER(province) LIKE LOWER(%s)
                ORDER BY rating DESC
            """
            
            cur.execute(query, [f"%{province}%"])
            results = cur.fetchall()
            
            print(f"Found {len(results)} places in {province}")
            
            if not results:
                dispatcher.utter_message(text=f"Không tìm thấy địa điểm nào ở {province}")
                return []
            
            categories = {}
            for r in results:
                cat = r.get('category', 'khác')
                categories[cat] = categories.get(cat, 0) + 1
            
            response = f"Tìm thấy {len(results)} địa điểm ở {province}:\n\n"
            
            for cat, count in categories.items():
                response += f"- {cat.capitalize()}: {count} địa điểm\n"
            
            response += f"\nTop {min(5, len(results))} địa điểm được đánh giá cao nhất:\n\n"
            
            for idx, item in enumerate(results[:5], 1):
                response += f"{idx}. {item['name']}"
                if item.get('rating'):
                    response += f" ({item['rating']}/5)"
                response += f"\n   Loại: {item.get('category', 'N/A')}\n"
                if item.get('description'):
                    desc = item['description'][:80] + "..."
                    response += f"   {desc}\n"
                response += "\n"
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            dispatcher.utter_message(text="Đã xảy ra lỗi khi tìm kiếm")
            
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
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
        amenities = tracker.get_slot("amenities")
        
        if not destination:
            dispatcher.utter_message(response="utter_ask_destination")
            return []
        
        conn = get_db_connection()
        if not conn:
            dispatcher.utter_message(text="Xin lỗi, hiện tại hệ thống đang gặp sự cố. Vui lòng thử lại sau.")
            return []
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT h.* FROM hotels h
                JOIN destinations d ON h.destination_id = d.id
                WHERE LOWER(d.name) LIKE LOWER(%s)
            """
            params = [f"%{destination}%"]
            
            if star_rating:
                rating_num = int(''.join(filter(str.isdigit, str(star_rating))))
                if rating_num:
                    query += " AND h.star_rating = %s"
                    params.append(rating_num)
            
            if price_range:
                query += " AND LOWER(h.price_range) LIKE LOWER(%s)"
                params.append(f"%{price_range}%")
            
            query += " ORDER BY h.star_rating DESC, h.name LIMIT 10"
            
            cur.execute(query, params)
            results = cur.fetchall()
            
            message = format_results(results, 'hotel')
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error in ActionSearchHotel: {e}")
            dispatcher.utter_message(text="Đã xảy ra lỗi khi tìm kiếm khách sạn. Vui lòng thử lại.")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
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
        
        if not destination:
            dispatcher.utter_message(response="utter_ask_destination")
            return []
        
        conn = get_db_connection()
        if not conn:
            dispatcher.utter_message(text="Xin lỗi, hiện tại hệ thống đang gặp sự cố.")
            return []
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT r.* FROM restaurants r
                JOIN destinations d ON r.destination_id = d.id
                WHERE LOWER(d.name) LIKE LOWER(%s)
            """
            params = [f"%{destination}%"]
            
            if cuisine_type:
                query += " AND LOWER(r.cuisine_type) LIKE LOWER(%s)"
                params.append(f"%{cuisine_type}%")
            
            if price_range:
                query += " AND LOWER(r.price_range) LIKE LOWER(%s)"
                params.append(f"%{price_range}%")
            
            query += " ORDER BY r.rating DESC LIMIT 10"
            
            cur.execute(query, params)
            results = cur.fetchall()
            
            message = format_results(results, 'restaurant')
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error in ActionSearchRestaurant: {e}")
            dispatcher.utter_message(text="Đã xảy ra lỗi khi tìm kiếm nhà hàng.")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
        return []


class ActionSearchActivity(Action):
    def name(self) -> Text:
        return "action_search_activity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        activity_type = tracker.get_slot("activity_type")
        
        if not destination:
            dispatcher.utter_message(response="utter_ask_destination")
            return []
        
        conn = get_db_connection()
        if not conn:
            dispatcher.utter_message(text="Xin lỗi, hiện tại hệ thống đang gặp sự cố.")
            return []
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT a.* FROM activities a
                JOIN destinations d ON a.destination_id = d.id
                WHERE LOWER(d.name) LIKE LOWER(%s)
            """
            params = [f"%{destination}%"]
            
            if activity_type:
                query += " AND LOWER(a.type) LIKE LOWER(%s)"
                params.append(f"%{activity_type}%")
            
            query += " ORDER BY a.price ASC LIMIT 10"
            
            cur.execute(query, params)
            results = cur.fetchall()
            
            message = format_results(results, 'activity')
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error in ActionSearchActivity: {e}")
            dispatcher.utter_message(text="Đã xảy ra lỗi khi tìm kiếm hoạt động.")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
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
        if not conn:
            dispatcher.utter_message(text="Xin lỗi, hiện tại hệ thống đang gặp sự cố.")
            return []
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = "SELECT * FROM tours WHERE 1=1"
            params = []
            
            if destination:
                query += " AND destinations::text LIKE %s"
                params.append(f"%{destination}%")
            
            if duration:
                days = int(''.join(filter(str.isdigit, str(duration))))
                if days:
                    query += " AND duration_days = %s"
                    params.append(days)
            
            query += " ORDER BY price ASC LIMIT 10"
            
            cur.execute(query, params)
            results = cur.fetchall()
            
            message = format_results(results, 'tour')
            dispatcher.utter_message(text=message)
            
        except Exception as e:
            logger.error(f"Error in ActionSearchTour: {e}")
            dispatcher.utter_message(text="Đã xảy ra lỗi khi tìm kiếm tour.")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
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
            dispatcher.utter_message(response="utter_ask_destination")
            return []
        
        conn = get_db_connection()
        if not conn:
            dispatcher.utter_message(text="Xin lỗi, hiện tại hệ thống đang gặp sự cố.")
            return []
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT w.*, d.name as destination_name 
                FROM weather w
                JOIN destinations d ON w.destination_id = d.id
                WHERE LOWER(d.name) LIKE LOWER(%s)
            """
            params = [f"%{destination}%"]
            
            if month:
                month_num = int(''.join(filter(str.isdigit, str(month))))
                if month_num and 1 <= month_num <= 12:
                    query += " AND w.month = %s"
                    params.append(month_num)
            
            query += " ORDER BY w.month"
            
            cur.execute(query, params)
            results = cur.fetchall()
            
            if not results:
                dispatcher.utter_message(text=f"Xin lỗi, tôi không có thông tin thời tiết cho {destination}.")
            else:
                response = f"🌤️ Thời tiết tại {results[0]['destination_name']}:\n\n"
                for item in results:
                    response += f"📅 Tháng {item['month']}: {item['description']}\n"
                    response += f"   🌡️ Nhiệt độ trung bình: {item['avg_temp']}°C\n\n"
                
                dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error in ActionGetWeather: {e}")
            dispatcher.utter_message(text="Đã xảy ra lỗi khi lấy thông tin thời tiết.")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
        return []


class ActionGetBestTime(Action):
    def name(self) -> Text:
        return "action_get_best_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        if not destination:
            dispatcher.utter_message(response="utter_best_time_general")
            return []
        
        conn = get_db_connection()
        if not conn:
            dispatcher.utter_message(response="utter_best_time_general")
            return []
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT w.*, d.name as destination_name, d.region
                FROM weather w
                JOIN destinations d ON w.destination_id = d.id
                WHERE LOWER(d.name) LIKE LOWER(%s)
                ORDER BY w.month
            """
            
            cur.execute(query, [f"%{destination}%"])
            results = cur.fetchall()
            
            if not results:
                dispatcher.utter_message(response="utter_best_time_general")
            else:
                dest_name = results[0]['destination_name']
                region = results[0].get('region', '')
                
                good_months = []
                for item in results:
                    temp = item['avg_temp']
                    desc = item['description'].lower()
                    if 20 <= temp <= 30 and 'mưa' not in desc and 'bão' not in desc:
                        good_months.append(item['month'])
                
                if good_months:
                    months_str = ", ".join([f"tháng {m}" for m in good_months])
                    response = f"⭐ Thời điểm tốt nhất đi {dest_name}:\n\n"
                    response += f"📅 {months_str}\n\n"
                    response += "Lý do:\n"
                    response += "• Thời tiết dễ chịu (20-30°C)\n"
                    response += "• Ít mưa và bão\n"
                    response += "• Thích hợp cho các hoạt động ngoài trời\n"
                else:
                    response = f"📅 Thông tin thời tiết {dest_name} theo tháng:\n\n"
                    for item in results[:6]:
                        response += f"Tháng {item['month']}: {item['description']}, {item['avg_temp']}°C\n"
                
                dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error in ActionGetBestTime: {e}")
            dispatcher.utter_message(response="utter_best_time_general")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
        return []


class ActionGetTransportation(Action):
    def name(self) -> Text:
        return "action_get_transportation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        from_location = tracker.get_slot("from_location")
        to_location = tracker.get_slot("to_location")
        
        if not from_location:
            dispatcher.utter_message(response="utter_ask_from_location")
            return []
        
        if not to_location:
            dispatcher.utter_message(response="utter_ask_to_location")
            return []
        
        conn = get_db_connection()
        if not conn:
            dispatcher.utter_message(response="utter_transportation_vietnam")
            return []
        
        try:
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
            
            if not results:
                response = f"Xin lỗi, tôi không tìm thấy thông tin di chuyển từ {from_location} đến {to_location}.\n\n"
                dispatcher.utter_message(text=response)
                dispatcher.utter_message(response="utter_transportation_vietnam")
            else:
                response = f"🚗 Cách di chuyển từ {results[0]['from_name']} đến {results[0]['to_name']}:\n\n"
                for idx, item in enumerate(results, 1):
                    icon = {"máy bay": "✈️", "tàu hỏa": "🚄", "xe khách": "🚌", "taxi": "🚕"}.get(item['type'], "🚗")
                    response += f"{idx}. {icon} {item['type'].capitalize()}\n"
                    response += f"   ⏱️ Thời gian: ~{item['duration']}\n"
                    response += f"   💰 Giá: {item['price_range']}\n\n"
                
                dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error in ActionGetTransportation: {e}")
            dispatcher.utter_message(response="utter_transportation_vietnam")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
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
        if not conn:
            dispatcher.utter_message(text="Xin lỗi, hiện tại hệ thống đang gặp sự cố.")
            return []
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
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
            
            if not results:
                dispatcher.utter_message(text=f"Chưa có đánh giá về {destination}.")
            else:
                avg_rating = sum(r['rating'] for r in results) / len(results)
                response = f"⭐ Đánh giá về {results[0]['destination_name']}:\n"
                response += f"📊 Điểm trung bình: {avg_rating:.1f}/5 ({len(results)} đánh giá)\n\n"
                
                for idx, item in enumerate(results[:3], 1):
                    stars = "⭐" * item['rating']
                    response += f"{idx}. {stars} ({item['rating']}/5)\n"
                    if item['comment']:
                        comment = item['comment'][:100] + "..." if len(item['comment']) > 100 else item['comment']
                        response += f"   💬 {comment}\n"
                    response += "\n"
                
                dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error in ActionGetReviews: {e}")
            dispatcher.utter_message(text="Đã xảy ra lỗi khi lấy đánh giá.")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
        return []


class ActionRecommendBudget(Action):
    def name(self) -> Text:
        return "action_recommend_budget"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("\n" + "="*60)
        print("ACTION: ActionRecommendBudget")
        print("="*60)
        
        destination = tracker.get_slot("destination")
        duration = tracker.get_slot("duration")
        traveler_count = tracker.get_slot("traveler_count")
        
        print(f"Slots: destination={destination}, duration={duration}, traveler_count={traveler_count}")
        
        if not destination:
            print("ERROR: No destination provided")
            dispatcher.utter_message(text="Bạn muốn đi đâu để tôi tính ngân sách giúp bạn?")
            return []
        
        days = 3
        people = 1
        
        if duration:
            try:
                days = int(''.join(filter(str.isdigit, str(duration))))
                print(f"Extracted days: {days}")
            except Exception as e:
                print(f"Error parsing duration: {e}")
                days = 3
        
        if traveler_count:
            try:
                people = int(''.join(filter(str.isdigit, str(traveler_count))))
                print(f"Extracted people: {people}")
            except Exception as e:
                print(f"Error parsing traveler_count: {e}")
                people = 1
        
        conn = get_db_connection()
        if not conn:
            print("ERROR: Database connection failed")
            dispatcher.utter_message(response="utter_budget_ranges")
            return []
        
        print("Database connected")
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
                        
            query = """
                SELECT 
                    d.name as destination_name,
                    AVG(CASE 
                        WHEN h.price_range LIKE '%%rẻ%%' THEN 500000
                        WHEN h.price_range LIKE '%%trung bình%%' THEN 1000000
                        WHEN h.price_range LIKE '%%cao cấp%%' THEN 2500000
                        ELSE 1000000
                    END) as avg_hotel_price,
                    AVG(CASE 
                        WHEN r.price_range LIKE '%%rẻ%%' THEN 100000
                        WHEN r.price_range LIKE '%%trung bình%%' THEN 250000
                        WHEN r.price_range LIKE '%%cao cấp%%' THEN 500000
                        ELSE 200000
                    END) as avg_restaurant_price
                FROM destinations d
                LEFT JOIN hotels h ON h.destination_id = d.id
                LEFT JOIN restaurants r ON r.destination_id = d.id
                WHERE LOWER(d.name) LIKE %s
                GROUP BY d.name
            """

            param = f"%{destination.lower()}%"
            print(f"Query param: {param}")

            cur.execute(query, (param,))

            result = cur.fetchone()
            
            print(f"Query result: {result}")
            
            if not result:
                print("ERROR: No destination found in database")
                dispatcher.utter_message(text=f"Xin lỗi, tôi không tìm thấy thông tin về {destination}.")
                return []
            
            hotel_per_night = result['avg_hotel_price'] or 1000000
            food_per_day = (result['avg_restaurant_price'] or 200000) * 3
            activities_per_day = 300000
            transport = 500000
            
            print(f"Prices: hotel={hotel_per_night}, food={food_per_day}, activities={activities_per_day}")
            
            hotel_total = hotel_per_night * days
            food_total = food_per_day * days
            activities_total = activities_per_day * days
            
            per_person = (hotel_total + food_total + activities_total + transport) / people if people > 1 else (hotel_total + food_total + activities_total + transport)
            total_group = per_person * people
            
            print(f"Calculated: per_person={per_person}, total_group={total_group}")
            
            response = f"Ngân sách dự kiến cho chuyến đi {result['destination_name']}:\n\n"
            response += f"Số người: {people}\n"
            response += f"Thời gian: {days} ngày\n\n"
            response += f"Chi phí cho 1 người:\n"
            response += f"- Khách sạn: {hotel_total/people if people > 1 else hotel_total:,.0f} VNĐ ({hotel_per_night:,.0f} VNĐ/đêm)\n"
            response += f"- Ăn uống: {food_total:,.0f} VNĐ ({food_per_day:,.0f} VNĐ/ngày)\n"
            response += f"- Hoạt động: {activities_total:,.0f} VNĐ ({activities_per_day:,.0f} VNĐ/ngày)\n"
            response += f"- Di chuyển: {transport/people if people > 1 else transport:,.0f} VNĐ\n\n"
            response += f"Tổng/người: {per_person:,.0f} VNĐ\n"
            
            if people > 1:
                response += f"Tổng cả nhóm: {total_group:,.0f} VNĐ\n"
            
            response += f"\nLưu ý: Chưa bao gồm vé máy bay và mua sắm cá nhân"
            
            dispatcher.utter_message(text=response)
            
            print("SUCCESS: Budget calculated and sent")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"ERROR: Exception occurred - {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            print("="*60 + "\n")
            
            logger.error(f"Error in ActionRecommendBudget: {e}")
            dispatcher.utter_message(response="utter_budget_ranges")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
        return []
    
class ActionCompareDestinations(Action):
    def name(self) -> Text:
        return "action_compare_destinations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message.get('entities', [])
        destinations = [e['value'] for e in entities if e['entity'] == 'destination']
        
        if len(destinations) < 2:
            dispatcher.utter_message(text="Bạn muốn so sánh điểm đến nào? Vui lòng cho tôi biết 2 địa điểm.")
            return []
        
        dest1, dest2 = destinations[0], destinations[1]
        
        conn = get_db_connection()
        if not conn:
            dispatcher.utter_message(text="Xin lỗi, hiện tại hệ thống đang gặp sự cố.")
            return []
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            query = "SELECT * FROM destinations WHERE LOWER(name) LIKE LOWER(%s)"
            
            cur.execute(query, [f"%{dest1}%"])
            result1 = cur.fetchone()
            
            cur.execute(query, [f"%{dest2}%"])
            result2 = cur.fetchone()
            
            if not result1 or not result2:
                dispatcher.utter_message(text="Xin lỗi, tôi không tìm thấy thông tin về một trong hai điểm đến này.")
                return []
            
            response = f"📊 So sánh {result1['name']} vs {result2['name']}:\n\n"
            
            response += f"📍 {result1['name']}:\n"
            response += f"   • Vị trí: {result1['province']}, {result1['region']}\n"
            response += f"   • Loại: {result1['category']}\n"
            response += f"   • Đánh giá: {result1['rating']}/5\n"
            if result1.get('description'):
                desc = result1['description'][:100] + "..."
                response += f"   • Mô tả: {desc}\n"
            response += "\n"
            
            response += f"📍 {result2['name']}:\n"
            response += f"   • Vị trí: {result2['province']}, {result2['region']}\n"
            response += f"   • Loại: {result2['category']}\n"
            response += f"   • Đánh giá: {result2['rating']}/5\n"
            if result2.get('description'):
                desc = result2['description'][:100] + "..."
                response += f"   • Mô tả: {desc}\n"
            response += "\n"
            
            if result1['rating'] > result2['rating']:
                response += f"⭐ {result1['name']} có đánh giá cao hơn\n"
            elif result2['rating'] > result1['rating']:
                response += f"⭐ {result2['name']} có đánh giá cao hơn\n"
            else:
                response += f"⭐ Cả hai đều có đánh giá tương đương\n"
            
            dispatcher.utter_message(text=response)
            
        except Exception as e:
            logger.error(f"Error in ActionCompareDestinations: {e}")
            dispatcher.utter_message(text="Đã xảy ra lỗi khi so sánh.")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
        
        return []


class ActionGetTravelTips(Action):
    def name(self) -> Text:
        return "action_get_travel_tips"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        if destination:
            response = f"💡 Tips du lịch {destination}:\n\n"
            response += "• Đổi tiền tại ngân hàng hoặc ATM chính thức\n"
            response += "• Mua sim 4G tại sân bay để dùng bản đồ\n"
            response += "• Sử dụng Grab/Be thay vì taxi truyền thống\n"
            response += "• Thương lượng giá khi mua sắm ở chợ\n"
            response += "• Mang theo thuốc cá nhân và kem chống nắng\n"
            response += "• Ăn thử đặc sản địa phương\n"
            response += "• Tôn trọng văn hóa và phong tục địa phương\n"
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(response="utter_travel_tips_general")
        
        return []


class ActionGetTravelDocuments(Action):
    def name(self) -> Text:
        return "action_get_travel_documents"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_visa_info")
        return []


class ActionGetSpecialRequirements(Action):
    def name(self) -> Text:
        return "action_get_special_requirements"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        special_need = tracker.get_slot("special_need")
        diet = tracker.get_slot("diet")
        traveler_type = tracker.get_slot("traveler_type")
        
        response = "🎯 Thông tin cho nhu cầu đặc biệt:\n\n"
        
        if special_need and "khuyết tật" in str(special_need).lower():
            response += "♿ Người khuyết tật:\n"
            response += "• Chọn khách sạn có thang máy và phòng tiện nghi\n"
            response += "• Liên hệ trước với nhà hàng về khả năng tiếp cận\n"
            response += "• Sử dụng dịch vụ xe riêng thay vì phương tiện công cộng\n"
            response += "• Các điểm tham quan lớn thường có hỗ trợ\n\n"
        
        if diet and "chay" in str(diet).lower():
            response += "🥗 Người ăn chay:\n"
            response += "• Việt Nam có nhiều chùa phục vụ đồ chay\n"
            response += "• Tìm nhà hàng chay (com chay) ở mọi thành phố\n"
            response += "• Nói rõ 'ăn chay' hoặc 'không thịt cá' khi gọi món\n\n"
        
        if traveler_type:
            if "người già" in str(traveler_type).lower() or "cao tuổi" in str(traveler_type).lower():
                response += "👴👵 Người cao tuổi:\n"
                response += "• Chọn tour nhẹ nhàng, ít leo trèo\n"
                response += "• Đặt khách sạn ở vị trí thuận tiện\n"
                response += "• Mang theo thuốc thường dùng\n"
                response += "• Tránh di chuyển quá nhiều trong ngày\n\n"
            
            elif "em bé" in str(traveler_type).lower() or "trẻ em" in str(traveler_type).lower():
                response += "👶 Trẻ em:\n"
                response += "• Chọn khách sạn có kids club\n"
                response += "• Mang theo đồ chơi và sách\n"
                response += "• Lên lịch nghỉ ngơi hợp lý\n"
                response += "• Chuẩn bị đồ ăn vặt và thuốc cơ bản\n\n"
        
        if response == "🎯 Thông tin cho nhu cầu đặc biệt:\n\n":
            response = "Bạn có nhu cầu đặc biệt gì? Tôi có thể tư vấn cho người khuyết tật, người ăn chay, người cao tuổi, trẻ em..."
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetPackingList(Action):
    def name(self) -> Text:
        return "action_get_packing_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("\n" + "="*60)
        print("ACTION: ActionGetPackingList CALLED")
        print("="*60)

        destination = tracker.get_slot("destination")
        category = tracker.get_slot("category")
        season = tracker.get_slot("season")

        print(f"Slots: destination={destination}, category={category}, season={season}")

        response = "🎒 Danh sách đồ cần mang:\n\n"

        response += "📋 Đồ cơ bản:\n"
        response += "• Giấy tờ tùy thân (CMND/Passport)\n"
        response += "• Tiền mặt và thẻ ngân hàng\n"
        response += "• Điện thoại, sạc, pin dự phòng\n"
        response += "• Thuốc cá nhân\n\n"

        if category:
            if "biển" in str(category).lower():
                response += "🏖️ Đi biển:\n"
                response += "• Đồ bơi, khăn tắm\n"
                response += "• Kem chống nắng SPF50+\n"
                response += "• Mũ, kính râm\n"
                response += "• Dép đi biển\n"
                response += "• Túi chống nước cho điện thoại\n\n"
            elif "núi" in str(category).lower():
                response += "⛰️ Đi núi:\n"
                response += "• Giày trekking tốt\n"
                response += "• Áo khoác ấm (núi lạnh)\n"
                response += "• Mũ/nón chống nắng\n"
                response += "• Ba lô chắc chắn\n"
                response += "• Đèn pin/headlamp\n\n"

        if season:
            if "đông" in str(season).lower() or "lạnh" in str(season).lower():
                response += "❄️ Mùa đông:\n"
                response += "• Áo khoác dày, áo len\n"
                response += "• Khăn choàng, găng tay\n"
                response += "• Quần dài ấm\n\n"
            elif "hè" in str(season).lower() or "nóng" in str(season).lower():
                response += "☀️ Mùa hè:\n"
                response += "• Quần áo mỏng, thoáng mát\n"
                response += "• Kem chống nắng\n"
                response += "• Mũ/nón rộng vành\n\n"

        dispatcher.utter_message(text=response)

        print("✅ ActionGetPackingList executed successfully")
        print("="*60 + "\n")

        return []

class ActionGetLocalCulture(Action):
    def name(self) -> Text:
        return "action_get_local_culture"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        response = "🏛️ Văn hóa và phong tục Việt Nam:\n\n"
        
        response += "👋 Lời chào:\n"
        response += "• Chào hỏi lịch sự khi gặp người\n"
        response += "• Cúi đầu nhẹ thể hiện tôn trọng\n\n"
        
        response += "🙏 Khi vào chùa/đền:\n"
        response += "• Mặc quần áo kín đáo\n"
        response += "• Cởi giày trước khi vào\n"
        response += "• Không ồn ào, giữ yên lặng\n"
        response += "• Xin phép trước khi chụp ảnh\n\n"
        
        response += "🍜 Ăn uống:\n"
        response += "• Dùng đũa khi ăn\n"
        response += "• Có thể húp phở ầm ĩ (bình thường)\n"
        response += "• Tip không bắt buộc nhưng được hoan nghênh\n\n"
        
        response += "🎁 Quà lưu niệm:\n"
        response += "• Thương lượng giá ở chợ\n"
        response += "• Mua tại cửa hàng cố định có giá rõ ràng\n"
        response += "• Đặc sản: cà phê, trà, tranh, áo dài\n\n"
        
        if destination:
            response += f"📍 {destination} có các lễ hội và đặc sản riêng, bạn có thể hỏi người dân địa phương!"
        
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
            dispatcher.utter_message(response="utter_top_beaches")
            return []
        
        response = f"📸 Địa điểm chụp ảnh đẹp:\n\n"
        response += "💡 Tips chụp ảnh:\n"
        response += "• Golden hour: 6-8h sáng, 16-18h chiều\n"
        response += "• Tránh chụp giữa trưa (ánh sáng gắt)\n"
        response += "• Dậy sớm để tránh đông người\n"
        response += "• Xin phép trước khi chụp người dân\n\n"
        
        dest_lower = destination.lower()
        if "đà nẵng" in dest_lower:
            response += "📍 Đà Nẵng:\n"
            response += "• Cầu Vàng (Golden Bridge)\n"
            response += "• Bãi biển Mỹ Khê lúc hoàng hôn\n"
            response += "• Bán đảo Sơn Trà\n"
            response += "• Cầu Rồng (tối thứ 7, CN)\n"
        elif "hội an" in dest_lower:
            response += "📍 Hội An:\n"
            response += "• Phố cổ về đêm (đèn lồng)\n"
            response += "• Cầu Nhật Bản\n"
            response += "• Bến Thuyền An Hội\n"
            response += "• Ruộng rau Trà Quế\n"
        elif "đà lạt" in dest_lower:
            response += "📍 Đà Lạt:\n"
            response += "• Đồi chè Cầu Đất\n"
            response += "• Hồ Tuyền Lâm\n"
            response += "• Ga Đà Lạt\n"
            response += "• Đường Hầm Đất Sét\n"
        elif "sapa" in dest_lower:
            response += "📍 Sapa:\n"
            response += "• Ruộng bậc thang (mùa nước đổ)\n"
            response += "• Đỉnh Fansipan\n"
            response += "• Bản Cát Cát\n"
            response += "• Thung lũng Mường Hoa\n"
        else:
            response += f"📍 Hãy hỏi người dân địa phương về các điểm chụp ảnh đẹp tại {destination}!"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetNightlife(Action):
    def name(self) -> Text:
        return "action_get_nightlife"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        response = "🌃 Hoạt động về đêm:\n\n"
        
        dest_lower = str(destination).lower() if destination else ""
        
        if "sài gòn" in dest_lower or "hcm" in dest_lower:
            response += "📍 Sài Gòn:\n"
            response += "• Phố đi bộ Nguyễn Huệ\n"
            response += "• Bùi Viện (backpacker street)\n"
            response += "• Rooftop bars: Chill Skybar, Social Club\n"
            response += "• Chợ đêm Bến Thành\n"
        elif "hà nội" in dest_lower:
            response += "📍 Hà Nội:\n"
            response += "• Phố cổ: Tạ Hiện, Mã Mây\n"
            response += "• Hồ Gươm về đêm\n"
            response += "• Chợ đêm cuối tuần (phố cổ)\n"
            response += "• Bia hơi Tạ Hiện\n"
        elif "đà nẵng" in dest_lower:
            response += "📍 Đà Nẵng:\n"
            response += "• Chợ đêm Sơn Trà\n"
            response += "• Cầu Rồng phun lửa (T7, CN 21h)\n"
            response += "• Sky36 Bar (tầng 36 Novotel)\n"
            response += "• Đi dạo bờ biển Mỹ Khê\n"
        elif "nha trang" in dest_lower:
            response += "📍 Nha Trang:\n"
            response += "• Chợ đêm Nha Trang\n"
            response += "• Sailing Club (beach bar)\n"
            response += "• Louisiane Brewhouse\n"
            response += "• Đi dạo công viên biển\n"
        else:
            response += "🎭 Hoạt động về đêm phổ biến:\n"
            response += "• Chợ đêm địa phương\n"
            response += "• Phố đi bộ\n"
            response += "• Quán bia, cafe\n"
            response += "• Ăn vặt đường phố\n"
        
        response += "\n⚠️ Lưu ý: Giữ tài sản cẩn thận, về sớm nếu đi một mình"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetFamilyActivities(Action):
    def name(self) -> Text:
        return "action_get_family_activities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        response = "👨‍👩‍👧‍👦 Hoạt động cho gia đình:\n\n"
        
        response += "🎯 Gợi ý chung:\n"
        response += "• Công viên nước, công viên giải trí\n"
        response += "• Bảo tàng tương tác cho trẻ em\n"
        response += "• Tham quan vườn thú, thủy cung\n"
        response += "• Hoạt động ngoài trời nhẹ nhàng\n"
        response += "• Ăn tối ở nhà hàng thân thiện trẻ em\n\n"
        
        if destination:
            dest_lower = str(destination).lower()
            if "đà nẵng" in dest_lower:
                response += "📍 Đà Nẵng:\n"
                response += "• Asia Park (công viên giải trí)\n"
                response += "• Bãi biển Mỹ Khê (an toàn)\n"
                response += "• Bảo tàng Chăm\n"
            elif "nha trang" in dest_lower:
                response += "📍 Nha Trang:\n"
                response += "• Vinpearl Land\n"
                response += "• Thủy cung Trí Nguyên\n"
                response += "• Tắm biển\n"
            elif "sài gòn" in dest_lower or "hcm" in dest_lower:
                response += "📍 Sài Gòn:\n"
                response += "• Thảo Cầm Viên (Sở thú)\n"
                response += "• Dam Sen Park\n"
                response += "• KizCiti (thành phố trẻ em)\n"
        
        response += "\n💡 Tip: Lên lịch nghỉ ngơi giữa ngày cho trẻ"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetAdventureActivities(Action):
    def name(self) -> Text:
        return "action_get_adventure_activities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        response = "🏔️ Hoạt động mạo hiểm:\n\n"
        
        if destination:
            dest_lower = str(destination).lower()
            if "đà lạt" in dest_lower:
                response += "📍 Đà Lạt:\n"
                response += "• Canyoning thác Datanla\n"
                response += "• Đi xe ATV\n"
                response += "• Trekking Langbiang\n"
                response += "• Zipline rừng thông\n"
            elif "sapa" in dest_lower:
                response += "📍 Sapa:\n"
                response += "• Chinh phục Fansipan\n"
                response += "• Trekking ruộng bậc thang\n"
                response += "• Camping qua đêm\n"
            elif "nha trang" in dest_lower:
                response += "📍 Nha Trang:\n"
                response += "• Lặn biển, snorkeling\n"
                response += "• Dù lượn (parasailing)\n"
                response += "• Jet ski\n"
                response += "• Flyboard\n"
            elif "mũi né" in dest_lower:
                response += "📍 Mũi Né:\n"
                response += "• Lướt ván diều (kitesurfing)\n"
                response += "• Đi xe jeep cồn cát\n"
                response += "• Trượt cát (sandboarding)\n"
            else:
                response += f"📍 {destination}:\n"
                response += "Hỏi người dân địa phương về các hoạt động mạo hiểm\n"
        else:
            response += "🎯 Hoạt động mạo hiểm phổ biến:\n"
            response += "• Trekking, leo núi\n"
            response += "• Lặn biển, snorkeling\n"
            response += "• Dù lượn, nhảy bungee\n"
            response += "• Rafting, canyoning\n"
            response += "• Zipline\n"
        
        response += "\n⚠️ Lưu ý: Chọn công ty uy tín, kiểm tra thiết bị an toàn"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetRomanticSpots(Action):
    def name(self) -> Text:
        return "action_get_romantic_spots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        destination = tracker.get_slot("destination")
        
        response = "💑 Địa điểm lãng mạn:\n\n"
        
        response += "✨ Gợi ý chung:\n"
        response += "• Ngắm hoàng hôn/bình minh cùng nhau\n"
        response += "• Dinner trên bãi biển\n"
        response += "• Spa couple\n"
        response += "• Đi dạo buổi tối\n"
        response += "• Villa/bungalow riêng tư\n\n"
        
        if destination:
            response += f"📍 Gợi ý cho {destination}:\n"
            response += "• Resort có private beach\n"
            response += "• Nhà hàng view đẹp\n"
            response += "• Điểm ngắm cảnh lãng mạn\n"
            response += "• Hoạt động riêng tư cho 2 người\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetFoodTour(Action):
    def name(self) -> Text:
        return "action_get_food_tour"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_vietnamese_food")
        
        destination = tracker.get_slot("destination")
        if destination:
            response = f"\n📍 Đặc sản {destination}:\n"
            response += "Hãy thử các món ăn địa phương tại chợ và quán vỉa hè!"
            dispatcher.utter_message(text=response)
        
        return []


class ValidateSearchDestinationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_search_destination_form"


class ValidateSearchHotelForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_search_hotel_form"