-- MySQL dump 10.13  Distrib 8.0.44, for Linux (aarch64)
--
-- Host: localhost    Database: electronics_db
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
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
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Category',6,'add_category'),(22,'Can change Category',6,'change_category'),(23,'Can delete Category',6,'delete_category'),(24,'Can view Category',6,'view_category'),(25,'Can add Order',7,'add_order'),(26,'Can change Order',7,'change_order'),(27,'Can delete Order',7,'delete_order'),(28,'Can view Order',7,'view_order'),(29,'Can add OrderItem',8,'add_orderitem'),(30,'Can change OrderItem',8,'change_orderitem'),(31,'Can delete OrderItem',8,'delete_orderitem'),(32,'Can view OrderItem',8,'view_orderitem'),(33,'Can add Payment',9,'add_payment'),(34,'Can change Payment',9,'change_payment'),(35,'Can delete Payment',9,'delete_payment'),(36,'Can view Payment',9,'view_payment'),(37,'Can add Product',10,'add_product'),(38,'Can change Product',10,'change_product'),(39,'Can delete Product',10,'delete_product'),(40,'Can view Product',10,'view_product'),(41,'Can add Subcategory',11,'add_subcategory'),(42,'Can change Subcategory',11,'change_subcategory'),(43,'Can delete Subcategory',11,'delete_subcategory'),(44,'Can view Subcategory',11,'view_subcategory'),(45,'Can add user',12,'add_customuser'),(46,'Can change user',12,'change_customuser'),(47,'Can delete user',12,'delete_customuser'),(48,'Can view user',12,'view_customuser');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_category`
--

DROP TABLE IF EXISTS `core_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_category`
--

LOCK TABLES `core_category` WRITE;
/*!40000 ALTER TABLE `core_category` DISABLE KEYS */;
INSERT INTO `core_category` VALUES (1,'Smartphones & Gadgets'),(2,'Home appliances'),(3,'TV & Audio');
/*!40000 ALTER TABLE `core_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_order`
--

DROP TABLE IF EXISTS `core_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `address` varchar(255) NOT NULL,
  `status` smallint unsigned NOT NULL,
  `created_at` date NOT NULL,
  `user_id` bigint NOT NULL,
  `payment_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `payment_id` (`payment_id`),
  KEY `core_order_user_id_b03bbffd_fk_users_customuser_id` (`user_id`),
  CONSTRAINT `core_order_payment_id_e5a26a3c_fk_core_payment_id` FOREIGN KEY (`payment_id`) REFERENCES `core_payment` (`id`),
  CONSTRAINT `core_order_user_id_b03bbffd_fk_users_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`),
  CONSTRAINT `core_order_chk_1` CHECK ((`status` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_order`
--

LOCK TABLES `core_order` WRITE;
/*!40000 ALTER TABLE `core_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_orderitem`
--

DROP TABLE IF EXISTS `core_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) NOT NULL,
  `quantity` int unsigned NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `order_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_orderitem_order_id_30929c10_fk_core_order_id` (`order_id`),
  KEY `core_orderitem_product_id_0c2047cd_fk_core_product_id` (`product_id`),
  CONSTRAINT `core_orderitem_order_id_30929c10_fk_core_order_id` FOREIGN KEY (`order_id`) REFERENCES `core_order` (`id`),
  CONSTRAINT `core_orderitem_product_id_0c2047cd_fk_core_product_id` FOREIGN KEY (`product_id`) REFERENCES `core_product` (`id`),
  CONSTRAINT `core_orderitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_orderitem`
--

LOCK TABLES `core_orderitem` WRITE;
/*!40000 ALTER TABLE `core_orderitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_payment`
--

DROP TABLE IF EXISTS `core_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_method` smallint unsigned NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` smallint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `core_payment_chk_1` CHECK ((`payment_method` >= 0)),
  CONSTRAINT `core_payment_chk_2` CHECK ((`status` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_payment`
--

LOCK TABLES `core_payment` WRITE;
/*!40000 ALTER TABLE `core_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_product`
--

DROP TABLE IF EXISTS `core_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `quantity` int unsigned NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` longtext NOT NULL,
  `subcategory_id` bigint NOT NULL,
  `image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_product_subcategory_id_eff25cab_fk_core_subcategory_id` (`subcategory_id`),
  CONSTRAINT `core_product_subcategory_id_eff25cab_fk_core_subcategory_id` FOREIGN KEY (`subcategory_id`) REFERENCES `core_subcategory` (`id`),
  CONSTRAINT `core_product_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_product`
--

LOCK TABLES `core_product` WRITE;
/*!40000 ALTER TABLE `core_product` DISABLE KEYS */;
INSERT INTO `core_product` VALUES (1,'iPhone 16',10,799.99,'The best phone ever',1,'Apple-iPhone-16-release-date-price-and-features.jpg'),(2,'Delonghi ECAM350',20,599.99,'Coffee brings life',2,'e30b33543d0746bd9b2b3554857955ff_768x700.jpg'),(3,'Apple Watch 10',5,359.99,'Smart and reliable',4,'121202-apple-watch-series-10.png'),(4,'Samsung TAB 10',25,499.99,'Android 13, 16 GB RAM, 128 GB Storage',3,'S10_Plus_Color_Selection_Moonstone_Gray_PC_1600x864.png.webp'),(5,'Samsung Galaxy S25 Ultra',20,999.99,'Samsung flagman smartphone',1,'products/samsung_galaxy_s25_ultra_gs4v76df4o4xshby.jpg.avif'),(6,'NINJA Luxe Cafe Premier Series ES601UK Bean to Cup Coffee Machine',10,549.99,'Bean to cup coffee machine',2,'products/M10270794_silver.webp'),(7,'SAMSUNG Series 5 SpaceMax WW11DG5B25AEEU WiFi-enabled 11 kg 1400 Spin Washing Machine - White',20,379.00,'Smart, compact and reliable',5,'products/10263818.webp'),(8,'SAMSUNG S95F 65\" OLED Glare Free 4K Vision AI Smart TV 2025 - QE65S95F',20,2399.00,'For those who eager a fancy picture',6,'products/10282705.webp'),(9,'MARSHALL Bromley 750 Bluetooth Megasound Party Speaker - Black & Brass',15,899.00,'Best of the best, and even better!',7,'products/10290002.webp');
/*!40000 ALTER TABLE `core_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_subcategory`
--

DROP TABLE IF EXISTS `core_subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_subcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_subcategory_category_id_ca17dbdb_fk_core_category_id` (`category_id`),
  CONSTRAINT `core_subcategory_category_id_ca17dbdb_fk_core_category_id` FOREIGN KEY (`category_id`) REFERENCES `core_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_subcategory`
--

LOCK TABLES `core_subcategory` WRITE;
/*!40000 ALTER TABLE `core_subcategory` DISABLE KEYS */;
INSERT INTO `core_subcategory` VALUES (1,'Smartphones',1),(2,'Coffe Machines',2),(3,'Tablets',1),(4,'Smart Watches',1),(5,'Washing Machines',2),(6,'Smart TV',3),(7,'Speakers & Hi-Fi systems',3);
/*!40000 ALTER TABLE `core_subcategory` ENABLE KEYS */;
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
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `users_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-10-31 13:35:27.878485','1','Smartphones & Gadgets',1,'[{\"added\": {}}]',6,1),(2,'2025-10-31 13:36:09.256074','2','Home appliances',1,'[{\"added\": {}}]',6,1),(3,'2025-10-31 13:36:41.273267','1','Smartphone',1,'[{\"added\": {}}]',11,1),(4,'2025-10-31 13:37:04.466199','2','Coffe Machines',1,'[{\"added\": {}}]',11,1),(5,'2025-10-31 13:37:13.348656','3','Tablets',1,'[{\"added\": {}}]',11,1),(6,'2025-10-31 13:37:25.980800','4','Smart Watches',1,'[{\"added\": {}}]',11,1),(7,'2025-10-31 13:38:42.978795','1','iPhone 16',1,'[{\"added\": {}}]',10,1),(8,'2025-10-31 13:40:23.842378','2','Delonghi ECAM350',1,'[{\"added\": {}}]',10,1),(9,'2025-10-31 13:41:03.905203','3','Apple Watch 10',1,'[{\"added\": {}}]',10,1),(10,'2025-10-31 13:42:52.421990','4','Samsung TAB 10',1,'[{\"added\": {}}]',10,1),(11,'2025-11-01 19:18:43.517439','4','Samsung TAB 10',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',10,1),(12,'2025-11-01 19:18:57.065939','3','Apple Watch 10',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',10,1),(13,'2025-11-01 19:19:06.741851','2','Delonghi ECAM350',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',10,1),(14,'2025-11-01 19:19:13.945753','1','iPhone 16',2,'[{\"changed\": {\"fields\": [\"Image\"]}}]',10,1),(15,'2025-11-01 21:47:10.562029','5','Samsung Galaxy S25 Ultra',1,'[{\"added\": {}}]',10,1),(16,'2025-11-01 21:53:45.501504','6','NINJA Luxe Cafe Premier Series ES601UK Bean to Cup Coffee Machine',1,'[{\"added\": {}}]',10,1),(17,'2025-11-02 15:40:22.390473','5','Washing Machines',1,'[{\"added\": {}}]',11,1),(18,'2025-11-02 15:42:13.997127','7','SAMSUNG Series 5 SpaceMax WW11DG5B25AEEU WiFi-enabled 11 kg 1400 Spin Washing Machine - White',1,'[{\"added\": {}}]',10,1),(19,'2025-11-02 15:46:51.258194','7','SAMSUNG Series 5 SpaceMax WW11DG5B25AEEU WiFi-enabled 11 kg 1400 Spin Washing Machine - White',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',10,1),(20,'2025-11-02 16:00:54.406682','1','Smartphones',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',11,1),(21,'2025-11-02 16:03:11.973137','3','TV & Audio',1,'[{\"added\": {}}]',6,1),(22,'2025-11-02 16:03:34.258162','6','Smart TV',1,'[{\"added\": {}}]',11,1),(23,'2025-11-02 16:04:52.287308','7','Speakers & Hi-Fi systems',1,'[{\"added\": {}}]',11,1),(24,'2025-11-02 16:07:14.340021','8','SAMSUNG S95F 65\" OLED Glare Free 4K Vision AI Smart TV 2025 - QE65S95F',1,'[{\"added\": {}}]',10,1),(25,'2025-11-02 16:09:31.172351','9','MARSHALL Bromley 750 Bluetooth Megasound Party Speaker - Black & Brass',1,'[{\"added\": {}}]',10,1);
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
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(6,'core','category'),(7,'core','order'),(8,'core','orderitem'),(9,'core','payment'),(10,'core','product'),(11,'core','subcategory'),(5,'sessions','session'),(12,'users','customuser');
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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-31 13:26:19.088381'),(2,'contenttypes','0002_remove_content_type_name','2025-10-31 13:26:19.112701'),(3,'auth','0001_initial','2025-10-31 13:26:19.185400'),(4,'auth','0002_alter_permission_name_max_length','2025-10-31 13:26:19.201119'),(5,'auth','0003_alter_user_email_max_length','2025-10-31 13:26:19.203632'),(6,'auth','0004_alter_user_username_opts','2025-10-31 13:26:19.206244'),(7,'auth','0005_alter_user_last_login_null','2025-10-31 13:26:19.207981'),(8,'auth','0006_require_contenttypes_0002','2025-10-31 13:26:19.208646'),(9,'auth','0007_alter_validators_add_error_messages','2025-10-31 13:26:19.210576'),(10,'auth','0008_alter_user_username_max_length','2025-10-31 13:26:19.212501'),(11,'auth','0009_alter_user_last_name_max_length','2025-10-31 13:26:19.214580'),(12,'auth','0010_alter_group_name_max_length','2025-10-31 13:26:19.221425'),(13,'auth','0011_update_proxy_permissions','2025-10-31 13:26:19.225216'),(14,'auth','0012_alter_user_first_name_max_length','2025-10-31 13:26:19.227094'),(15,'users','0001_initial','2025-10-31 13:26:19.309978'),(16,'admin','0001_initial','2025-10-31 13:26:19.394709'),(17,'admin','0002_logentry_remove_auto_add','2025-10-31 13:26:19.397827'),(18,'admin','0003_logentry_add_action_flag_choices','2025-10-31 13:26:19.401327'),(19,'core','0001_initial','2025-10-31 13:26:19.468618'),(20,'core','0002_initial','2025-10-31 13:26:19.586132'),(21,'sessions','0001_initial','2025-10-31 13:26:19.599018'),(22,'core','0003_product_image','2025-11-01 19:14:45.585850'),(23,'core','0004_alter_product_image','2025-11-01 19:39:03.216617'),(24,'core','0005_alter_subcategory_category','2025-11-02 16:00:04.642035');
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
INSERT INTO `django_session` VALUES ('txcitpcps5m1gfbw5r5wbtt2c1i1l71u','.eJxVjMsOwiAQRf-FtSEwUyjj0r3fQHgMUjU0Ke3K-O_apAvd3nPOfQkftrX6rfPipyzOQovT7xZDenDbQb6Hdptlmtu6TFHuijxol9c58_NyuH8HNfT6rZEtQnGWMpWUUDlC1IBMjArJDEET2MGokRwgMYxR6-RAOWUKM0Tx_gCugTZj:1vEpFC:zTfxXUaWbdrkmJBO2UnrZ7qf0KiJT0hqrsYROXSxY30','2025-11-14 13:32:42.547833');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_customuser`
--

DROP TABLE IF EXISTS `users_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
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
  `address` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_customuser`
--

LOCK TABLES `users_customuser` WRITE;
/*!40000 ALTER TABLE `users_customuser` DISABLE KEYS */;
INSERT INTO `users_customuser` VALUES (1,'pbkdf2_sha256$1000000$xP8iTpRN71PMHxry7Zkc6m$2+OmGFLK455Jraz00bxD38F2HNpYVvQSxFZ8yH0KIK4=','2025-10-31 13:32:42.545382',1,'test','','','test@example.com',1,1,'2025-10-31 13:32:34.163632','','');
/*!40000 ALTER TABLE `users_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_customuser_groups`
--

DROP TABLE IF EXISTS `users_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_customuser_groups_customuser_id_group_id_76b619e3_uniq` (`customuser_id`,`group_id`),
  KEY `users_customuser_groups_group_id_01390b14_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_customuser_gro_customuser_id_958147bf_fk_users_cus` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`),
  CONSTRAINT `users_customuser_groups_group_id_01390b14_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_customuser_groups`
--

LOCK TABLES `users_customuser_groups` WRITE;
/*!40000 ALTER TABLE `users_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_customuser_user_permissions`
--

DROP TABLE IF EXISTS `users_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_customuser_user_pe_customuser_id_permission_7a7debf6_uniq` (`customuser_id`,`permission_id`),
  KEY `users_customuser_use_permission_id_baaa2f74_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_customuser_use_customuser_id_5771478b_fk_users_cus` FOREIGN KEY (`customuser_id`) REFERENCES `users_customuser` (`id`),
  CONSTRAINT `users_customuser_use_permission_id_baaa2f74_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_customuser_user_permissions`
--

LOCK TABLES `users_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 20:29:24
