CREATE TABLE `log` (
  `id` int(11) UNSIGNED NOT NULL,
  `m_datetime` datetime DEFAULT NULL,
  `m_host` varchar(100) DEFAULT NULL,
  `m_id` varchar(20) DEFAULT NULL,
  `m_hostname` varchar(100) DEFAULT NULL,
  `m_uri` varchar(200) DEFAULT NULL,
  `m_data` varchar(2000) NOT NULL,
  `m_msg` varchar(1000) DEFAULT NULL,
  `m_original` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
