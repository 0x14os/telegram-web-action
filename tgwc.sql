/*
 Navicat Premium Data Transfer

 Source Server         : andy-bak
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : 207.154.228.100:3306
 Source Schema         : tgwc

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

 Date: 08/11/2022 09:22:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tg_msg
-- ----------------------------
DROP TABLE IF EXISTS `tg_msg`;
CREATE TABLE `tg_msg` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `guid` char(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT 'GUID',
  `type` tinyint(1) DEFAULT '1' COMMENT '1/系统通知,2/信箱',
  `user_id` char(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'userId',
  `title` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '名称',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '内容',
  `status` int DEFAULT '1' COMMENT '1/未读,2/已读',
  `create_time` int DEFAULT NULL,
  `update_time` int DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='消息';

-- ----------------------------
-- Records of tg_msg
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tg_task
-- ----------------------------
DROP TABLE IF EXISTS `tg_task`;
CREATE TABLE `tg_task` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `guid` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'guid',
  `type` int NOT NULL DEFAULT '1' COMMENT '1/群组发送,2/?',
  `user_id` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户id',
  `user_account_id` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户TG账号',
  `user_account_group_list` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '群发ID集合，以逗号进行分割',
  `send_group_number` int NOT NULL COMMENT '群发数量',
  `title` varchar(120) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '标题',
  `msg` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '发送内容',
  `timer` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '任务触发时间',
  `remark` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '备注',
  `status` tinyint unsigned DEFAULT '1' COMMENT '1/正常,2/删除',
  `create_time` int DEFAULT NULL,
  `update_time` int DEFAULT NULL,
  `method` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '模式',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='任务';

-- ----------------------------
-- Records of tg_task
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tg_task_msg
-- ----------------------------
DROP TABLE IF EXISTS `tg_task_msg`;
CREATE TABLE `tg_task_msg` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `task_id` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '任务ID',
  `user_account_group_id` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '群组id',
  `text` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '内容',
  `status` tinyint unsigned DEFAULT '0' COMMENT '1/发送成功,2/发送失败',
  `status_time` int DEFAULT NULL COMMENT '状态触发时间',
  `status_exp_log` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '异常日志',
  `create_time` int DEFAULT NULL,
  `update_time` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='任务消息';

-- ----------------------------
-- Records of tg_task_msg
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tg_task_private
-- ----------------------------
DROP TABLE IF EXISTS `tg_task_private`;
CREATE TABLE `tg_task_private` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `guid` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'guid',
  `user_id` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户id',
  `userAccountIdList` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '用户TG账号集合，以逗号进行分割',
  `title` varchar(120) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '标题',
  `soKey` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '关键词逗号分隔',
  `sendNumber` int DEFAULT NULL COMMENT '群发数量',
  `sendAccountNumber` int DEFAULT NULL COMMENT '账号发送条数',
  `accountNumber` int DEFAULT NULL COMMENT '账号数量',
  `timer` int DEFAULT NULL COMMENT '休眠时间',
  `remark` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '备注',
  `status` tinyint unsigned DEFAULT '1' COMMENT '1/待启动,2/启动,3/任务结束',
  `create_time` int DEFAULT NULL,
  `update_time` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='私人任务';

-- ----------------------------
-- Records of tg_task_private
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tg_task_private_log
-- ----------------------------
DROP TABLE IF EXISTS `tg_task_private_log`;
CREATE TABLE `tg_task_private_log` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `guid` char(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `task_id` char(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '任务ID',
  `user_account_id` char(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'tg账号ID',
  `user_account_group_user_id` char(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '群成员id',
  `soKey` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '关键词',
  `tg_username` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户名',
  `tg_user_id` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户ID',
  `tg_access_hash` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户哈希',
  `tg_nicename` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '无' COMMENT '昵称',
  `tg_phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '手机号码',
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '内容',
  `status` tinyint unsigned DEFAULT '0' COMMENT '1/待发送,2/已发送,3/发送失败',
  `status_time` int DEFAULT NULL COMMENT '状态触发时间',
  `create_time` int DEFAULT NULL,
  `update_time` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=68949 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='私人群发日志';

-- ----------------------------
-- Records of tg_task_private_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tg_task_private_text
-- ----------------------------
DROP TABLE IF EXISTS `tg_task_private_text`;
CREATE TABLE `tg_task_private_text` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `guid` char(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `task_id` char(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '任务ID',
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '内容',
  `status` tinyint unsigned DEFAULT '0' COMMENT '1/正常,2/删除',
  `create_time` int DEFAULT NULL,
  `update_time` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='私人任务内容';

-- ----------------------------
-- Records of tg_task_private_text
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tg_user
-- ----------------------------
DROP TABLE IF EXISTS `tg_user`;
CREATE TABLE `tg_user` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `guid` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'guid',
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'email',
  `password` varchar(360) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码',
  `password_random` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码随机数',
  `token` varchar(360) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'token',
  `role_use` int DEFAULT '2' COMMENT '1/管理员,2/普通用户',
  `login_count` int DEFAULT '0' COMMENT '登陆次数',
  `last_ip` varchar(210) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '127.0.0.1' COMMENT '最后登陆ip',
  `status` tinyint unsigned DEFAULT '1' COMMENT '1/正常,2/删除',
  `create_time` int DEFAULT NULL,
  `update_time` int DEFAULT NULL COMMENT '更新时间',
  `groupId` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '组id',
  `taskNumber` int DEFAULT NULL,
  `tgNumber` int DEFAULT NULL,
  `tgGroupNumber` int DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='用户表';

-- ----------------------------
-- Records of tg_user
-- ----------------------------
BEGIN;
INSERT INTO `tg_user` (`id`, `guid`, `email`, `password`, `password_random`, `token`, `role_use`, `login_count`, `last_ip`, `status`, `create_time`, `update_time`, `groupId`, `taskNumber`, `tgNumber`, `tgGroupNumber`) VALUES (1, '16439214-fc45-11e9-bd65-38f9d309cec3', 'x@x.com', 'pbkdf2:sha256:150000$hc1J25Ni$558542e7462955ab209b1058b7fa4b5fead04e6f1d61dcc147d0c5fa157e332a', '24', 'e6dc5b13dd8910d2b5c43e43061f991d', 1, 25, '127.0.0.1', 1, 1572570926, 1651217583, NULL, NULL, NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for tg_user_account
-- ----------------------------
DROP TABLE IF EXISTS `tg_user_account`;
CREATE TABLE `tg_user_account` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `guid` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'guid',
  `user_id` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '0' COMMENT 'user_id',
  `api_id` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'api id',
  `api_hash` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'token in hash',
  `api_name` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '0' COMMENT 'api 名称',
  `api_certificate` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '公钥',
  `phone_code_hash` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'login',
  `phone` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '0' COMMENT '手机号码',
  `username` varchar(38) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '0' COMMENT '用户名称',
  `is_activation` int DEFAULT '1' COMMENT '1/未激活,2/已激活',
  `is_group` int DEFAULT '1' COMMENT '1/未更新,2/已更新',
  `status` tinyint unsigned DEFAULT '1' COMMENT '1/正常,2/删除',
  `create_time` int DEFAULT NULL,
  `update_time` int DEFAULT NULL COMMENT '更新时间',
  `is_new_group` int DEFAULT '1' COMMENT '1/未创建,2/创建新群,3/新建失败',
  `new_group_list` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '创建时有数据，创建完成，清空数据',
  `new_group_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '新名称',
  `proof` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '凭证',
  `mode` tinyint(1) DEFAULT NULL COMMENT '1/群发,2/私人',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=551 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC COMMENT='用户Tg账户';

-- ----------------------------
-- Records of tg_user_account
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tg_user_account_friend
-- ----------------------------
DROP TABLE IF EXISTS `tg_user_account_friend`;
CREATE TABLE `tg_user_account_friend` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `guid` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'guid',
  `user_id` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户ID',
  `user_account_id` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'tg账号ID',
  `account_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT 'TG账号id',
  `account_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '用户名',
  `phone` varchar(250) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '手机号码',
  `nickname` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '0' COMMENT '昵称',
  `avatar` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '/timg.jpg' COMMENT '头像',
  `status` tinyint unsigned DEFAULT '1' COMMENT '1/正常,2/删除',
  `create_time` int DEFAULT NULL,
  `update_time` int DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='用户账号好友';

-- ----------------------------
-- Records of tg_user_account_friend
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tg_user_account_group
-- ----------------------------
DROP TABLE IF EXISTS `tg_user_account_group`;
CREATE TABLE `tg_user_account_group` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `guid` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'guid',
  `user_id` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户ID',
  `user_account_id` char(38) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'tg账号ID',
  `channel_id` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '0' COMMENT '群id',
  `channel_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '无' COMMENT '群标题',
  `channel_username` varchar(250) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '群名称',
  `channel_access_hash` varchar(180) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '群访问token',
  `avatar` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '/timg.jpg' COMMENT '群头像',
  `group_info` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '' COMMENT '群简介',
  `approval` tinyint DEFAULT '1' COMMENT '是否需要验证加群:1/验证,2/不验证,3/第三方验证',
  `group_size` int DEFAULT '0' COMMENT '加群人数',
  `status` tinyint unsigned DEFAULT '1' COMMENT '1/正常,2/删除',
  `create_time` int DEFAULT NULL,
  `update_time` int DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `channel_title` (`channel_title`) USING BTREE,
  UNIQUE KEY `channel_username` (`channel_username`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='用户TG账号群组';

-- ----------------------------
-- Records of tg_user_account_group
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tg_user_account_group_user
-- ----------------------------
DROP TABLE IF EXISTS `tg_user_account_group_user`;
CREATE TABLE `tg_user_account_group_user` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `guid` char(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'guid',
  `user_id` char(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '用户ID',
  `user_account_id` char(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT 'tg账号ID',
  `user_account_group_id` char(38) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '群id',
  `channel_id` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '0' COMMENT '群id',
  `channel_title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '无' COMMENT '群标题',
  `channel_username` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '' COMMENT '群id名',
  `tg_username` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户名',
  `tg_user_id` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户ID',
  `tg_access_hash` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户哈希',
  `tg_nicename` varchar(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '无' COMMENT '昵称',
  `tg_phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '国际手机号码',
  `tg_last_time` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '最后登录时间',
  `status` tinyint unsigned DEFAULT '1' COMMENT '1/正常,2/删除',
  `create_time` int DEFAULT NULL,
  `update_time` int DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=61526 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC COMMENT='TG群组用户';

-- ----------------------------
-- Records of tg_user_account_group_user
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
