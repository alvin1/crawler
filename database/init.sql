CREATE DATABASE  IF NOT EXISTS `crawler` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `crawler`;
-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: 127.0.0.1    Database: crawler
-- ------------------------------------------------------
-- Server version	5.7.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `candidate`
--

DROP TABLE IF EXISTS `candidate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidate` (
  `tender_id` char(36) NOT NULL,
  `candidate_id` char(36) NOT NULL,
  `ranking` varchar(10) DEFAULT NULL,
  `candidate_name` varchar(900) NOT NULL,
  `tender_price` varchar(300) DEFAULT NULL,
  `tender_price_review` varchar(300) DEFAULT NULL,
  `review_score` double DEFAULT NULL,
  PRIMARY KEY (`tender_id`,`candidate_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `candidate_incharge`
--

DROP TABLE IF EXISTS `candidate_incharge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidate_incharge` (
  `tender_id` char(36) NOT NULL,
  `candidate_id` char(36) DEFAULT NULL,
  `incharge_id` char(36) NOT NULL,
  `incharge_type` varchar(50) NOT NULL,
  `incharge_name` varchar(50) NOT NULL,
  `incharge_certificate_name` varchar(300) DEFAULT NULL,
  `incharge_certificate_no` varchar(50) DEFAULT NULL,
  `professional_titles` varchar(300) DEFAULT NULL,
  `professional_grade` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `candidate_incharge_projects`
--

DROP TABLE IF EXISTS `candidate_incharge_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidate_incharge_projects` (
  `tender_id` char(36) DEFAULT NULL,
  `candidate_id` char(36) DEFAULT NULL,
  `incharge_id` char(36) DEFAULT NULL,
  `owner` varchar(1000) DEFAULT NULL,
  `name` varchar(1000) DEFAULT NULL,
  `kick_off_date` datetime DEFAULT NULL,
  `deliver_date` datetime DEFAULT NULL,
  `finish_date` datetime DEFAULT NULL,
  `scale` varchar(8000) DEFAULT NULL,
  `contract_price` double DEFAULT NULL,
  `tech_incharge_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `candidate_projects`
--

DROP TABLE IF EXISTS `candidate_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidate_projects` (
  `tender_id` char(36) DEFAULT NULL,
  `candidate_id` char(36) DEFAULT NULL,
  `owner` varchar(1000) DEFAULT NULL,
  `name` varchar(1000) DEFAULT NULL,
  `kick_off_date` datetime DEFAULT NULL,
  `deliver_date` datetime DEFAULT NULL,
  `finish_date` datetime DEFAULT NULL,
  `scale` varchar(8000) DEFAULT NULL,
  `contract_price` double DEFAULT NULL,
  `project_incharge_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `failed_page`
--

DROP TABLE IF EXISTS `failed_page`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `failed_page` (
  `tender_id` char(36) DEFAULT NULL,
  `page_url` varchar(1000) DEFAULT NULL,
  `failed_type` varchar(10) DEFAULT NULL,
  `page_num` int(11) DEFAULT NULL,
  `page_type` varchar(45) DEFAULT NULL,
  `pubdate` datetime DEFAULT NULL,
  `reprocessed` tinyint(1) NOT NULL DEFAULT '0',
  `process_times` varchar(45) NOT NULL DEFAULT '0',
  `last_process_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `grab_status`
--

DROP TABLE IF EXISTS `grab_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grab_status` (
  `page_num` int(11) DEFAULT NULL,
  `total_pages` int(11) DEFAULT NULL,
  `grab_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `other_tenderer_review`
--

DROP TABLE IF EXISTS `other_tenderer_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `other_tenderer_review` (
  `tender_id` char(36) DEFAULT NULL,
  `tenderer_id` char(36) DEFAULT NULL,
  `tenderer_name` varchar(1000) DEFAULT NULL,
  `price_or_vote_down` varchar(3000) DEFAULT NULL,
  `price_review_or_vote_down_reason` varchar(3000) DEFAULT NULL,
  `review_score_or_description` varchar(3000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `review_board_member`
--

DROP TABLE IF EXISTS `review_board_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `review_board_member` (
  `tender_id` char(36) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `company` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tender_info`
--

DROP TABLE IF EXISTS `tender_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tender_info` (
  `tender_id` char(36) NOT NULL,
  `tender_name` varchar(1000) NOT NULL,
  `pubdate` datetime NOT NULL,
  `page_url` varchar(1000) NOT NULL,
  `owner` varchar(1000) DEFAULT NULL,
  `owner_phone` varchar(200) DEFAULT NULL,
  `tenderee` varchar(1000) DEFAULT NULL,
  `tenderee_phone` varchar(200) DEFAULT NULL,
  `tenderee_proxy` varchar(1000) DEFAULT NULL,
  `tenderee_proxy_phone` varchar(200) DEFAULT NULL,
  `tender_openning_location` varchar(1000) DEFAULT NULL,
  `tender_openning_time` datetime DEFAULT NULL,
  `tender_ceil_price` varchar(100) DEFAULT NULL,
  `publicity_start` datetime DEFAULT NULL,
  `publicity_end` datetime DEFAULT NULL,
  `other_description` varchar(3000) DEFAULT NULL,
  `review_department` varchar(1000) DEFAULT NULL,
  `review_department_phone` varchar(200) DEFAULT NULL,
  `administration_department` varchar(1000) DEFAULT NULL,
  `administration_department_phone` varchar(200) DEFAULT NULL,
  `page_num` int(11) DEFAULT NULL,
  PRIMARY KEY (`tender_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-06-18 14:00:23
