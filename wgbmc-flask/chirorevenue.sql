-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 23, 2026 at 10:48 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `galii_baha_oromiyaa`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(10) UNSIGNED NOT NULL,
  `username` varchar(80) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `username`, `password_hash`, `created_at`) VALUES
(1, 'admin', '$2y$10$F0e3miH3kDpI591J/jkkgu5WfDN9AwZYhdQVuOodSR75QTSJaEmUC', '2026-11-20 19:28:49');

-- --------------------------------------------------------

--
-- Table structure for table `revenue_records`
--

CREATE TABLE `revenue_records` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `category` varchar(40) NOT NULL,
  `serial_no` int(11) DEFAULT NULL,
  `entity_name` varchar(160) NOT NULL,
  `annual_plan` decimal(18,2) NOT NULL DEFAULT 0.00,
  `annual_actual` decimal(18,2) NOT NULL DEFAULT 0.00,
  `annual_percent` decimal(8,2) NOT NULL DEFAULT 0.00,
  `daily_plan` decimal(18,2) NOT NULL DEFAULT 0.00,
  `daily_actual` decimal(18,2) NOT NULL DEFAULT 0.00,
  `daily_percent` decimal(8,2) NOT NULL DEFAULT 0.00,
  `is_summary` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `revenue_records`
--

INSERT INTO `revenue_records` (`id`, `category`, `serial_no`, `entity_name`, `annual_plan`, `annual_actual`, `annual_percent`, `daily_plan`, `daily_actual`, `daily_percent`, `is_summary`, `created_at`, `updated_at`) VALUES
(374, 'MQopheessaa', 1, 'Ifaa Na jbaas', '40832284.61', '8804326.89', '21.56', '204161.42', '219330.48', '107.43', 0, '2026-11-20 20:58:23', '2026-11-21 17:40:25'),
(375, 'MQopheessaa', 2, 'Ballina Ciroo', '18131901.64', '2057174.83', '11.35', '95659.51', '67509.13', '70.57', 0, '2026-11-20 21:01:01', '2026-11-21 16:46:16'),
(376, 'MQopheessaa', 3, 'Harawa Gora', '28650167.74', '5104237.98', '17.82', '118250.84', '66024.04', '55.83', 0, '2026-11-20 21:03:00', '2026-11-20 21:03:00'),
(377, 'MQopheessaa', 4, 'Burqaa Ciroo', '90496884.00', '19659008.69', '21.72', '452482.42', '222938.26', '49.27', 0, '2026-11-20 21:04:33', '2026-11-20 21:04:33'),
(378, 'MQopheessaa', 5, 'Barii Qillisoo', '41061868.78', '10469824.74', '25.50', '205309.34', '67509.13', '32.88', 0, '2026-11-20 21:06:20', '2026-11-20 21:06:20'),
(379, 'MQopheessaa', 6, 'Cafee Araaraa', '105390197.87', '36228992.15', '34.38', '541950.99', '140816.48', '25.98', 0, '2026-11-20 21:31:32', '2026-11-20 21:31:32'),
(380, 'MQopheessaa', 7, 'Madda Bekumsa', '61075602.86', '11387287.25', '18.64', '305378.01', '73149.26', '23.95', 0, '2026-11-20 21:32:56', '2026-11-20 21:32:56'),
(381, 'MQopheessaa', 8, 'Ifa Misoomaa', '93676071.03', '21702037.45', '23.17', '473380.36', '105859.21', '22.36', 0, '2026-11-20 21:34:03', '2026-11-20 21:34:03'),
(382, 'MQopheessaa', 9, 'Burqaa Wadd', '32690181.73', '6722124.12', '20.56', '165450.91', '32123.00', '19.42', 0, '2026-11-20 21:34:58', '2026-11-20 21:34:58'),
(383, 'MQopheessaa', 10, 'Madhicho Muc', '32611281.06', '7171789.14', '21.99', '163056.41', '8716.78', '5.35', 0, '2026-11-20 21:36:06', '2026-11-20 21:36:06');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `revenue_records`
--
ALTER TABLE `revenue_records`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_category` (`category`),
  ADD KEY `idx_entity` (`entity_name`),
  ADD KEY `idx_summary` (`is_summary`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `revenue_records`
--
ALTER TABLE `revenue_records`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=384;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
