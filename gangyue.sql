﻿# Host: localhost  (Version: 5.7.26)
# Date: 2020-04-24 11:06:04
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "user"
#

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` varchar(10) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `password` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

#
# Data for table "user"
#

INSERT INTO `user` VALUES (1,'3119305699','郭开阔','123',1),(2,'3119305698','赵四','123',1),(3,'3119305611','王五','123',1),(4,'3119101195','张雯昕','zwxzwx',1),(5,'3119305692','巩效义','123456',1);

#
# Structure for table "post"
#

DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  `category` enum('觅食','运动','学习','娱乐') NOT NULL,
  `content` text NOT NULL,
  `added_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `is_knot` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `XIF1post` (`user_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8;

#
# Data for table "post"
#

INSERT INTO `post` VALUES (2,'test1','运动','2020-04-11 18:32:40',2,1,0),(3,'test1','运动','2020-04-11 18:32:44',2,1,0),(4,'test1','运动','2020-04-12 13:59:31',2,1,0),(5,'test2','学习','2020-04-12 13:59:31',3,1,0),(6,'test3','娱乐','2020-04-12 13:59:31',1,1,0),(7,'test4','觅食','2020-04-12 14:00:25',2,1,0),(8,'test5','运动','2020-04-12 14:00:25',3,1,0),(9,'test6','学习','2020-04-12 14:00:25',1,1,0),(10,'test7','娱乐','2020-04-12 14:00:25',2,1,0),(11,'test8','觅食','2020-04-12 14:00:25',3,1,0),(12,'test9','运动','2020-04-12 14:00:25',1,1,0),(13,'test10','学习','2020-04-12 14:00:25',2,1,0),(14,'test11','娱乐','2020-04-12 14:00:25',3,1,0),(15,'test12','觅食','2020-04-12 14:00:25',1,1,0),(16,'test13','运动','2020-04-12 14:00:25',2,1,0),(17,'test14','学习','2020-04-12 14:00:25',3,1,0),(18,'test15','娱乐','2020-04-12 14:00:25',1,1,0),(19,'test16','觅食','2020-04-12 14:00:25',2,1,0),(20,'test17','运动','2020-04-12 14:00:25',3,1,0),(21,'test18','学习','2020-04-12 14:00:25',1,1,0),(22,'test19','娱乐','2020-04-12 14:00:25',2,1,0),(23,'test20','觅食','2020-04-12 14:00:25',3,1,0),(24,'test21','运动','2020-04-12 14:00:25',1,1,0),(25,'test22','学习','2020-04-12 14:00:25',2,1,0),(26,'test23','娱乐','2020-04-12 14:00:25',3,1,0),(27,'test24','觅食','2020-04-12 14:00:25',1,1,0),(28,'test25','运动','2020-04-12 14:00:25',2,1,0),(29,'test26','学习','2020-04-12 14:00:25',3,1,0),(30,'test27','娱乐','2020-04-12 14:00:25',1,1,0),(31,'test28','觅食','2020-04-12 14:00:25',2,1,0),(32,'test29','运动','2020-04-12 14:00:25',3,1,0),(33,'test30','学习','2020-04-12 14:00:25',1,1,0),(34,'test31','娱乐','2020-04-12 14:00:25',2,1,0),(35,'test32','觅食','2020-04-12 14:00:25',3,1,0),(36,'test33','运动','2020-04-12 14:00:25',1,1,0),(37,'test34','学习','2020-04-12 14:00:25',2,1,0),(38,'test35','娱乐','2020-04-12 14:00:25',3,1,0),(39,'test36','觅食','2020-04-12 14:00:25',1,1,0),(40,'test37','运动','2020-04-12 14:00:25',2,1,0),(41,'test38','学习','2020-04-12 14:00:25',3,1,0),(42,'test39','娱乐','2020-04-12 14:00:25',1,1,0),(43,'test40','觅食','2020-04-12 14:00:25',2,1,0),(44,'test41','运动','2020-04-12 14:00:25',3,1,0),(45,'test42','学习','2020-04-12 14:00:25',1,1,0),(46,'test43','娱乐','2020-04-12 14:00:25',2,1,0),(47,'test44','觅食','2020-04-12 14:00:25',3,1,0),(48,'test45','运动','2020-04-12 14:00:25',1,1,0),(49,'test46','学习','2020-04-12 14:00:25',2,1,0),(50,'test47','娱乐','2020-04-12 14:00:25',3,1,0),(51,'test48','觅食','2020-04-12 14:00:25',1,1,0),(52,'test49','运动','2020-04-12 14:00:25',2,1,0),(53,'test50','学习','2020-04-12 14:00:25',3,1,0),(54,'test51','娱乐','2020-04-12 14:00:25',1,1,0),(55,'test52','觅食','2020-04-12 14:00:25',2,1,0),(56,'test53','运动','2020-04-12 14:00:25',3,1,0),(57,'test54','学习','2020-04-12 14:00:25',1,1,0),(58,'test55','娱乐','2020-04-12 14:00:25',2,1,0),(59,'test56','觅食','2020-04-12 14:00:25',3,1,0),(60,'test57','运动','2020-04-12 14:00:25',1,1,0),(61,'test58','学习','2020-04-12 14:00:25',2,1,0),(62,'test59','娱乐','2020-04-12 14:00:25',3,1,0),(63,'test60','觅食','2020-04-12 14:00:25',1,1,0),(64,'test61','运动','2020-04-12 14:00:25',2,1,0),(65,'test62','学习','2020-04-12 14:00:25',3,1,0),(66,'test63','娱乐','2020-04-12 14:00:25',1,1,0),(67,'test64','觅食','2020-04-12 14:00:25',2,1,0),(68,'test65','运动','2020-04-12 14:00:25',3,1,0),(69,'test66','学习','2020-04-12 14:00:25',1,1,0),(70,'test67','娱乐','2020-04-12 14:00:25',2,1,0),(71,'test68','觅食','2020-04-12 14:00:25',3,1,0),(72,'test69','运动','2020-04-12 14:00:25',1,1,0),(73,'test70','学习','2020-04-12 14:00:25',2,1,0),(74,'test71','娱乐','2020-04-12 14:00:25',3,1,0),(75,'test72','觅食','2020-04-12 14:00:25',1,1,0),(76,'test73','运动','2020-04-12 14:00:25',2,1,0),(77,'test74','学习','2020-04-12 14:00:25',3,1,0),(78,'test75','娱乐','2020-04-12 14:00:25',1,1,0),(79,'test76','觅食','2020-04-12 14:00:25',2,1,0),(80,'test77','运动','2020-04-12 14:00:25',3,1,0),(81,'test78','学习','2020-04-12 14:00:25',1,1,0),(82,'test79','娱乐','2020-04-12 14:00:25',2,1,0),(83,'test80','觅食','2020-04-12 14:00:25',3,1,0),(84,'test81','运动','2020-04-12 14:00:25',1,1,0),(85,'test82','学习','2020-04-12 14:00:25',2,1,0),(86,'test83','娱乐','2020-04-12 14:00:25',3,1,0),(87,'test84','觅食','2020-04-12 14:00:25',1,1,0),(88,'test85','运动','2020-04-12 14:00:25',2,1,0),(89,'test86','学习','2020-04-12 14:00:25',3,1,0),(90,'test87','娱乐','2020-04-12 14:00:25',1,1,0),(91,'test88','觅食','2020-04-12 14:00:25',2,1,0),(92,'test89','运动','2020-04-12 14:00:25',3,1,0),(93,'test90','学习','2020-04-12 14:00:25',1,1,0),(94,'test91','娱乐','2020-04-12 14:00:25',2,1,0),(95,'test92','觅食','2020-04-12 14:00:25',3,1,0),(96,'test93','运动','2020-04-12 14:00:25',1,1,0),(97,'test94','学习','2020-04-12 14:00:25',2,1,0),(98,'test95','娱乐','2020-04-12 14:00:25',3,1,0),(99,'test96','觅食','2020-04-12 14:00:25',1,1,0),(100,'test97','运动','2020-04-12 14:00:25',2,1,0),(101,'test98','学习','2020-04-12 14:00:25',3,1,0),(102,'test99','娱乐','2020-04-12 14:00:25',1,1,0),(10508,'去玩吧去玩吧去玩吧去玩吧','运动','2020-04-24 11:00:37',5,1,0);

#
# Structure for table "reply"
#

DROP TABLE IF EXISTS `reply`;
CREATE TABLE `reply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `added_time` datetime NOT NULL,
  `post_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `XIF1reply` (`post_id`),
  KEY `XIF2reply` (`user_id`),
  CONSTRAINT `reply_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`),
  CONSTRAINT `reply_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "reply"
#


#
# Structure for table "chat_record"
#

DROP TABLE IF EXISTS `chat_record`;
CREATE TABLE `chat_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `added_time` datetime NOT NULL,
  `from_user_id` int(11) NOT NULL,
  `to_user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `XIF1chat_record` (`from_user_id`),
  KEY `XIF2chat_record` (`to_user_id`),
  CONSTRAINT `chat_record_ibfk_1` FOREIGN KEY (`from_user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `chat_record_ibfk_2` FOREIGN KEY (`to_user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "chat_record"
#

