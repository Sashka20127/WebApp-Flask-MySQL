-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Хост: 127.0.0.1
-- Время создания: Дек 18 2018 г., 00:37
-- Версия сервера: 5.5.25
-- Версия PHP: 5.3.13

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- База данных: `paid_treatment`
--

-- --------------------------------------------------------

--
-- Структура таблицы `doctor`
--

CREATE TABLE IF NOT EXISTS `doctor` (
  `doctors_code` int(11) NOT NULL AUTO_INCREMENT,
  `doctors_name` text NOT NULL,
  `info` text NOT NULL,
  PRIMARY KEY (`doctors_code`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;



-- --------------------------------------------------------

--
-- Структура таблицы `patient`
--

CREATE TABLE IF NOT EXISTS `patient` (
  `patients_code` int(11) NOT NULL AUTO_INCREMENT,
  `patients_name` text NOT NULL,
  `birthday_date` date NOT NULL,
  PRIMARY KEY (`patients_code`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=16 ;



-- --------------------------------------------------------

--
-- Структура таблицы `rendering_service`
--

CREATE TABLE IF NOT EXISTS `rendering_service` (
  `act_num` int(11) NOT NULL AUTO_INCREMENT,
  `service_date` date NOT NULL,
  `services_code` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `patient_code` int(11) NOT NULL,
  `doctors_code` int(11) NOT NULL,
  PRIMARY KEY (`act_num`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=33 ;



-- --------------------------------------------------------

--
-- Структура таблицы `service`
--

CREATE TABLE IF NOT EXISTS `service` (
  `services_code` int(11) NOT NULL AUTO_INCREMENT,
  `services_name` text NOT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`services_code`),
  UNIQUE KEY `services_code` (`services_code`),
  UNIQUE KEY `services_code_2` (`services_code`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=22 ;


-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `users_id` int(11) NOT NULL AUTO_INCREMENT,
  `login` text NOT NULL,
  `password` text NOT NULL,
  `priv` int(1) NOT NULL,
  PRIMARY KEY (`users_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`users_id`, `login`, `password`, `priv`) VALUES
(1, 'admin', 'admin', 1);


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
