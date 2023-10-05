-- CREATE TABLES FOR DATABASE `database`
DROP TABLE IF EXISTS `database`.`blockzeit`;
CREATE TABLE `database`.`blockzeit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_from` date NOT NULL,
  `date_to` date NOT NULL,
  `days` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

INSERT INTO `database`.`blockzeit` VALUES (1,'2022-04-22','2022-05-13',16),(2,'2022-01-24','2022-02-16',17);

DROP TABLE IF EXISTS `database`.`klasse`;
CREATE TABLE `database`.`klasse` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4;

INSERT INTO `database`.`klasse` VALUES (1,'IT9a'),(2,'IT9b'),(3,'IT9c'),(4,'IT9d'),(5,'IT9e'),(6,'IT9f'),(7,'IT9i'),(8,'IT9j'),(9,'IT9k'),(10,'IT9l'),(11,'IT9m'),(12,'IT9o'),(13,'IT9p'),(14,'IT9g'),(15,'IT9h'),(16,'IT9n'),(17,'IT9s'),(18,'IT9t'),(19,'IT9z'),(20,'IT9r'),(21,'IT9x'),(22,'IT9y'),(23,'IT0a'),(24,'IT0b'),(25,'IT0c'),(26,'IT0d'),(27,'IT0e'),(28,'IT0f'),(29,'IT0i'),(30,'IT0j'),(31,'IT0k'),(32,'IT0l'),(33,'IT0m'),(34,'IT0o'),(35,'IT0p'),(36,'IT0g'),(37,'IT0h'),(38,'IT0n'),(39,'IT0s'),(40,'IT0t'),(41,'IT0z'),(42,'IT0r'),(43,'IT0x'),(44,'IT0y'),(45,'IT1a'),(46,'IT1b'),(47,'IT1c'),(48,'IT1d'),(49,'IT1e'),(50,'IT1f'),(51,'IT1i'),(52,'IT1j'),(53,'IT1k'),(54,'IT1l'),(55,'IT1m'),(56,'IT1o'),(57,'IT1p'),(58,'IT1g'),(59,'IT1h'),(60,'IT1n'),(61,'IT1s'),(62,'IT1t'),(63,'IT1z'),(64,'IT1r'),(65,'IT1x'),(66,'IT1y');

DROP TABLE IF EXISTS `database`.`klasse_to_blockzeit`;
CREATE TABLE `database`.`klasse_to_blockzeit` (
  `klasse_id` int(11) NOT NULL,
  `blockzeit_id` int(11) NOT NULL,
  PRIMARY KEY (`klasse_id`,`blockzeit_id`) USING BTREE,
  FOREIGN KEY (klasse_id) REFERENCES klasse(id),
  FOREIGN KEY (blockzeit_id) REFERENCES blockzeit(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Neue Tabelle für die News
DROP TABLE IF EXISTS `database`.`news`;
CREATE TABLE `database`.`news` (
  `news_id` int(11) NOT NULL AUTO_INCREMENT,
  `news_image` VARCHAR(100) NOT NULL,
  `news_date_from` date NOT NULL,
  `news_date_to` date NOT NULL,
  `news_body` text NOT NULL,
  PRIMARY KEY (`news_id`) USING BTREE
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `database`.`news` VALUES (1,'TestTest','2022-04-22', '2022-11-10','Testnachricht'),(2,'TestTest2','2022-11-22', '2022-11-25','Testnachricht2'), (3,'TestTest3','2023-11-22','2024-11-22','Testnachricht3');
 
-- CREATE DATABASE `auth`
CREATE DATABASE `auth`;
-- GRANT user `user` ACCESS TO DATABASE `auth`
GRANT ALL PRIVILEGES ON `auth`.* TO 'user'@'%';
FLUSH PRIVILEGES;

-- CREATE TABLES FOR DATABASE `auth`
DROP TABLE IF EXISTS `auth`.`user`;
CREATE TABLE `auth`.`user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `mfa_secret` VARCHAR(255) NOT NULL,
  `status` INT(11) NOT NULL COMMENT "0 = Inaktiv | 1 = Aktiv | 2 = Gesperrt",
  `created_at` DATETIME NOT NULL,
  `last_login` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `auth`.`mac_address`;
CREATE TABLE `auth`.`mac_address` (
`mac_address` VARCHAR(255) NOT NULL,
`id` int(11) NOT NULL,
  PRIMARY KEY (`mac_address`) USING BTREE,
  FOREIGN KEY (id) REFERENCES user(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `auth`.`login_log`;
CREATE TABLE `auth`.`login_log` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `event` TEXT NOT NULL,
  `ip` VARCHAR(255) NOT NULL,
  `timestamp` DATETIME NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
