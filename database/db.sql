-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Tempo de geração: 04/04/2024 às 03:16
-- Versão do servidor: 8.3.0
-- Versão do PHP: 8.2.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `counter`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `people_entering`
--

CREATE TABLE `people_entering` (
  `id` int NOT NULL,
  `id_people` int NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `people_entering`
--

INSERT INTO `people_entering` (`id`, `id_people`, `created_at`) VALUES
(1, 2, '2024-04-04 00:00:46'),
(2, 4, '2024-04-04 00:00:52');

-- --------------------------------------------------------

--
-- Estrutura para tabela `people_exiting`
--

CREATE TABLE `people_exiting` (
  `id` int NOT NULL,
  `id_people` int NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `people_entering`
--
ALTER TABLE `people_entering`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `people_exiting`
--
ALTER TABLE `people_exiting`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `people_entering`
--
ALTER TABLE `people_entering`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `people_exiting`
--
ALTER TABLE `people_exiting`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
