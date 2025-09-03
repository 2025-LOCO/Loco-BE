-- scripts/seed.sql
-- 초기 데이터 삽입 스크립트 (DB 스키마 정합성 보장 버전)
-- 여러 번 실행해도 에러 없이 동일 상태가 되도록 설계 (idempotent)

-- 확장 기능 (존재 시 건너뜀)
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

BEGIN;

-- 0) 기본값/무결성 안전장치 ----------------------------------------------
-- users: NOT NULL 컬럼의 기본값을 명시적으로 보정
ALTER TABLE IF EXISTS users ALTER COLUMN token_version SET DEFAULT 0;
ALTER TABLE IF EXISTS users ALTER COLUMN points SET DEFAULT 0;
ALTER TABLE IF EXISTS users ALTER COLUMN grade SET DEFAULT 'C';
UPDATE users SET token_version = 0 WHERE token_version IS NULL;
UPDATE users SET points = 0 WHERE points IS NULL;
UPDATE users SET grade = 'C' WHERE grade IS NULL;

-- places: 투표 카운터 기본값 보정
ALTER TABLE IF EXISTS places ALTER COLUMN count_real SET DEFAULT 0;
ALTER TABLE IF EXISTS places ALTER COLUMN count_normal SET DEFAULT 0;
ALTER TABLE IF EXISTS places ALTER COLUMN count_bad SET DEFAULT 0;
UPDATE places SET count_real = 0 WHERE count_real IS NULL;
UPDATE places SET count_normal = 0 WHERE count_normal IS NULL;
UPDATE places SET count_bad = 0 WHERE count_bad IS NULL;

-- routes: 투표 카운터 기본값 보정
ALTER TABLE IF EXISTS routes ALTER COLUMN count_real SET DEFAULT 0;
ALTER TABLE IF EXISTS routes ALTER COLUMN count_normal SET DEFAULT 0;
ALTER TABLE IF EXISTS routes ALTER COLUMN count_bad SET DEFAULT 0;
UPDATE routes SET count_real = 0 WHERE count_real IS NULL;
UPDATE routes SET count_normal = 0 WHERE count_normal IS NULL;
UPDATE routes SET count_bad = 0 WHERE count_bad IS NULL;

-- 1) 지역 마스터 -----------------------------------------------------------
INSERT INTO region_provinces (province_id, kor_name, eng_name) VALUES
  ('11', '서울', 'Seoul'),
  ('26', '부산', 'Busan'),
  ('41', '경기', 'Gyeonggi-do')
ON CONFLICT (province_id) DO NOTHING;

INSERT INTO region_cities (region_id, province_id, kor_name, eng_name) VALUES
  ('110000', '11', '서울특별시', 'Seoul'),
  ('260000', '26', '부산광역시', 'Busan'),
  ('411100', '41', '수원시', 'Suwon-si')
ON CONFLICT (region_id) DO NOTHING;

-- 2) 테스트 사용자 ---------------------------------------------------------
-- 모든 사용자의 비밀번호는 'password' 입니다 (bcrypt 샘플 해시 사용)
INSERT INTO users (
  id, token_version, email, hashed_password, nickname, intro, city_id, is_local, points, grade
) VALUES
  (1, 0, 'local.user@example.com', '$2b$12$EixZa7NpcyA.1x43j2yvDu2x8zB7pT.hyEXIFMvAfYFhQax2iNB2G', '수원현지인', '수원의 모든 것을 알려드립니다!', '411100', true, 1250, 'A'),
  (2, 0, 'traveler@example.com', '$2b$12$EixZa7NpcyA.1x43j2yvDu2x8zB7pT.hyEXIFMvAfYFhQax2iNB2G', '여행가', '전국을 여행하는 것을 좋아합니다.', '110000', false, 300, 'C'),
  (3, 0, 'busan.local@example.com', '$2b$12$EixZa7NpcyA.1x43j2yvDu2x8zB7pT.hyEXIFMvAfYFhQax2iNB2G', '부산갈매기', '부산 맛집 전문가', '260000', true, 800, 'B')
ON CONFLICT (id) DO UPDATE SET
  token_version = EXCLUDED.token_version,
  email = EXCLUDED.email,
  nickname = EXCLUDED.nickname,
  intro = EXCLUDED.intro,
  city_id = EXCLUDED.city_id,
  is_local = EXCLUDED.is_local,
  points = EXCLUDED.points,
  grade = EXCLUDED.grade;

-- 3) 테스트 장소 -----------------------------------------------------------
-- ⚠️ 실제 DB 테이블의 컬럼 순서에 맞춰 컬럼 리스트를 명시합니다.
--    관찰 결과(DB에서 오류 로그 기준) places는 다음 순서로 존재합니다:
--    place_id, name, type, is_frequent, created_by, kakao_place_id,
--    atmosphere, pros, cons, image_url, count_real, count_normal, count_bad,
--    created_at, latitude, longitude
--    ※ created_at은 DEFAULT 사용을 위해 INSERT에서 제외하고, 나머지는 모두 지정합니다.
INSERT INTO places (
  place_id, name, type, is_frequent, created_by, kakao_place_id,
  atmosphere, pros, cons, image_url, count_real, count_normal, count_bad,
  latitude, longitude
) VALUES
  (1, '행궁동 벽화마을', '관광지', false, 1, '1111',
   '자유롭고 감성적인', '사진 찍기 좋음', '주말에 사람이 너무 많음',
   'https://placehold.co/600x400/DDDDDD/000000?text=Haenggung-dong', 0, 0, 0,
   37.2836, 127.0166),
  (2, '광교호수공원', '공원', true, 1, '2222',
   '자연과 함께하는', '산책로가 잘 되어있고 야경이 멋짐', '주차하기 힘듦',
   'https://placehold.co/600x400/AACCFF/000000?text=Gwanggyo+Lake+Park', 0, 0, 0,
   37.2891, 127.0641),
  (3, '부산 해운대해수욕장', '해변', false, 3, '3333',
   '활기차고 신나는', '여름에 놀기 좋음', '물가가 비쌈',
   'https://placehold.co/600x400/99CCFF/000000?text=Haeundae+Beach', 0, 0, 0,
   35.1587, 129.1604)
ON CONFLICT (place_id) DO UPDATE SET
  name = EXCLUDED.name,
  type = EXCLUDED.type,
  is_frequent = EXCLUDED.is_frequent,
  created_by = EXCLUDED.created_by,
  kakao_place_id = EXCLUDED.kakao_place_id,
  atmosphere = EXCLUDED.atmosphere,
  pros = EXCLUDED.pros,
  cons = EXCLUDED.cons,
  image_url = EXCLUDED.image_url,
  count_real = COALESCE(EXCLUDED.count_real, 0),
  count_normal = COALESCE(EXCLUDED.count_normal, 0),
  count_bad = COALESCE(EXCLUDED.count_bad, 0),
  latitude = EXCLUDED.latitude,
  longitude = EXCLUDED.longitude;

-- NULL 카운터 보정(안전망)
UPDATE places
SET count_real = 0, count_normal = 0, count_bad = 0
WHERE count_real IS NULL OR count_normal IS NULL OR count_bad IS NULL;

-- 4) 테스트 루트 -----------------------------------------------------------
-- embedding은 NULL 유지 (애플리케이션에서 채움)
INSERT INTO routes (
  route_id, name, is_recommend, created_by, image_url,
  count_real, count_normal, count_bad,
  tag_period, tag_env, tag_with, tag_move, tag_atmosphere, tag_place_count
) VALUES
  (1, '수원 화성 당일치기 감성코스', true, 1,
   'https://placehold.co/600x400/FFCC99/000000?text=Suwon+Fortress+Tour',
   0, 0, 0,
   1, 'city', 'friend', 'walk', '자유롭고 감성적인', 3),
  (2, '부산 해변 맛집 탐방', true, 3,
   'https://placehold.co/600x400/99DDFF/000000?text=Busan+Beach+Eats',
   0, 0, 0,
   2, 'sea', 'love', 'public', '활기차고 신나는', 4)
ON CONFLICT (route_id) DO UPDATE SET
  name = EXCLUDED.name,
  is_recommend = EXCLUDED.is_recommend,
  created_by = EXCLUDED.created_by,
  image_url = EXCLUDED.image_url,
  count_real = COALESCE(EXCLUDED.count_real, 0),
  count_normal = COALESCE(EXCLUDED.count_normal, 0),
  count_bad = COALESCE(EXCLUDED.count_bad, 0),
  tag_period = EXCLUDED.tag_period,
  tag_env = EXCLUDED.tag_env,
  tag_with = EXCLUDED.tag_with,
  tag_move = EXCLUDED.tag_move,
  tag_atmosphere = EXCLUDED.tag_atmosphere,
  tag_place_count = EXCLUDED.tag_place_count;

-- 5) 루트-장소 매핑 -------------------------------------------------------
-- 안전장치: route_place_maps 기본값 보정 (is_transportation NOT NULL 대비)
ALTER TABLE IF EXISTS route_place_maps ALTER COLUMN is_transportation SET DEFAULT false;
UPDATE route_place_maps SET is_transportation = false WHERE is_transportation IS NULL;

-- 루트 1: 수원 화성 코스
INSERT INTO route_place_maps (route_id, place_id, "order", is_transportation, transportation_name) VALUES
  (1, 1, 1, false, NULL), -- 행궁동 벽화마을
  (1, 2, 2, false, NULL)  -- 광교호수공원
ON CONFLICT (route_id, place_id, "order") DO NOTHING;

-- 루트 2: 부산 해변 코스
INSERT INTO route_place_maps (route_id, place_id, "order", is_transportation, transportation_name) VALUES
  (2, 3, 1, false, NULL) -- 해운대
ON CONFLICT (route_id, place_id, "order") DO NOTHING;

-- 6) 시퀀스 보정 ----------------------------------------------------------
SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 0));
SELECT setval('places_place_id_seq', COALESCE((SELECT MAX(place_id) FROM places), 0));
SELECT setval('routes_route_id_seq', COALESCE((SELECT MAX(route_id) FROM routes), 0));

COMMIT;
