-- Prefs Fare table
CREATE TABLE `prefs_fare` (
  `id` int NOT NULL AUTO_INCREMENT,
  `direction` varchar(80) NOT NULL,
  `prefix_list` longtext NOT NULL,
  `connection_charge` double NOT NULL,
  `fee_per_second` double NOT NULL,
  `reg_exp` longtext NOT NULL,
  `ordering` int NOT NULL,
  `icon` varchar(50) NOT NULL,
  `position` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1
