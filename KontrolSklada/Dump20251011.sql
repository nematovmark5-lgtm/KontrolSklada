-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: warehouse_system
-- ------------------------------------------------------
-- Server version	9.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Товар',7,'add_product'),(26,'Can change Товар',7,'change_product'),(27,'Can delete Товар',7,'delete_product'),(28,'Can view Товар',7,'view_product'),(29,'Can add Сектор',8,'add_sector'),(30,'Can change Сектор',8,'change_sector'),(31,'Can delete Сектор',8,'delete_sector'),(32,'Can view Сектор',8,'view_sector'),(33,'Can add Пункт выдачи',9,'add_pickuppoint'),(34,'Can change Пункт выдачи',9,'change_pickuppoint'),(35,'Can delete Пункт выдачи',9,'delete_pickuppoint'),(36,'Can view Пункт выдачи',9,'view_pickuppoint'),(37,'Can add Запрос товара',10,'add_productrequest'),(38,'Can change Запрос товара',10,'change_productrequest'),(39,'Can delete Запрос товара',10,'delete_productrequest'),(40,'Can view Запрос товара',10,'view_productrequest'),(41,'Can add Движение товара',11,'add_productmovement'),(42,'Can change Движение товара',11,'change_productmovement'),(43,'Can delete Движение товара',11,'delete_productmovement'),(44,'Can view Движение товара',11,'view_productmovement'),(45,'Can add Отчет',12,'add_report'),(46,'Can change Отчет',12,'change_report'),(47,'Can delete Отчет',12,'delete_report'),(48,'Can view Отчет',12,'view_report');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$G0RbiJq5rHehc8L3ub6ka8$5UmBi/3iT2rAdk7ngCG2VsYp5D9v8uecB7J1Wfm8y10=','2025-10-11 04:13:16.504719',0,'pvz_user','Менеджер','ПВЗ Центр','pvz@example.com',0,1,'2025-10-10 18:16:19.508396'),(2,'pbkdf2_sha256$1000000$UsA9DBHTpdHcEeWP48gMlz$zC13VRLZfWfeNrPvVA/zGWjwCJ1ubeLCMXeyvxFduJM=',NULL,0,'pvz_user2','Менеджер','ПВЗ Север','pvz2@example.com',0,1,'2025-10-10 18:16:20.015343'),(3,'pbkdf2_sha256$1000000$k9oZXuogdp4I2B9FtvWpHr$gjpWn/4Hah/pcAHHszI1/p3uHY6dHdBRUfBvaNJceAM=','2025-10-11 07:05:46.614315',1,'admin','','','admin@example.com',1,1,'2025-10-10 19:00:06.760829');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-10-11 06:48:47.612226','5','Сектор A',3,'',8,3),(2,'2025-10-11 06:48:59.957527','7','Сектор C',3,'',8,3),(3,'2025-10-11 06:49:12.776966','6','Сектор B',3,'',8,3);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(9,'warehouse','pickuppoint'),(7,'warehouse','product'),(11,'warehouse','productmovement'),(10,'warehouse','productrequest'),(12,'warehouse','report'),(8,'warehouse','sector');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-10 18:16:12.205148'),(2,'auth','0001_initial','2025-10-10 18:16:12.825112'),(3,'admin','0001_initial','2025-10-10 18:16:12.947947'),(4,'admin','0002_logentry_remove_auto_add','2025-10-10 18:16:12.954482'),(5,'admin','0003_logentry_add_action_flag_choices','2025-10-10 18:16:12.960421'),(6,'contenttypes','0002_remove_content_type_name','2025-10-10 18:16:13.050182'),(7,'auth','0002_alter_permission_name_max_length','2025-10-10 18:16:13.101815'),(8,'auth','0003_alter_user_email_max_length','2025-10-10 18:16:13.119282'),(9,'auth','0004_alter_user_username_opts','2025-10-10 18:16:13.125123'),(10,'auth','0005_alter_user_last_login_null','2025-10-10 18:16:13.179848'),(11,'auth','0006_require_contenttypes_0002','2025-10-10 18:16:13.181681'),(12,'auth','0007_alter_validators_add_error_messages','2025-10-10 18:16:13.187717'),(13,'auth','0008_alter_user_username_max_length','2025-10-10 18:16:13.259900'),(14,'auth','0009_alter_user_last_name_max_length','2025-10-10 18:16:13.311948'),(15,'auth','0010_alter_group_name_max_length','2025-10-10 18:16:13.326841'),(16,'auth','0011_update_proxy_permissions','2025-10-10 18:16:13.333334'),(17,'auth','0012_alter_user_first_name_max_length','2025-10-10 18:16:13.405233'),(18,'sessions','0001_initial','2025-10-10 18:16:13.435306'),(19,'warehouse','0001_initial','2025-10-10 18:16:13.960494'),(20,'warehouse','0002_report','2025-10-10 18:16:14.240917'),(21,'warehouse','0003_alter_pickuppoint_options_and_more','2025-10-11 05:18:26.996250');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0s7vpl6zbru3ww0ko94iea1h6jc0o533','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7Qzp:2gf7gYGqihPGTVBFodqeRYlQRCtiBE-f2goCWyXo4is','2025-10-25 04:14:17.164810'),('1x8jnhf3x68b0w6uwytfgpr6dctu61zj','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7RvF:toErEmYEPahikPDWwo0geIG5gKByPeXq2LEh2tpAzFU','2025-10-25 05:13:37.740695'),('220itfvzr5lnspkigv8qdc87r0kq6y4o','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7SAn:lqKz3U9msnkPRH5Is5PgjGez95NawHiMX1r9MY0HJkA','2025-10-25 05:29:41.209208'),('73tua01n0n7se2trjaenunv1st7u118d','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7S9W:oPY92qM5Uxff8Wl9vwPWfuVkfEZj2ENwkF_E3J35Vnc','2025-10-25 05:28:22.422699'),('7pmzjei1g7i5rov86c46s0e65t22yzr2','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7SAW:Ja2LFB--WzrWEMEOLcYVcuGUCbNj3iuRL33t_NLhWSY','2025-10-25 05:29:24.336916'),('9kooxc0n0mpfm2du7mwqf92bggpv520c','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7SDY:KO_wuV5BOl42ZFLvXpawnDk0BmQOWWv-8pg0k6msmys','2025-10-25 05:32:32.405487'),('avxsjzmo201gudkp4x9jdq2r2fci4doi','.eJxVjDsOwjAQBe_iGlmO_6ak5wzWeneDA8iR4qRC3B0ipYD2zcx7iQzbWvPWeckTibMw4vS7FcAHtx3QHdptlji3dZmK3BV50C6vM_Hzcrh_BxV6_daY2LtIEUJUEAdKYJznwAguebCWBw1kggVFEROOo2OdFFGx2tgSnXh_APHeOEU:1v7JSC:u9vuJ0G3GKC1nvWFDo6A_3RIArP6iM975TdSxCQSQLQ','2025-10-24 20:11:04.532685'),('buqfr4i4ggkdeqkrvo563g9s0pjcifpx','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7RwL:TVUrEvTCNywLrhslOvk0uxlg-vkPvxucU7V27BvuVNg','2025-10-25 05:14:45.687247'),('dymlkiazckv75j6lwb5b8cf3qb96wo0z','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7TIG:Frc0WFDzLn00L6LQua-FLeKIaLHV37d4GRMaj5rRljU','2025-10-25 06:41:28.044785'),('e2sktfy6m2hye2upuatfawa8xy8nulzg','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7RKh:_Rhpq2vPxDKnqJVttjve4uua5PeXrox8eRMdTBzjF14','2025-10-25 04:35:51.466566'),('gi4qgtopz4txtyppoaqned70izrx3yq6','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7TNW:ETsPURb9fYm4QuheLi4dO8WfB5K-Kdf8z6prnpfZYig','2025-10-25 06:46:54.855907'),('gmc53a1700000erwt2jn9zfrkyrgxy47','.eJxVjMsOwiAQRf-FtSE8CnVcuu83kBmGStVAUtqV8d-VpAtd3eSek_MSAfcth72lNSwsLsKK0-9HGB-pdMB3LLcqYy3bupDsijxok1Pl9Lwe7l8gY8s9O1hQyhoHTGOKoGeNOoLB70B0aAZHmLyeE2hvHaNnwEhnRoKRFYv3B9ZLOFM:1v7Jd5:Ov8yDJym0rM_7Q7ZzDNIUR6-bKLIQ0uVj28YtfLaV7U','2025-10-24 20:22:19.146582'),('hlj9j17vy4ayi1colc5g2ogl3xsxcrvf','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7RcG:TEuG97MEre3cH1hkkt3EtghZLrM-YcViPApJ69eo5m0','2025-10-25 04:54:00.925284'),('icll8cdz91ajlu44j6shtihm0jbq1vjf','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7Tfm:MD4RuUz1_ZMLb6OVz2CEuacX2QhKnnGnUwmCqTgOPxM','2025-10-25 07:05:46.616263'),('imy1au5ufmy9q25v7z316lo2okqrv47e','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7S8F:IgI0dRVjnwy7mRp7eRNIL1TBxB1-OURMf7Rxkt0s1f4','2025-10-25 05:27:03.149064'),('ip92s744zya83jtga3upff38i83ostac','.eJxVjDsOwyAQBe9CHSHMbyFlep8BsbAEJxGWjF1FuXtsyUXSzsx7bxbittawdVrClNmVDezyyzCmJ7VD5Eds95mnua3LhPxI-Gk7H-dMr9vZ_h3U2Ou-Fp5AaGdMhiId4KAJJJiMqByZAkKAVNqjEUVLi8omVSxYj97LHSn2-QK5FTad:1v7Hij:HsngkEQM4pZRbu9c2qK8cRaE49KcAt2e80GoCBFIYdU','2025-10-24 18:20:01.897774'),('kgrkn5zpaykybujx57c1e8b7k2s21auk','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7THv:2Jdmaa3c3MeKbuHRyBvLAIn54iwUJoqHJohbmpnLt34','2025-10-25 06:41:07.852775'),('mb33hgb8snvaouvdg8qj1rr31xoh7gd5','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7SD0:S0wlYhz--FJiF5p0jHfB9Yw2juT-YFSaPCfNZKKUxNU','2025-10-25 05:31:58.589233'),('o0uxtuj1al3jt1ybj46r4v2vtaxjx6r4','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7RqA:MQtStCKr9lJDPhPNChGo9EYLkuO6Rrs3SAeppFh6Eys','2025-10-25 05:08:22.413833'),('uxeg8ig4bd5r5s1ddfb82ecmo5yciywj','.eJxVjMsOwiAQRf-FtSFDBwu4dN9vIDxmpGogKe3K-O_apAvd3nPOfQkftrX4rdPi5ywuAsXpd4shPajuIN9DvTWZWl2XOcpdkQftcmqZntfD_TsooZdvnTQ7dDYlMAYis2V2OhI6ldERnYPGDAoYgMkSjCoPCYOxaowGB4Xi_QH2STfW:1v7TP0:RD2wZWfxW7mcRg5YZAg-y9e5NNACRYA_N_ft-zZMMfQ','2025-10-25 06:48:26.603597'),('wz9oq5u76y2pfmu636k7bq6hisdzi0nn','.eJxVjDsOwjAQBe_iGlm24y8lPWew1rtrHECJFCcV4u4QKQW0b2beS2TY1pa3zkseSZyFFqffrQA-eNoB3WG6zRLnaV3GIndFHrTL60z8vBzu30GD3r61AapcsSTLFKJPGpwbgkKrlGUMKuqIpKMJ1QSmNPjoqBZjPWgakkfx_gDxGzfi:1v7Qyq:30XRyY_1SIV0xM1xb_oHstfR_ATq7ks3b4d1jrzqQts','2025-10-25 04:13:16.507549'),('y7o8lxxxxtu3et1p3xqaqv3918thp63i','.eJxVjMsOwiAQRf-FtSE8CnVcuu83kBmGStVAUtqV8d-VpAtd3eSek_MSAfcth72lNSwsLsKK0-9HGB-pdMB3LLcqYy3bupDsijxok1Pl9Lwe7l8gY8s9O1hQyhoHTGOKoGeNOoLB70B0aAZHmLyeE2hvHaNnwEhnRoKRFYv3B9ZLOFM:1v7Qe8:neGHy2gL2hn2Qt6KXbOfSvyA3DEWySksjGNS53soA8E','2025-10-25 03:51:52.040852'),('ybk094v11r7oxjepm7kthcg8cnc8chd0','.eJxVjDsOwyAQBe9CHSHMbyFlep8BsbAEJxGWjF1FuXtsyUXSzsx7bxbittawdVrClNmVDezyyzCmJ7VD5Eds95mnua3LhPxI-Gk7H-dMr9vZ_h3U2Ou-Fp5AaGdMhiId4KAJJJiMqByZAkKAVNqjEUVLi8omVSxYj97LHSn2-QK5FTad:1v7JJp:ntol_FrZyTxfmhQcGZRQTijnnOX9PtZLOmYPmNNF1AU','2025-10-24 20:02:25.524211'),('zwn9in5vq2hf0hvqinfys0x5hweoasr7','.eJxVjDsOwyAQBe9CHSHMbyFlep8BsbAEJxGWjF1FuXtsyUXSzsx7bxbittawdVrClNmVDezyyzCmJ7VD5Eds95mnua3LhPxI-Gk7H-dMr9vZ_h3U2Ou-Fp5AaGdMhiId4KAJJJiMqByZAkKAVNqjEUVLi8omVSxYj97LHSn2-QK5FTad:1v7I4V:jJZvBquUClC5ICQR9HstOqDnb5aBnZ67gbngm6ouGNo','2025-10-24 18:42:31.275871');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse_pickuppoint`
--

DROP TABLE IF EXISTS `warehouse_pickuppoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse_pickuppoint` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `address` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `manager_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `warehouse_pickuppoint_manager_id_77b604a0_fk_auth_user_id` (`manager_id`),
  CONSTRAINT `warehouse_pickuppoint_manager_id_77b604a0_fk_auth_user_id` FOREIGN KEY (`manager_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse_pickuppoint`
--

LOCK TABLES `warehouse_pickuppoint` WRITE;
/*!40000 ALTER TABLE `warehouse_pickuppoint` DISABLE KEYS */;
INSERT INTO `warehouse_pickuppoint` VALUES (1,'ПВЗ Центр','ул. Центральная, 1','2025-10-10 18:16:20.595565',1),(2,'ПВЗ Север','ул. Северная, 15','2025-10-10 18:16:20.598246',2),(3,'ПВЗ Центральный','ул. Ленина, 10','2025-10-11 06:45:09.486521',3),(4,'ПВЗ Северный','ул. Мира, 25','2025-10-11 06:45:09.488889',3);
/*!40000 ALTER TABLE `warehouse_pickuppoint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse_product`
--

DROP TABLE IF EXISTS `warehouse_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `article` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `quantity` int unsigned NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `sector_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `article` (`article`),
  KEY `warehouse_product_sector_id_84d21e85_fk_warehouse_sector_id` (`sector_id`),
  CONSTRAINT `warehouse_product_sector_id_84d21e85_fk_warehouse_sector_id` FOREIGN KEY (`sector_id`) REFERENCES `warehouse_sector` (`id`),
  CONSTRAINT `warehouse_product_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse_product`
--

LOCK TABLES `warehouse_product` WRITE;
/*!40000 ALTER TABLE `warehouse_product` DISABLE KEYS */;
INSERT INTO `warehouse_product` VALUES (1,'iPhone 15','IP15-128','Смартфон Apple iPhone 15 128GB',19,'2025-10-10 18:16:20.561603','2025-10-11 05:14:50.600260',1),(2,'Samsung Galaxy S24','SGS24-256','Смартфон Samsung Galaxy S24 256GB',14,'2025-10-10 18:16:20.564591','2025-10-11 05:35:42.459035',1),(3,'Беспроводные наушники','WH-001','Bluetooth наушники TWS',50,'2025-10-10 18:16:20.566944','2025-10-10 18:16:20.566958',1),(4,'Зарядное устройство','CHG-USB-C','USB-C зарядное устройство 20W',100,'2025-10-10 18:16:20.569171','2025-10-10 18:16:20.569187',1),(5,'Футболка мужская','TSHIRT-M-001','Хлопковая футболка размер M',80,'2025-10-10 18:16:20.571652','2025-10-10 18:16:20.571665',2),(6,'Джинсы женские','JEANS-W-002','Джинсы классического кроя',29,'2025-10-10 18:16:20.573911','2025-10-11 04:14:21.592778',2),(7,'Кроссовки','SNEAK-001','Спортивные кроссовки унисекс',20,'2025-10-10 18:16:20.576380','2025-10-10 18:16:20.576398',2),(8,'Чайник электрический','KETTLE-001','Электрический чайник 1.7л',12,'2025-10-10 18:16:20.579534','2025-10-10 18:16:20.579550',3),(9,'Пылесос','VAC-001','Пылесос с мешком для сбора пыли',5,'2025-10-10 18:16:20.582329','2025-10-10 18:16:20.582344',3),(10,'Лампа настольная','LAMP-001','LED настольная лампа',35,'2025-10-10 18:16:20.584586','2025-10-10 18:16:20.584602',3),(11,'Мяч футбольный','BALL-001','Профессиональный футбольный мяч',18,'2025-10-10 18:16:20.586685','2025-10-10 18:16:20.586697',4),(12,'Гантели','DUMB-001','Разборные гантели 2х10кг',8,'2025-10-10 18:16:20.588853','2025-10-10 18:16:20.588866',4),(13,'Йога-мат','YOGA-001','Коврик для йоги и фитнеса',25,'2025-10-10 18:16:20.591669','2025-10-10 18:16:20.591685',4);
/*!40000 ALTER TABLE `warehouse_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse_productmovement`
--

DROP TABLE IF EXISTS `warehouse_productmovement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse_productmovement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `movement_type` varchar(10) NOT NULL,
  `quantity` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `notes` longtext NOT NULL,
  `product_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `from_sector_id` bigint DEFAULT NULL,
  `to_sector_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `warehouse_productmov_product_id_49a6ce23_fk_warehouse` (`product_id`),
  KEY `warehouse_productmovement_user_id_d7f0b3c8_fk_auth_user_id` (`user_id`),
  KEY `warehouse_productmov_from_sector_id_9aed7302_fk_warehouse` (`from_sector_id`),
  KEY `warehouse_productmov_to_sector_id_2b374e3d_fk_warehouse` (`to_sector_id`),
  CONSTRAINT `warehouse_productmov_from_sector_id_9aed7302_fk_warehouse` FOREIGN KEY (`from_sector_id`) REFERENCES `warehouse_sector` (`id`),
  CONSTRAINT `warehouse_productmov_product_id_49a6ce23_fk_warehouse` FOREIGN KEY (`product_id`) REFERENCES `warehouse_product` (`id`),
  CONSTRAINT `warehouse_productmov_to_sector_id_2b374e3d_fk_warehouse` FOREIGN KEY (`to_sector_id`) REFERENCES `warehouse_sector` (`id`),
  CONSTRAINT `warehouse_productmovement_user_id_d7f0b3c8_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse_productmovement`
--

LOCK TABLES `warehouse_productmovement` WRITE;
/*!40000 ALTER TABLE `warehouse_productmovement` DISABLE KEYS */;
/*!40000 ALTER TABLE `warehouse_productmovement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse_productrequest`
--

DROP TABLE IF EXISTS `warehouse_productrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse_productrequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `status` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `processed_at` datetime(6) DEFAULT NULL,
  `notes` longtext NOT NULL,
  `pickup_point_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `requested_by_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `warehouse_productreq_pickup_point_id_162a5c37_fk_warehouse` (`pickup_point_id`),
  KEY `warehouse_productreq_product_id_029dff89_fk_warehouse` (`product_id`),
  KEY `warehouse_productreq_requested_by_id_a5c41d92_fk_auth_user` (`requested_by_id`),
  CONSTRAINT `warehouse_productreq_pickup_point_id_162a5c37_fk_warehouse` FOREIGN KEY (`pickup_point_id`) REFERENCES `warehouse_pickuppoint` (`id`),
  CONSTRAINT `warehouse_productreq_product_id_029dff89_fk_warehouse` FOREIGN KEY (`product_id`) REFERENCES `warehouse_product` (`id`),
  CONSTRAINT `warehouse_productreq_requested_by_id_a5c41d92_fk_auth_user` FOREIGN KEY (`requested_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `warehouse_productrequest_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse_productrequest`
--

LOCK TABLES `warehouse_productrequest` WRITE;
/*!40000 ALTER TABLE `warehouse_productrequest` DISABLE KEYS */;
INSERT INTO `warehouse_productrequest` VALUES (1,2,'rejected','2025-10-10 18:16:20.601202','2025-10-11 04:13:27.731975','',1,1,1),(2,10,'rejected','2025-10-10 18:16:20.603895','2025-10-11 04:13:25.254728','',1,3,1),(3,5,'rejected','2025-10-10 18:16:20.606662','2025-10-10 20:06:13.441815','',2,5,2),(4,5,'approved','2025-10-10 18:22:41.463800','2025-10-10 18:22:47.000002','',1,1,1),(5,2,'rejected','2025-10-11 04:10:05.767775','2025-10-11 04:13:23.592333','Тест исправленного API',2,1,3),(6,1,'rejected','2025-10-11 04:12:52.926201','2025-10-11 04:13:19.859760','',1,2,1),(7,1,'approved','2025-10-11 04:13:50.104571','2025-10-11 04:14:21.592714','',1,6,1),(8,1,'approved','2025-10-11 05:14:33.566242','2025-10-11 05:14:50.600205','',1,1,1),(9,1,'rejected','2025-10-11 05:28:10.283882','2025-10-11 05:28:24.570168','',1,2,1),(10,1,'approved','2025-10-11 05:32:19.890105','2025-10-11 05:35:42.458975','',1,2,1),(11,1,'rejected','2025-10-11 05:35:31.846318','2025-10-11 05:35:44.718326','',1,3,1),(12,5,'rejected','2025-10-11 05:54:40.207480','2025-10-11 06:22:40.960851','',1,1,3),(13,1,'rejected','2025-10-11 06:22:31.836812','2025-10-11 06:22:39.040145','',1,2,1),(14,5,'pending','2025-10-11 06:45:09.494344',NULL,'Тестовый запрос для iPhone 15',2,1,3),(15,5,'pending','2025-10-11 06:45:09.497407',NULL,'Тестовый запрос для Samsung Galaxy S24',4,2,3),(16,1,'pending','2025-10-11 07:05:36.616978',NULL,'',1,2,1);
/*!40000 ALTER TABLE `warehouse_productrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse_report`
--

DROP TABLE IF EXISTS `warehouse_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse_report` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `report_type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `date_from` date DEFAULT NULL,
  `date_to` date DEFAULT NULL,
  `pdf_file` varchar(100) DEFAULT NULL,
  `excel_file` varchar(100) DEFAULT NULL,
  `created_by_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `warehouse_report_created_by_id_d9d8c105_fk_auth_user_id` (`created_by_id`),
  CONSTRAINT `warehouse_report_created_by_id_d9d8c105_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse_report`
--

LOCK TABLES `warehouse_report` WRITE;
/*!40000 ALTER TABLE `warehouse_report` DISABLE KEYS */;
INSERT INTO `warehouse_report` VALUES (1,'Тестовый отчет 08:40:35','inventory','Автоматически созданный тестовый отчет','2025-10-11 05:40:35.744872',NULL,NULL,'reports/pdf/report_1_20251011_054035.txt','reports/excel/report_1_20251011_054035_data.txt',3),(2,'Test Report','inventory','','2025-10-11 05:41:16.139000',NULL,NULL,'reports/pdf/report_2_20251011_054116.txt','reports/excel/report_2_20251011_054116_data.txt',3),(3,'Тестовый отчет 08:42:13','inventory','Автоматически созданный тестовый отчет','2025-10-11 05:42:13.867256',NULL,NULL,'reports/pdf/report_3_20251011_054213.txt','reports/excel/report_3_20251011_054213_data.txt',3),(4,'Test Shell Report','inventory','','2025-10-11 05:42:48.737405',NULL,NULL,'reports/pdf/test.txt','',3),(5,'Test Inventory Report','inventory','API test report','2025-10-11 05:52:12.850685',NULL,NULL,'reports/pdf/report_5_20251011_055212.txt','reports/excel/report_5_20251011_055212_data.txt',3),(6,'Test Inventory Report','inventory','API test report','2025-10-11 05:53:11.463431',NULL,NULL,'reports/pdf/report_6_20251011_055311.txt','reports/excel/report_6_20251011_055311_data.txt',3),(7,'Тест отчёт','inventory','Тестовый отчёт для диагностики','2025-10-11 06:27:02.502823',NULL,NULL,'reports/pdf/report_7_20251011_062702.txt','reports/excel/report_7_20251011_062702_data.txt',3),(8,'Отчёт по остаткам товаров','inventory','Тестовый отчёт по остаткам товаров','2025-10-11 06:45:09.500515',NULL,NULL,'','',3),(9,'Отчёт по движению товаров','movements','Тестовый отчёт по движению товаров','2025-10-11 06:45:09.503206',NULL,NULL,'','',3),(10,'Отчёт по запросам ПВЗ','requests','Тестовый отчёт по запросам пвз','2025-10-11 06:45:09.506106',NULL,NULL,'','',3),(11,'Статистический отчёт','statistics','Тестовый статистический отчёт','2025-10-11 06:45:09.508559',NULL,NULL,'','',3);
/*!40000 ALTER TABLE `warehouse_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse_report_pickup_points`
--

DROP TABLE IF EXISTS `warehouse_report_pickup_points`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse_report_pickup_points` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `report_id` bigint NOT NULL,
  `pickuppoint_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `warehouse_report_pickup__report_id_pickuppoint_id_1626f884_uniq` (`report_id`,`pickuppoint_id`),
  KEY `warehouse_report_pic_pickuppoint_id_fd9564ed_fk_warehouse` (`pickuppoint_id`),
  CONSTRAINT `warehouse_report_pic_pickuppoint_id_fd9564ed_fk_warehouse` FOREIGN KEY (`pickuppoint_id`) REFERENCES `warehouse_pickuppoint` (`id`),
  CONSTRAINT `warehouse_report_pic_report_id_6211741f_fk_warehouse` FOREIGN KEY (`report_id`) REFERENCES `warehouse_report` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse_report_pickup_points`
--

LOCK TABLES `warehouse_report_pickup_points` WRITE;
/*!40000 ALTER TABLE `warehouse_report_pickup_points` DISABLE KEYS */;
/*!40000 ALTER TABLE `warehouse_report_pickup_points` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse_report_sectors`
--

DROP TABLE IF EXISTS `warehouse_report_sectors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse_report_sectors` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `report_id` bigint NOT NULL,
  `sector_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `warehouse_report_sectors_report_id_sector_id_245b2ea9_uniq` (`report_id`,`sector_id`),
  KEY `warehouse_report_sec_sector_id_cc4bf99d_fk_warehouse` (`sector_id`),
  CONSTRAINT `warehouse_report_sec_report_id_8595d335_fk_warehouse` FOREIGN KEY (`report_id`) REFERENCES `warehouse_report` (`id`),
  CONSTRAINT `warehouse_report_sec_sector_id_cc4bf99d_fk_warehouse` FOREIGN KEY (`sector_id`) REFERENCES `warehouse_sector` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse_report_sectors`
--

LOCK TABLES `warehouse_report_sectors` WRITE;
/*!40000 ALTER TABLE `warehouse_report_sectors` DISABLE KEYS */;
/*!40000 ALTER TABLE `warehouse_report_sectors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse_sector`
--

DROP TABLE IF EXISTS `warehouse_sector`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse_sector` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse_sector`
--

LOCK TABLES `warehouse_sector` WRITE;
/*!40000 ALTER TABLE `warehouse_sector` DISABLE KEYS */;
INSERT INTO `warehouse_sector` VALUES (1,'Электроника','Телефоны, планшеты, аксессуары','2025-10-10 18:16:20.549233'),(2,'Одежда','Мужская и женская одежда','2025-10-10 18:16:20.551540'),(3,'Дом и сад','Товары для дома и дачи','2025-10-10 18:16:20.554121'),(4,'Спорт','Спортивные товары и инвентарь','2025-10-10 18:16:20.557436');
/*!40000 ALTER TABLE `warehouse_sector` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-11 10:14:49
