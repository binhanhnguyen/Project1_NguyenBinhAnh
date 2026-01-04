import re
import requests
import time
from typing import Tuple, Optional, List, Dict

# --- CẤU HÌNH ---
BACHKHOA_BBOX = {
    'north': 21.0110,
    'south': 21.0020,
    'east': 105.8530,
    'west': 105.8400
}

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

# --- DỮ LIỆU ĐỊA ĐIỂM (Đã cập nhật chuẩn xác) ---
# Format: "tên_viết_thường": (latitude, longitude)
COMMON_LOCATIONS = {
    # --- KHU GIẢNG ĐƯỜNG C ---
    "c1": (21.0070715, 105.8425561),      # Bộ môn C1-226
    "nhà c1": (21.0070715, 105.8425561),
    "c2": (21.0064474, 105.8423066),      # Hội trường C2
    "nhà c2": (21.0064474, 105.8423066),
    "c3": (21.0066214, 105.8439327),
    "nhà c3": (21.0066214, 105.8439327),
    "c7": (21.0052757, 105.8451778),      # Cụm C4-C10
    "nhà c7": (21.0052757, 105.8451778),
    
    # --- KHU GIẢNG ĐƯỜNG D ---
    "d3": (21.0047785, 105.8447491),
    "nhà d3": (21.0047785, 105.8447491),
    "d3-5": (21.0046330, 105.8452138),    # Nối giữa D3 và D5
    "d5": (21.0046330, 105.8452138),
    "d6": (21.0043525, 105.8426955),
    "nhà d6": (21.0043525, 105.8426955),
    "d7": (21.0040340, 105.8448670),      # Viện Đào tạo Quốc tế SIE
    "sie": (21.0040340, 105.8448670),
    "d8": (21.0039763, 105.8426704),
    "nhà d8": (21.0039763, 105.8426704),
    "d9": (21.0037956, 105.8444671),
    "nhà d9": (21.0037956, 105.8444671),

    # --- THƯ VIỆN & TRUNG TÂM ---
    "thư viện": (21.0044106, 105.8439888),
    "tqb": (21.0044106, 105.8439888),
    "thư viện tạ quang bửu": (21.0044106, 105.8439888),
    "hồ tiền": (21.0040519, 105.8434327),
    
    # --- KHU VỰC KHÁC ---
    "b1": (21.0044157, 105.8465901),
    "nhà b1": (21.0044157, 105.8465901),
    "ktx": (21.0049406, 105.8469539),     # Cổng KTX đường Tạ Quang Bửu
    "ký túc xá": (21.0049406, 105.8469539),
    "sân vận động": (21.0021875, 105.8478125),
    "sân bóng": (21.0021875, 105.8478125),
    "nhà thi đấu": (21.0035324, 105.8470866),
    "nhà t": (21.0035661, 105.8489794),   # Khu nhà T
    "trung tâm": (21.0035661, 105.8489794),
    "tc": (21.0025178, 105.8470152),      # Tòa Tại chức
    "tại chức": (21.0025178, 105.8470152),

    # --- CÁC CỔNG TRƯỜNG ---
    "cổng đại cồ việt": (21.007350, 105.843150),
    "cổng chính": (21.007350, 105.843150),
    "cổng parabol": (21.001650, 105.841850), # Cổng Giải Phóng
    "cổng giải phóng": (21.001650, 105.841850),
    "cổng trần đại nghĩa": (21.004850, 105.849350), # Cổng sang KTX
    "cổng tạ quang bửu": (21.002500, 105.845000), # Cổng phía sau D9

    # --- ĐẠI HỌC KINH TẾ QUỐC DÂN (NEU) ---
    "cổng neu giải phóng": (21.000094, 105.842499),
    "cổng neu trần đại nghĩa": (20.999125, 105.845597),
    "cổng ktx neu": (20.999353, 105.846564),

    # --- ĐẠI HỌC XÂY DỰNG HÀ NỘI (HUCE) ---
    "cổng huce giải phóng": (21.003314, 105.843321),
    "cổng huce trần đại nghĩa": (21.003029, 105.844619),

    # --- TIỆN ÍCH KHÁC ---
    "sân bóng": (21.005000, 105.846000),
    "bể bơi": (21.003418, 105.847198),
    "quảng trường c1": (21.006800, 105.842800),
    "cây xăng bách khoa": (21.001977, 105.849331),
    "cây xăng": (21.001977, 105.849331),
    "cây xăng giải phóng": (21.001800, 105.841500),
}

# --- CÁC HÀM HỖ TRỢ ---

def is_coordinate_string(input_str: str) -> bool:
    pattern = r'^-?\d+\.?\d*\s*,\s*-?\d+\.?\d*$'
    return bool(re.match(pattern, input_str.strip()))

def parse_coordinates(coord_str: str) -> Tuple[float, float]:
    parts = coord_str.strip().split(',')
    lat = float(parts[0].strip())
    lon = float(parts[1].strip())
    return lat, lon

def is_in_bachkhoa_area(lat: float, lon: float) -> bool:
    """Kiểm tra xem tọa độ có nằm trong vùng Bách Khoa không"""
    return (BACHKHOA_BBOX['south'] <= lat <= BACHKHOA_BBOX['north'] and
            BACHKHOA_BBOX['west'] <= lon <= BACHKHOA_BBOX['east'])

# --- CÁC HÀM GỌI API ---

def search_osm_overpass(query: str, retries: int = 2) -> List[Dict]:
    bbox = f"{BACHKHOA_BBOX['south']},{BACHKHOA_BBOX['west']},{BACHKHOA_BBOX['north']},{BACHKHOA_BBOX['east']}"
    # Tìm node và way, không phân biệt hoa thường
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["name"~"{query}",i]({bbox});
      way["name"~"{query}",i]({bbox});
    );
    out center;
    """
    
    for url in OVERPASS_URLS:
        for attempt in range(retries):
            try:
                response = requests.post(url, data=overpass_query, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    results = []
                    for el in data.get('elements', []):
                        lat = el.get('lat') or el.get('center', {}).get('lat')
                        lon = el.get('lon') or el.get('center', {}).get('lon')
                        if lat and lon:
                            results.append({'lat': lat, 'lon': lon, 'name': el.get('tags', {}).get('name')})
                    return results
            except Exception:
                pass 
    return []

def geocode_with_nominatim_fallback(address: str) -> Tuple[Optional[float], Optional[float]]:
    try:
        from geopy.geocoders import Nominatim
        geocoder = Nominatim(user_agent="bachkhoa_pathfinding_app_v3")
        
        # Tìm rộng trong HN rồi lọc lại
        location = geocoder.geocode(
            f"{address}, Hai Bà Trưng, Hà Nội",
            timeout=5
        )
        if location:
            # Lọc: Chỉ lấy kết quả nằm trong vùng Bách Khoa
            if is_in_bachkhoa_area(location.latitude, location.longitude):
                return location.latitude, location.longitude
            else:
                print(f"  Warning: Tìm thấy '{address}' nhưng nằm ngoài vùng BK.")
    except Exception as e:
        print(f"  Nominatim error: {e}")
    return None, None

# --- HÀM CHÍNH (LOGIC TỐI ƯU) ---

def get_location_with_fallback(input_str: str) -> Tuple[float, float]:
    input_str = input_str.strip()
    input_lower = input_str.lower()
    
    print(f"Đang xử lý địa điểm: '{input_str}'")

    # 1. Check Tọa độ (Nhanh nhất)
    if is_coordinate_string(input_str):
        print("  -> Phát hiện định dạng tọa độ.")
        return parse_coordinates(input_str)

    # 2. Check Từ điển có sẵn (Chính xác nhất cho tên tòa nhà)
    if input_lower in COMMON_LOCATIONS:
        print(f"  -> Tìm thấy trong dữ liệu mẫu (Chính xác).")
        return COMMON_LOCATIONS[input_lower]
    
    # Tìm gần đúng trong từ điển (ví dụ: 'đến nhà b1' -> 'b1')
    for key, coords in COMMON_LOCATIONS.items():
        if key in input_lower: 
            print(f"  -> Tìm thấy trong dữ liệu mẫu (Gần đúng: {key}).")
            return coords

    # 3. Check OSM Overpass (Gọi API)
    print("  -> Không có dữ liệu mẫu, đang tìm trên OSM...")
    results = search_osm_overpass(input_str)
    if results:
        print(f"  -> Tìm thấy trên OSM: {results[0].get('name')}")
        return results[0]['lat'], results[0]['lon']

    # 4. Check Nominatim (Fallback cuối cùng)
    print("  -> OSM không thấy, thử Nominatim...")
    lat, lon = geocode_with_nominatim_fallback(input_str)
    if lat and lon:
        print("  -> Tìm thấy trên Nominatim.")
        return lat, lon

    # Nếu tất cả đều thua
    raise ValueError(f"Không tìm thấy địa điểm: '{input_str}'. Vui lòng thử tên khác hoặc nhập tọa độ.")

# Test nhanh
if __name__ == "__main__":
  try:
        # Thử test địa điểm bạn vừa sửa
        lat, lon = get_location_with_fallback("Thư viện")
        print(f"Test Thư viện: {lat}, {lon}")
  except Exception as e:
        print(e)
