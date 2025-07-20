INSERT INTO users (email, password, created_at)
VALUES ("test@example.com", "test1234", now);

INSERT INTO ocrs (user_id, new_owner_name, new_owner_address_main, new_owner_address_street, new_owner_address_number, raw_text, created_at)
VALUES (1, "田中　太郎", "兵庫県姫路市飾磨区中島", "1", "3250", "整理番号 MI\n印鑑証明書\n会社法人等番号\n号\n0104 01-059818\n弁護士ドットコム株式会社\n店\n東京都港区六本木四丁目1番4号\n代表取締役\n内田 陽介\n昭和\n日生\nこれは提出されている印鑑の写しに相違ないことを証明する。\n(東京法務局港出張所管轄\n令和2年12月 3日\n東京法務局港出張所\n登記官\n高野\n|東常\n晃張\n登記\n務|\nLU\nCOPY", now());