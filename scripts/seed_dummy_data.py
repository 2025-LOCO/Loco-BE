#!/usr/bin/env python3
"""
더미 데이터 생성 스크립트
test.db에 테스트용 더미 데이터를 삽입합니다.
"""
import sys
import os
from datetime import datetime, timedelta
import random

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.core.database import engine, Base
from app.models.user import User, UserGrade
from app.models.place import Place
from app.models.route import Route
from app.models.region_province import RegionProvince
from app.models.region_city import RegionCity
from app.models.associations import FavoritePlace, FavoriteRoute, RoutePlaceMap
from app.models.votes import PlaceVote, RouteVote
from app.models.vote_enums import VoteType
from app.models.qna import Question, Answer
from app.core.security import get_password_hash


def clear_data(db: Session):
    """기존 데이터를 모두 삭제합니다."""
    print("기존 데이터를 삭제하는 중...")
    
    # 순서대로 삭제 (외래키 제약 고려)
    db.query(Answer).delete()
    db.query(Question).delete()
    db.query(PlaceVote).delete()
    db.query(RouteVote).delete()
    db.query(FavoritePlace).delete()
    db.query(FavoriteRoute).delete()
    db.query(RoutePlaceMap).delete()
    db.query(Route).delete()
    db.query(Place).delete()
    db.query(User).delete()
    db.query(RegionCity).delete()
    db.query(RegionProvince).delete()
    
    db.commit()
    print("✓ 기존 데이터 삭제 완료")


def create_regions(db: Session):
    """지역 데이터를 생성합니다."""
    print("\n지역 데이터를 생성하는 중...")
    
    provinces = [
        RegionProvince(province_id="11", kor_name="서울", eng_name="Seoul"),
        RegionProvince(province_id="26", kor_name="부산", eng_name="Busan"),
        RegionProvince(province_id="41", kor_name="경기", eng_name="Gyeonggi-do"),
        RegionProvince(province_id="43", kor_name="충북", eng_name="Chungcheongbuk-do"),
        RegionProvince(province_id="44", kor_name="충남", eng_name="Chungcheongnam-do"),
        RegionProvince(province_id="47", kor_name="경북", eng_name="Gyeongsangbuk-do"),
        RegionProvince(province_id="48", kor_name="경남", eng_name="Gyeongsangnam-do"),
        RegionProvince(province_id="50", kor_name="제주", eng_name="Jeju"),
    ]
    
    cities = [
        # 서울
        RegionCity(region_id="110000", province_id="11", kor_name="서울특별시", eng_name="Seoul"),
        RegionCity(region_id="111000", province_id="11", kor_name="종로구", eng_name="Jongno-gu"),
        RegionCity(region_id="112000", province_id="11", kor_name="강남구", eng_name="Gangnam-gu"),
        RegionCity(region_id="113000", province_id="11", kor_name="마포구", eng_name="Mapo-gu"),
        RegionCity(region_id="114000", province_id="11", kor_name="용산구", eng_name="Yongsan-gu"),
        
        # 부산
        RegionCity(region_id="260000", province_id="26", kor_name="부산광역시", eng_name="Busan"),
        RegionCity(region_id="261000", province_id="26", kor_name="해운대구", eng_name="Haeundae-gu"),
        RegionCity(region_id="262000", province_id="26", kor_name="중구", eng_name="Jung-gu"),
        
        # 경기
        RegionCity(region_id="411100", province_id="41", kor_name="수원시", eng_name="Suwon-si"),
        RegionCity(region_id="411200", province_id="41", kor_name="성남시", eng_name="Seongnam-si"),
        RegionCity(region_id="411300", province_id="41", kor_name="용인시", eng_name="Yongin-si"),
        
        # 제주
        RegionCity(region_id="500000", province_id="50", kor_name="제주특별자치도", eng_name="Jeju"),
        RegionCity(region_id="501000", province_id="50", kor_name="제주시", eng_name="Jeju-si"),
        RegionCity(region_id="502000", province_id="50", kor_name="서귀포시", eng_name="Seogwipo-si"),
    ]
    
    db.add_all(provinces)
    db.add_all(cities)
    db.commit()
    print(f"✓ 지역 데이터 생성 완료: 시/도 {len(provinces)}개, 시/군/구 {len(cities)}개")


def create_users(db: Session):
    """사용자 데이터를 생성합니다."""
    print("\n사용자 데이터를 생성하는 중...")
    
    # 비밀번호는 모두 'password123'
    hashed_pw = get_password_hash("password123")
    
    users = [
        User(
            id=1,
            email="local.suwon@example.com",
            hashed_password=hashed_pw,
            nickname="수원현지인",
            intro="수원의 모든 것을 알려드립니다!",
            city_id="411100",
            is_local=True,
            points=1250,
            grade=UserGrade.A,
            ranking=1
        ),
        User(
            id=2,
            email="traveler@example.com",
            hashed_password=hashed_pw,
            nickname="여행가",
            intro="전국을 여행하는 것을 좋아합니다.",
            city_id="110000",
            is_local=False,
            points=300,
            grade=UserGrade.C,
            ranking=15
        ),
        User(
            id=3,
            email="busan.local@example.com",
            hashed_password=hashed_pw,
            nickname="부산갈매기",
            intro="부산 맛집 전문가",
            city_id="260000",
            is_local=True,
            points=800,
            grade=UserGrade.B,
            ranking=5
        ),
        User(
            id=4,
            email="seoul.tourist@example.com",
            hashed_password=hashed_pw,
            nickname="서울탐험가",
            intro="서울의 숨겨진 명소를 찾아다닙니다",
            city_id="112000",
            is_local=True,
            points=950,
            grade=UserGrade.B,
            ranking=3
        ),
        User(
            id=5,
            email="jeju.lover@example.com",
            hashed_password=hashed_pw,
            nickname="제주도민",
            intro="제주 토박이입니다",
            city_id="501000",
            is_local=True,
            points=1500,
            grade=UserGrade.S,
            ranking=1
        ),
        User(
            id=6,
            email="newbie@example.com",
            hashed_password=hashed_pw,
            nickname="여행초보",
            intro="여행을 시작한지 얼마 안됐어요",
            city_id="411200",
            is_local=False,
            points=50,
            grade=UserGrade.C,
            ranking=None
        ),
        User(
            id=7,
            email="jecy123@naver.com",
            hashed_password=get_password_hash("locoloco"),
            nickname="수원지키미",
            intro="수원토박이가 소개합니다!",
            city_id="411100", # 수원시
            is_local=True,
            points=0,
            grade=UserGrade.C,
            ranking=None
        ),
    ]
    
    db.add_all(users)
    db.commit()
    print(f"✓ 사용자 데이터 생성 완료: {len(users)}명")
    return users


def create_places(db: Session, users):
    """장소 데이터를 생성합니다."""
    print("\n장소 데이터를 생성하는 중...")
    
    places = [
        # 수원 장소들
        Place(
            place_id=1,
            name="행궁동 벽화마을",
            type="관광지",
            is_frequent=False,
            created_by=1,
            kakao_place_id="1111",
            atmosphere="자유롭고 감성적인",
            pros="사진 찍기 좋음, 예쁜 카페 많음",
            cons="주말에 사람이 너무 많음",
            image_url="https://picsum.photos/600/400?random=1",
            count_real=15,
            count_normal=3,
            count_bad=1,
            latitude=37.2836,
            longitude=127.0166,
            intro="수원 화성 근처의 벽화 거리",
            phone="031-123-4567",
            address_name="경기도 수원시 팔달구 행궁동",
            short_location="수원시 팔달구",
            link="https://example.com/haenggung"
        ),
        Place(
            place_id=2,
            name="광교호수공원",
            type="공원",
            is_frequent=True,
            created_by=1,
            kakao_place_id="2222",
            atmosphere="자연과 함께하는",
            pros="산책로가 잘 되어있고 야경이 멋짐",
            cons="주차하기 힘듦",
            image_url="https://picsum.photos/600/400?random=2",
            count_real=25,
            count_normal=5,
            count_bad=2,
            latitude=37.2891,
            longitude=127.0641,
            intro="광교 신도시의 대표 공원",
            phone="031-228-4000",
            address_name="경기도 수원시 영통구 광교동",
            short_location="수원시 영통구",
            link="https://example.com/gwanggyo"
        ),
        Place(
            place_id=3,
            name="수원 화성",
            type="역사 유적지",
            is_frequent=False,
            created_by=1,
            kakao_place_id="3333",
            atmosphere="전통적이고 역사적인",
            pros="유네스코 세계문화유산, 교육적",
            cons="여름에 더움",
            image_url="https://picsum.photos/600/400?random=3",
            count_real=30,
            count_normal=8,
            count_bad=1,
            latitude=37.2865,
            longitude=127.0145,
            intro="조선시대 정조대왕이 건설한 성곽",
            phone="031-290-3600",
            address_name="경기도 수원시 장안구 연무동",
            short_location="수원시 장안구",
            link="https://example.com/hwaseong"
        ),
        
        # 부산 장소들
        Place(
            place_id=4,
            name="해운대 해수욕장",
            type="해변",
            is_frequent=False,
            created_by=3,
            kakao_place_id="4444",
            atmosphere="활기차고 신나는",
            pros="여름에 놀기 좋음, 야경이 멋짐",
            cons="물가가 비쌈, 여름에 사람이 너무 많음",
            image_url="https://picsum.photos/600/400?random=4",
            count_real=50,
            count_normal=10,
            count_bad=3,
            latitude=35.1587,
            longitude=129.1604,
            intro="부산의 대표 해수욕장",
            phone="051-749-5700",
            address_name="부산광역시 해운대구 우동",
            short_location="해운대구",
            link="https://example.com/haeundae"
        ),
        Place(
            place_id=5,
            name="광안리 해변",
            type="해변",
            is_frequent=True,
            created_by=3,
            kakao_place_id="5555",
            atmosphere="로맨틱하고 감성적인",
            pros="광안대교 야경이 멋짐, 회센터 많음",
            cons="주차 어려움",
            image_url="https://picsum.photos/600/400?random=5",
            count_real=40,
            count_normal=7,
            count_bad=2,
            latitude=35.1532,
            longitude=129.1189,
            intro="광안대교가 보이는 해변",
            phone="051-610-4111",
            address_name="부산광역시 수영구 광안동",
            short_location="수영구",
            link="https://example.com/gwangalli"
        ),
        Place(
            place_id=6,
            name="감천문화마을",
            type="관광지",
            is_frequent=False,
            created_by=3,
            kakao_place_id="6666",
            atmosphere="예술적이고 감성적인",
            pros="사진 찍기 좋음, 독특한 분위기",
            cons="경사가 심함, 주민들 배려 필요",
            image_url="https://picsum.photos/600/400?random=6",
            count_real=35,
            count_normal=6,
            count_bad=1,
            latitude=35.0976,
            longitude=129.0104,
            intro="부산의 산토리니",
            phone="051-204-1444",
            address_name="부산광역시 사하구 감천동",
            short_location="사하구",
            link="https://example.com/gamcheon"
        ),
        
        # 서울 장소들
        Place(
            place_id=7,
            name="경복궁",
            type="역사 유적지",
            is_frequent=False,
            created_by=4,
            kakao_place_id="7777",
            atmosphere="전통적이고 웅장한",
            pros="경복궁 수문장 교대식, 한복 대여 할인",
            cons="관광객이 많음",
            image_url="https://picsum.photos/600/400?random=7",
            count_real=45,
            count_normal=8,
            count_bad=2,
            latitude=37.5788,
            longitude=126.9770,
            intro="조선 왕조의 정궁",
            phone="02-3700-3900",
            address_name="서울특별시 종로구 사직로 161",
            short_location="종로구",
            link="https://example.com/gyeongbokgung"
        ),
        Place(
            place_id=8,
            name="홍대 거리",
            type="번화가",
            is_frequent=True,
            created_by=4,
            kakao_place_id="8888",
            atmosphere="자유롭고 활기찬",
            pros="다양한 음식점, 클럽, 버스킹",
            cons="시끄럽고 복잡함",
            image_url="https://picsum.photos/600/400?random=8",
            count_real=38,
            count_normal=12,
            count_bad=5,
            latitude=37.5563,
            longitude=126.9236,
            intro="젊음의 거리",
            phone=None,
            address_name="서울특별시 마포구 서교동",
            short_location="마포구",
            link="https://example.com/hongdae"
        ),
        Place(
            place_id=9,
            name="남산타워",
            type="관광지",
            is_frequent=False,
            created_by=4,
            kakao_place_id="9999",
            atmosphere="로맨틱하고 아름다운",
            pros="서울 전망, 야경이 멋짐",
            cons="입장료가 비쌈, 케이블카 대기 시간 길음",
            image_url="https://picsum.photos/600/400?random=9",
            count_real=42,
            count_normal=10,
            count_bad=3,
            latitude=37.5512,
            longitude=126.9882,
            intro="서울의 상징",
            phone="02-3455-9277",
            address_name="서울특별시 용산구 남산공원길 105",
            short_location="용산구",
            link="https://example.com/namsantower"
        ),
        
        # 제주 장소들
        Place(
            place_id=10,
            name="성산일출봉",
            type="자연 명소",
            is_frequent=False,
            created_by=5,
            kakao_place_id="10001",
            atmosphere="웅장하고 신비로운",
            pros="일출이 아름다움, 유네스코 세계자연유산",
            cons="계단이 많아 체력 필요",
            image_url="https://picsum.photos/600/400?random=10",
            count_real=55,
            count_normal=5,
            count_bad=1,
            latitude=33.4598,
            longitude=126.9426,
            intro="제주 동쪽의 화산 분화구",
            phone="064-783-0959",
            address_name="제주특별자치도 서귀포시 성산읍",
            short_location="서귀포시",
            link="https://example.com/seongsan"
        ),
        Place(
            place_id=11,
            name="한라산 국립공원",
            type="자연 명소",
            is_frequent=True,
            created_by=5,
            kakao_place_id="10002",
            atmosphere="자연과 함께하는",
            pros="등산 코스 다양, 자연 경관 우수",
            cons="날씨 변화 심함, 체력 필요",
            image_url="https://picsum.photos/600/400?random=11",
            count_real=48,
            count_normal=8,
            count_bad=2,
            latitude=33.3617,
            longitude=126.5292,
            intro="제주도 중앙의 명산",
            phone="064-713-9950",
            address_name="제주특별자치도 제주시 해안동",
            short_location="제주시",
            link="https://example.com/hallasan"
        ),
        Place(
            place_id=12,
            name="애월 카페거리",
            type="카페거리",
            is_frequent=True,
            created_by=5,
            kakao_place_id="10003",
            atmosphere="감성적이고 여유로운",
            pros="오션뷰 카페 많음, 사진 찍기 좋음",
            cons="가격이 비쌈",
            image_url="https://picsum.photos/600/400?random=12",
            count_real=60,
            count_normal=15,
            count_bad=5,
            latitude=33.4648,
            longitude=126.3186,
            intro="제주 서쪽 해안의 카페 명소",
            phone=None,
            address_name="제주특별자치도 제주시 애월읍",
            short_location="제주시 애월",
            link="https://example.com/aewol"
        ),
    ]
    
    db.add_all(places)
    db.commit()
    print(f"✓ 장소 데이터 생성 완료: {len(places)}개")
    return places


def create_routes(db: Session, users):
    """여행 루트 데이터를 생성합니다."""
    print("\n여행 루트 데이터를 생성하는 중...")
    
    now = datetime.now()
    
    routes = [
        Route(
            route_id=1,
            name="수원 화성 당일치기 감성코스",
            intro="수원의 역사와 감성을 느낄 수 있는 코스",
            location="경기도 수원시",
            is_recommend=True,
            created_by=1,
            image_url="https://picsum.photos/800/600?random=101",
            count_real=20,
            count_soso=5,
            count_bad=1,
            created_at=now - timedelta(days=10),
            tag_period=1,  # 당일
            tag_env="city",
            tag_with="friend",
            tag_move="walk",
            tag_atmosphere="다채로운 경험",
            tag_place_count=3
        ),
        Route(
            route_id=2,
            name="부산 해변 맛집 탐방",
            intro="부산 바다를 보며 즐기는 맛집 투어",
            location="부산광역시",
            is_recommend=True,
            created_by=3,
            image_url="https://picsum.photos/800/600?random=102",
            count_real=35,
            count_soso=8,
            count_bad=2,
            created_at=now - timedelta(days=8),
            tag_period=2,  # 1박 2일
            tag_env="sea",
            tag_with="love",
            tag_move="public",
            tag_atmosphere="맛있는 여행",
            tag_place_count=4
        ),
        Route(
            route_id=3,
            name="서울 궁궐 투어",
            intro="서울의 역사를 느낄 수 있는 궁궐 탐방",
            location="서울특별시",
            is_recommend=True,
            created_by=4,
            image_url="https://picsum.photos/800/600?random=103",
            count_real=28,
            count_soso=6,
            count_bad=1,
            created_at=now - timedelta(days=5),
            tag_period=1,
            tag_env="city",
            tag_with="family",
            tag_move="public",
            tag_atmosphere="다채로운 경험",
            tag_place_count=3
        ),
        Route(
            route_id=4,
            name="제주 동부 일주",
            intro="제주 동쪽의 아름다운 자연을 만나는 코스",
            location="제주특별자치도",
            is_recommend=True,
            created_by=5,
            image_url="https://picsum.photos/800/600?random=104",
            count_real=45,
            count_soso=10,
            count_bad=3,
            created_at=now - timedelta(days=3),
            tag_period=3,  # 2박 3일
            tag_env="sea",
            tag_with="friend",
            tag_move="car",
            tag_atmosphere="잔잔하고 조용한",
            tag_place_count=5
        ),
        Route(
            route_id=5,
            name="홍대 핫플레이스 탐방",
            intro="홍대의 핫한 장소들을 둘러보는 코스",
            location="서울 마포구",
            is_recommend=False,
            created_by=2,
            image_url="https://picsum.photos/800/600?random=105",
            count_real=18,
            count_soso=7,
            count_bad=4,
            created_at=now - timedelta(days=2),
            tag_period=1,
            tag_env="city",
            tag_with="friend",
            tag_move="walk",
            tag_atmosphere="신나는 액티비티",
            tag_place_count=2
        ),
        Route(
            route_id=6,
            name="제주 카페 투어",
            intro="제주의 감성 카페들을 방문하는 코스",
            location="제주시 애월",
            is_recommend=False,
            created_by=6,
            image_url="https://picsum.photos/800/600?random=106",
            count_real=25,
            count_soso=12,
            count_bad=5,
            created_at=now - timedelta(days=1),
            tag_period=2,
            tag_env="sea",
            tag_with="love",
            tag_move="car",
            tag_atmosphere="아늑하고 로맨틱한",
            tag_place_count=3
        ),
    ]
    
    db.add_all(routes)
    db.commit()
    print(f"✓ 여행 루트 데이터 생성 완료: {len(routes)}개")
    return routes


def create_route_place_maps(db: Session, routes, places):
    """루트-장소 매핑 데이터를 생성합니다."""
    print("\n루트-장소 매핑 데이터를 생성하는 중...")
    
    # 장소 ID로 빠르게 찾기 위한 딕셔너리
    place_dict = {p.place_id: p for p in places}
    
    mappings = [
        # 루트 1: 수원 화성 당일치기 (1, 2, 3번 장소)
        RoutePlaceMap(route_id=1, place_id=3, order=1, memo="먼저 화성 둘러보기", transportation="도보"),
        RoutePlaceMap(route_id=1, place_id=1, order=2, memo="벽화마을에서 사진 찍기", transportation="도보"),
        RoutePlaceMap(route_id=1, place_id=2, order=3, memo="저녁에 호수공원 산책", transportation="버스"),
        
        # 루트 2: 부산 해변 맛집 탐방 (4, 5, 6번 장소)
        RoutePlaceMap(route_id=2, place_id=4, order=1, memo="해운대에서 아침 산책", transportation=None),
        RoutePlaceMap(route_id=2, place_id=5, order=2, memo="광안리 회센터에서 점심", transportation="지하철"),
        RoutePlaceMap(route_id=2, place_id=6, order=3, memo="감천문화마을 구경", transportation="버스"),
        RoutePlaceMap(route_id=2, place_id=5, order=4, memo="광안대교 야경 보기", transportation="버스"),
        
        # 루트 3: 서울 궁궐 투어 (7, 9번 장소)
        RoutePlaceMap(route_id=3, place_id=7, order=1, memo="경복궁 관람", transportation=None),
        RoutePlaceMap(route_id=3, place_id=9, order=2, memo="남산타워에서 서울 야경", transportation="지하철"),
        
        # 루트 4: 제주 동부 일주 (10, 11번 장소)
        RoutePlaceMap(route_id=4, place_id=10, order=1, memo="일출봉에서 일출 보기", transportation=None),
        RoutePlaceMap(route_id=4, place_id=11, order=2, memo="한라산 등산", transportation="렌터카"),
        
        # 루트 5: 홍대 핫플레이스 (8번 장소)
        RoutePlaceMap(route_id=5, place_id=8, order=1, memo="홍대 거리 구경", transportation=None),
        
        # 루트 6: 제주 카페 투어 (12번 장소)
        RoutePlaceMap(route_id=6, place_id=12, order=1, memo="애월 카페거리 투어", transportation=None),
    ]
    
    db.add_all(mappings)
    db.commit()
    print(f"✓ 루트-장소 매핑 데이터 생성 완료: {len(mappings)}개")


def create_favorites(db: Session, users, places, routes):
    """즐겨찾기 데이터를 생성합니다."""
    print("\n즐겨찾기 데이터를 생성하는 중...")
    
    favorite_places = [
        # 사용자 2 (여행가)의 즐겨찾기
        FavoritePlace(user_id=2, place_id=1, is_certificated=False),
        FavoritePlace(user_id=2, place_id=4, is_certificated=True, certificate_img_url="https://picsum.photos/400/300?random=201"),
        FavoritePlace(user_id=2, place_id=7, is_certificated=True, certificate_img_url="https://picsum.photos/400/300?random=202"),
        
        # 사용자 6 (여행초보)의 즐겨찾기
        FavoritePlace(user_id=6, place_id=8, is_certificated=False),
        FavoritePlace(user_id=6, place_id=12, is_certificated=False),
        
        # 사용자 3 (부산갈매기)의 즐겨찾기
        FavoritePlace(user_id=3, place_id=4, is_certificated=True, certificate_img_url="https://picsum.photos/400/300?random=203"),
        FavoritePlace(user_id=3, place_id=5, is_certificated=True, certificate_img_url="https://picsum.photos/400/300?random=204"),
    ]
    
    favorite_routes = [
        # 사용자들의 루트 즐겨찾기
        FavoriteRoute(user_id=2, route_id=1),
        FavoriteRoute(user_id=2, route_id=3),
        FavoriteRoute(user_id=6, route_id=4),
        FavoriteRoute(user_id=6, route_id=6),
        FavoriteRoute(user_id=3, route_id=2),
        FavoriteRoute(user_id=4, route_id=3),
    ]
    
    db.add_all(favorite_places)
    db.add_all(favorite_routes)
    db.commit()
    print(f"✓ 즐겨찾기 데이터 생성 완료: 장소 {len(favorite_places)}개, 루트 {len(favorite_routes)}개")


def create_votes(db: Session, users, places, routes):
    """투표 데이터를 생성합니다."""
    print("\n투표 데이터를 생성하는 중...")
    
    place_votes = []
    route_votes = []
    
    # 장소 투표 생성 (각 사용자가 한 번만 투표)
    place_vote_data = [
        (1, {1: VoteType.real, 2: VoteType.real, 3: VoteType.normal, 4: VoteType.real, 5: VoteType.real, 6: VoteType.bad}),
        (2, {1: VoteType.real, 2: VoteType.real, 3: VoteType.real, 4: VoteType.normal, 5: VoteType.real, 6: VoteType.normal}),
        (3, {1: VoteType.real, 2: VoteType.real, 3: VoteType.real, 4: VoteType.real, 5: VoteType.normal, 6: VoteType.real}),
        (4, {1: VoteType.real, 2: VoteType.real, 3: VoteType.real, 4: VoteType.real, 5: VoteType.real, 6: VoteType.normal}),
        (5, {1: VoteType.real, 2: VoteType.real, 3: VoteType.normal, 4: VoteType.real, 5: VoteType.real}),
        (6, {2: VoteType.real, 3: VoteType.real, 4: VoteType.bad, 5: VoteType.normal}),
        (7, {1: VoteType.real, 2: VoteType.real, 3: VoteType.real, 4: VoteType.real, 5: VoteType.real, 6: VoteType.bad}),
        (8, {1: VoteType.normal, 2: VoteType.bad, 3: VoteType.real, 4: VoteType.normal, 5: VoteType.real, 6: VoteType.bad}),
        (9, {1: VoteType.real, 2: VoteType.real, 3: VoteType.normal, 4: VoteType.real, 5: VoteType.real, 6: VoteType.bad}),
        (10, {1: VoteType.real, 2: VoteType.real, 3: VoteType.real, 4: VoteType.real, 5: VoteType.real, 6: VoteType.real}),
        (11, {1: VoteType.real, 2: VoteType.normal, 3: VoteType.real, 4: VoteType.real, 5: VoteType.real, 6: VoteType.normal}),
        (12, {1: VoteType.real, 2: VoteType.real, 3: VoteType.bad, 4: VoteType.normal, 5: VoteType.real, 6: VoteType.normal}),
    ]
    
    for place_id, user_votes in place_vote_data:
        for user_id, vote_type in user_votes.items():
            place_votes.append(PlaceVote(user_id=user_id, place_id=place_id, vote_type=vote_type))
    
    # 루트 투표 생성
    route_vote_data = [
        (1, {1: VoteType.real, 2: VoteType.real, 3: VoteType.normal, 4: VoteType.real, 5: VoteType.real, 6: VoteType.bad}),
        (2, {1: VoteType.real, 2: VoteType.real, 3: VoteType.real, 4: VoteType.normal, 5: VoteType.real, 6: VoteType.normal}),
        (3, {1: VoteType.real, 2: VoteType.real, 3: VoteType.normal, 4: VoteType.real, 5: VoteType.real, 6: VoteType.real}),
        (4, {1: VoteType.real, 2: VoteType.real, 3: VoteType.real, 4: VoteType.normal, 5: VoteType.real, 6: VoteType.bad}),
        (5, {1: VoteType.normal, 2: VoteType.real, 3: VoteType.bad, 4: VoteType.normal, 5: VoteType.bad, 6: VoteType.real}),
        (6, {1: VoteType.real, 2: VoteType.normal, 3: VoteType.bad, 4: VoteType.normal, 5: VoteType.real, 6: VoteType.bad}),
    ]
    
    for route_id, user_votes in route_vote_data:
        for user_id, vote_type in user_votes.items():
            route_votes.append(RouteVote(user_id=user_id, route_id=route_id, vote_type=vote_type))
    
    db.add_all(place_votes)
    db.add_all(route_votes)
    db.commit()
    print(f"✓ 투표 데이터 생성 완료: 장소 {len(place_votes)}개, 루트 {len(route_votes)}개")


def create_qna(db: Session, users):
    """Q&A 데이터를 생성합니다."""
    print("\nQ&A 데이터를 생성하는 중...")
    
    questions = [
        Question(
            question_id=1,
            user_id=2,
            title="수원 화성 방문 시 주의할 점이 있나요?",
            content="다음 주에 수원 화성을 방문하려고 하는데, 현지인분들께서 알려주실 팁이나 주의사항이 있을까요?",
            view_count=45,
            answer_count=2,
            created_at=datetime.now() - timedelta(days=5)
        ),
        Question(
            question_id=2,
            user_id=6,
            title="부산 해운대 주차장 추천 부탁드립니다",
            content="해운대에 차를 가지고 가려고 하는데, 주차하기 좋은 곳 추천해주세요!",
            view_count=32,
            answer_count=1,
            created_at=datetime.now() - timedelta(days=3)
        ),
        Question(
            question_id=3,
            user_id=2,
            title="제주도 렌터카 필수인가요?",
            content="제주도 여행 계획 중인데, 렌터카 없이 대중교통으로 다니기 힘들까요?",
            view_count=78,
            answer_count=3,
            created_at=datetime.now() - timedelta(days=7)
        ),
        Question(
            question_id=4,
            user_id=6,
            title="홍대에서 저렴한 맛집 추천해주세요",
            content="대학생이라 예산이 빠듯한데, 홍대 근처에서 가성비 좋은 맛집 알려주세요!",
            view_count=56,
            answer_count=2,
            created_at=datetime.now() - timedelta(days=2)
        ),
    ]
    
    answers = [
        # 질문 1에 대한 답변들
        Answer(
            answer_id=1,
            user_id=1,
            question_id=1,
            content="화성은 생각보다 넓어서 천천히 둘러보시면 3-4시간 정도 걸립니다. 편한 신발 꼭 신으시고, 여름에는 물 챙겨가세요. 행궁동 쪽에 맛집도 많으니 점심 시간 고려해서 계획 짜시면 좋아요!",
            vote_type=VoteType.real,
            created_at=datetime.now() - timedelta(days=4)
        ),
        Answer(
            answer_id=2,
            user_id=4,
            question_id=1,
            content="저도 최근에 다녀왔는데 정말 좋았어요. 화성행궁 앞에서 수원 화성 투어 가이드 신청하시면 더 알차게 둘러볼 수 있습니다!",
            vote_type=VoteType.real,
            created_at=datetime.now() - timedelta(days=4, hours=5)
        ),
        
        # 질문 2에 대한 답변
        Answer(
            answer_id=3,
            user_id=3,
            question_id=2,
            content="해운대 시장 지하주차장이나 해운대 비치 아파트 주차장을 이용하시면 됩니다. 주말에는 일찍 가셔야 자리가 있어요. 아니면 지하철 이용하시는 게 더 편할 수도 있습니다.",
            vote_type=VoteType.normal,
            created_at=datetime.now() - timedelta(days=2)
        ),
        
        # 질문 3에 대한 답변들
        Answer(
            answer_id=4,
            user_id=5,
            question_id=3,
            content="제주도는 렌터카가 거의 필수입니다. 대중교통이 있긴 하지만 배차 간격이 길고, 가고 싶은 곳을 자유롭게 다니기 어렵습니다. 렌터카 빌리시는 걸 강력 추천드려요!",
            vote_type=VoteType.real,
            created_at=datetime.now() - timedelta(days=6)
        ),
        Answer(
            answer_id=5,
            user_id=3,
            question_id=3,
            content="저는 버스 타고 다녔는데 생각보다 괜찮았어요. 다만 시간 여유가 있으셔야 하고, 계획을 잘 짜셔야 합니다.",
            vote_type=VoteType.normal,
            created_at=datetime.now() - timedelta(days=6, hours=3)
        ),
        Answer(
            answer_id=6,
            user_id=2,
            question_id=3,
            content="일정이 빡빡하시면 렌터카 추천드리고, 여유있게 관광지 위주로만 다니신다면 택시나 버스 이용도 괜찮습니다.",
            vote_type=VoteType.normal,
            created_at=datetime.now() - timedelta(days=5, hours=10)
        ),
        
        # 질문 4에 대한 답변들
        Answer(
            answer_id=7,
            user_id=4,
            question_id=4,
            content="홍대입구역 근처 '국밥집'이랑 '통닭집' 추천드립니다. 양도 많고 가격도 저렴해요. 그리고 '순대국집'도 괜찮아요!",
            vote_type=VoteType.real,
            created_at=datetime.now() - timedelta(days=1)
        ),
        Answer(
            answer_id=8,
            user_id=1,
            question_id=4,
            content="홍대 뒷골목에 있는 작은 식당들이 가성비 좋아요. 특히 점심 시간에 가면 세트 메뉴가 저렴합니다.",
            vote_type=VoteType.bad,
            created_at=datetime.now() - timedelta(days=1, hours=3)
        ),
    ]
    
    db.add_all(questions)
    db.add_all(answers)
    db.commit()
    print(f"✓ Q&A 데이터 생성 완료: 질문 {len(questions)}개, 답변 {len(answers)}개")


def main():
    """메인 함수"""
    print("=" * 60)
    print("Loco-BE 더미 데이터 생성 스크립트")
    print("=" * 60)
    
    # 테이블 생성
    print("\n데이터베이스 테이블을 확인하는 중...")
    Base.metadata.create_all(bind=engine)
    print("✓ 데이터베이스 테이블 확인 완료")
    
    # 세션 생성
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # 기존 데이터 삭제
        clear_data(db)
        
        # 데이터 생성
        create_regions(db)
        users = create_users(db)
        places = create_places(db, users)
        routes = create_routes(db, users)
        create_route_place_maps(db, routes, places)
        create_favorites(db, users, places, routes)
        create_votes(db, users, places, routes)
        create_qna(db, users)
        
        print("\n" + "=" * 60)
        print("✓ 모든 더미 데이터 생성 완료!")
        print("=" * 60)
        print("\n테스트 계정 정보:")
        print("  Email: local.suwon@example.com")
        print("  Password: password123")
        print("\n  다른 사용자들도 동일한 비밀번호(password123)를 사용합니다.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

