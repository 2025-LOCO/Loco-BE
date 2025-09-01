-- scripts/seed.sql
-- 1) 확장(선택): 사용하는 경우만 유지하세요
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS vector;

BEGIN;

-- 2) 지역 마스터
INSERT INTO region_provinces (province_id, kor_name, eng_name)
VALUES
  ('11', '서울', 'Seoul')
ON CONFLICT (province_id) DO NOTHING;

INSERT INTO region_cities (region_id, province_id, kor_name, eng_name)
VALUES
  ('110000', '11', '서울특별시', 'Seoul')
ON CONFLICT (region_id) DO NOTHING;

-- 3) 테스트 사용자
-- 비밀번호 해시 값은 임시 문자열이어도 무방합니다(애플리케이션 검증은 로그인 시에만 사용).
-- 실제 로그인 테스트가 필요하면, 나중에 /auth/register API로 정상 가입을 수행하세요.
INSERT INTO users (id, token_version, email, hashed_password, nickname, intro, city_id, created_at, is_local)
VALUES
  (1, 0, 'seed_user@example.com', '$2b$12$abcdefghijklmnopqrstuv', 'seed-user', 'seeded user', '110000', NOW(), FALSE)
ON CONFLICT (id) DO NOTHING;

-- 이메일이 유니크라면 이메일 기준도 보정
INSERT INTO users (token_version, email, hashed_password, nickname, intro, city_id, created_at, is_local)
SELECT 0, 'seed_user@example.com', '$2b$12$abcdefghijklmnopqrstuv', 'seed-user', 'seeded user', '110000', NOW(), FALSE
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'seed_user@example.com');

-- 4) 장소 더미 데이터 (created_by = 1 필수)
-- kakao_place_id 는 NULL 허용
INSERT INTO places (
  place_id, name, type, is_frequent, created_by,
  atmosphere, pros, cons, image_url,
  count_real, count_normal, count_bad,
  created_at, latitude, longitude, kakao_place_id
) VALUES
  (1, '카페 라떼하우스', '카페', TRUE, 1,
   '아늑함', '와이파이/콘센트 많음', '주말 대기 김', 'https://example.com/images/cafe-lattehouse.jpg',
   0, 0, 0,
   NOW(), 37.5665, 126.9780, NULL),
  (2, '포레스트릿', '레스토랑', FALSE, 1,
   '활기참', '단체석 가능', '피크타임 혼잡', 'https://example.com/images/forest-restaurant.jpg',
   0, 0, 0,
   NOW(), 37.5700, 126.9820, NULL)
ON CONFLICT (place_id) DO NOTHING;

-- 5) 시퀀스 보정: SERIAL/AUTOINCREMENT를 쓰는 PK가 있으면 현재 최대값에 맞춰 setval
-- 시퀀스 이름은 DB에서 \d places 등으로 확인 후 맞춰 주세요.
-- 예시: places_place_id_seq, users_id_seq 라는 이름일 때
DO $$
DECLARE
  max_users_id BIGINT;
  max_places_id BIGINT;
BEGIN
  SELECT COALESCE(MAX(id), 0) INTO max_users_id FROM users;
  PERFORM setval('users_id_seq', max_users_id);

  SELECT COALESCE(MAX(place_id), 0) INTO max_places_id FROM places;
  PERFORM setval('places_place_id_seq', max_places_id);
END $$;

COMMIT;