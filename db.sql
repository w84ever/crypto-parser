SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

CREATE TABLE `users` (
  `id` integer UNSIGNED NOT NULL auto_increment,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `date_of_reg` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE `binance` (
  `id` integer UNSIGNED NOT NULL auto_increment,
  `symbol` varchar(20) NOT NULL,
  `ask` varchar(20) NOT NULL,
  `bid` varchar(20) NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (symbol),
  KEY (id)
) ENGINE=InnoDB;

CREATE TABLE `bybit` (
  `id` integer UNSIGNED NOT NULL auto_increment,
  `symbol` varchar(20) NOT NULL,
  `ask` varchar(20) NOT NULL,
  `bid` varchar(20) NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (symbol),
  KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `huobi` (
  `id` integer UNSIGNED NOT NULL auto_increment,
  `symbol` varchar(20) NOT NULL,
  `ask` varchar(20) NOT NULL,
  `bid` varchar(20) NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (symbol),
  KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `gate` (
  `id` integer UNSIGNED NOT NULL auto_increment,
  `symbol` varchar(20) NOT NULL,
  `ask` varchar(20) NOT NULL,
  `bid` varchar(20) NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (symbol),
  KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `kucoin` (
  `id` integer UNSIGNED NOT NULL auto_increment,
  `symbol` varchar(20) NOT NULL,
  `ask` varchar(20) NOT NULL,
  `bid` varchar(20) NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (symbol),
  KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `mexc` (
  `id` integer UNSIGNED NOT NULL auto_increment,
  `symbol` varchar(20) NOT NULL,
  `ask` varchar(20) NOT NULL,
  `bid` varchar(20) NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (symbol),
  KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;