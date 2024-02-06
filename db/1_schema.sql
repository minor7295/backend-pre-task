-- 연락처 테이블
CREATE TABLE `kidsnote_contact`.`tb_contact` (
  `contact_id` int NOT NULL AUTO_INCREMENT COMMENT "연락처 id",
  `profile` varchar(2083) DEFAULT NULL COMMENT "프로필 사진 url",
  `name` varchar(100) NOT NULL COMMENT "이름",
  `email` varchar(254) DEFAULT NULL COMMENT "이메일",
  `phone` varchar(100) NOT NULL COMMENT "전화번호",
  `company` varchar(100) DEFAULT NULL COMMENT "회사",
  `position` varchar(100) DEFAULT NULL COMMENT "직책",
  `memo` longtext COMMENT "메모",
  `address` longtext COMMENT "주소",
  `birthday` date DEFAULT NULL COMMENT "생일",
  `website` varchar(2083) DEFAULT NULL COMMENT "웹사이트",
  PRIMARY KEY (`contact_id`),
  UNIQUE KEY `ix_api_contact_01` (`phone`),
  KEY `ix_api_contact_02` (`name`),
  KEY `ix_api_contact_03` (`email`),
  KEY `ix_api_contact_04` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT "연락처";

-- 라벨 테이블
CREATE TABLE `kidsnote_contact`.`tb_label` (
  `label_id` int NOT NULL AUTO_INCREMENT COMMENT "라벨 id",
  `label_name` varchar(100) NOT NULL COMMENT "라벨 이름",
  PRIMARY KEY (`label_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT "라벨";

-- 연락처 - 라벨 매개 테이블
CREATE TABLE `kidsnote_contact`.`tb_contact_label` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `contact_id` int NOT NULL COMMENT "연락처 id",
  `label_id` int NOT NULL COMMENT "라벨 id",
  PRIMARY KEY (`id`),
  KEY `ix_api_contact_label_01` (`contact_id`),
  KEY `ix_api_contact_label_02` (`label_id`),
  CONSTRAINT `fk_contact_label_contact` FOREIGN KEY (`contact_id`) REFERENCES `tb_contact` (`contact_id`),
  CONSTRAINT `fk_contact_label_label` FOREIGN KEY (`label_id`) REFERENCES `tb_label` (`label_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
