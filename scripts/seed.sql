-- scripts/seed.sql
INSERT INTO region_provinces (province_id, kor_name, eng_name)
VALUES ('11', '서울', 'Seoul')
ON CONFLICT (province_id) DO NOTHING;

INSERT INTO region_cities (region_id, province_id, kor_name, eng_name)
VALUES ('110000', '11', '서울특별시', 'Seoul')
ON CONFLICT (region_id) DO NOTHING;