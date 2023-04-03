-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : lun. 03 avr. 2023 à 11:21
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `discord`
--

-- --------------------------------------------------------

--
-- Structure de la table `canaux`
--

DROP TABLE IF EXISTS `canaux`;
CREATE TABLE IF NOT EXISTS `canaux` (
  `id_canal` int NOT NULL AUTO_INCREMENT,
  `nom_canal` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `type_canal` varchar(255) DEFAULT NULL,
  `id_serveur` int DEFAULT NULL,
  `port` int DEFAULT NULL,
  PRIMARY KEY (`id_canal`),
  KEY `id_serveur` (`id_serveur`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `canaux`
--

INSERT INTO `canaux` (`id_canal`, `nom_canal`, `description`, `type_canal`, `id_serveur`, `port`) VALUES
(1, 'Général', 'Premier canal', 'textuelle', 1, 1024),
(2, 'Bienvenue', '...', 'Textuelle', 1, 1025),
(3, 'Blabla', '...', 'Textuelle', 1, 1026);

-- --------------------------------------------------------

--
-- Structure de la table `membres`
--

DROP TABLE IF EXISTS `membres`;
CREATE TABLE IF NOT EXISTS `membres` (
  `id_utilisateur` int DEFAULT NULL,
  `id_serveur` int DEFAULT NULL,
  `date_joined` date DEFAULT NULL,
  KEY `id_utilisateur` (`id_utilisateur`),
  KEY `id_serveur` (`id_serveur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `membres`
--

INSERT INTO `membres` (`id_utilisateur`, `id_serveur`, `date_joined`) VALUES
(1, 1, '2023-03-29'),
(NULL, NULL, NULL),
(3, 1, '2023-04-02');

-- --------------------------------------------------------

--
-- Structure de la table `messages`
--

DROP TABLE IF EXISTS `messages`;
CREATE TABLE IF NOT EXISTS `messages` (
  `id_message` int NOT NULL AUTO_INCREMENT,
  `text` varchar(1024) DEFAULT NULL,
  `date_envoi` date DEFAULT NULL,
  `heure_envoi` time DEFAULT NULL,
  `id_utilisateur` int DEFAULT NULL,
  `id_canal` int DEFAULT NULL,
  PRIMARY KEY (`id_message`),
  KEY `id_utilisateur` (`id_utilisateur`),
  KEY `id_canal` (`id_canal`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `messages`
--

INSERT INTO `messages` (`id_message`, `text`, `date_envoi`, `heure_envoi`, `id_utilisateur`, `id_canal`) VALUES
(3, 'test: Naruto est le meilleure manga srx', '2023-04-03', '07:21:30', 1, 1),
(4, 'test: Eh ouais...', '2023-04-03', '07:24:02', 1, 1),
(5, 'test: regardez jojo', '2023-04-03', '07:31:39', 1, 1),
(6, 'test: dernier test...', '2023-04-03', '07:33:15', 1, 1);

-- --------------------------------------------------------

--
-- Structure de la table `serveur`
--

DROP TABLE IF EXISTS `serveur`;
CREATE TABLE IF NOT EXISTS `serveur` (
  `id_serveur` int NOT NULL AUTO_INCREMENT,
  `nom_serveur` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `date_creation` date DEFAULT NULL,
  `id_utilisateur` int DEFAULT NULL,
  PRIMARY KEY (`id_serveur`),
  KEY `id_utilisateur` (`id_utilisateur`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `serveur`
--

INSERT INTO `serveur` (`id_serveur`, `nom_serveur`, `description`, `date_creation`, `id_utilisateur`) VALUES
(1, 'First Server', 'Premier serveur du projet discord', '2023-03-29', 1);

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs`
--

DROP TABLE IF EXISTS `utilisateurs`;
CREATE TABLE IF NOT EXISTS `utilisateurs` (
  `id_utilisateur` int NOT NULL AUTO_INCREMENT,
  `nom_utilisateur` varchar(255) DEFAULT NULL,
  `email_utilisateur` varchar(255) DEFAULT NULL,
  `mot_de_passe` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_utilisateur`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `utilisateurs`
--

INSERT INTO `utilisateurs` (`id_utilisateur`, `nom_utilisateur`, `email_utilisateur`, `mot_de_passe`) VALUES
(1, 'test', 'azerty@gmail.com', 'azerty'),
(2, 'Rayan13', 'rayanahamadi13@gmail.com', 'qxd8enkm'),
(3, 'root', 'root@root.com', 'root');

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `canaux`
--
ALTER TABLE `canaux`
  ADD CONSTRAINT `canaux_ibfk_1` FOREIGN KEY (`id_serveur`) REFERENCES `serveur` (`id_serveur`),
  ADD CONSTRAINT `canaux_ibfk_2` FOREIGN KEY (`id_serveur`) REFERENCES `serveur` (`id_serveur`);

--
-- Contraintes pour la table `membres`
--
ALTER TABLE `membres`
  ADD CONSTRAINT `membres_ibfk_1` FOREIGN KEY (`id_utilisateur`) REFERENCES `utilisateurs` (`id_utilisateur`),
  ADD CONSTRAINT `membres_ibfk_2` FOREIGN KEY (`id_utilisateur`) REFERENCES `utilisateurs` (`id_utilisateur`),
  ADD CONSTRAINT `membres_ibfk_3` FOREIGN KEY (`id_serveur`) REFERENCES `serveur` (`id_serveur`);

--
-- Contraintes pour la table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`id_utilisateur`) REFERENCES `utilisateurs` (`id_utilisateur`),
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`id_canal`) REFERENCES `canaux` (`id_canal`);

--
-- Contraintes pour la table `serveur`
--
ALTER TABLE `serveur`
  ADD CONSTRAINT `serveur_ibfk_1` FOREIGN KEY (`id_utilisateur`) REFERENCES `utilisateurs` (`id_utilisateur`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
