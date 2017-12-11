/*
Navicat MySQL Data Transfer

Source Server         : MyConnection
Source Server Version : 50718
Source Host           : localhost:3306
Source Database       : design

Target Server Type    : MYSQL
Target Server Version : 50718
File Encoding         : 65001

Date: 2017-12-11 16:40:21
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for iotform
-- ----------------------------
DROP TABLE IF EXISTS `iotform`;
CREATE TABLE `iotform` (
  `id` bigint(255) NOT NULL AUTO_INCREMENT,
  `CurrentTime` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `Tem1` float NOT NULL,
  `Tem2` float NOT NULL,
  `Tem3` float NOT NULL,
  `Hum1` float NOT NULL,
  `Hum2` float NOT NULL,
  `Pre1` float NOT NULL,
  `Pre2` float NOT NULL,
  `LED1` bit(1) NOT NULL,
  `LED2` bit(1) NOT NULL,
  `LED3` bit(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21996 DEFAULT CHARSET=utf8;
