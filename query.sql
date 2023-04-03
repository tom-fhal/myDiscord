ALTER TABLE messages
ADD FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur);

ALTER TABLE messages
ADD FOREIGN KEY (id_canal) REFERENCES canaux(id_canal);

ALTER TABLE canaux
ADD FOREIGN KEY (id_serveur) REFERENCES serveur(id_serveur);

ALTER TABLE membres
ADD FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur);

ALTER TABLE messages
ADD FOREIGN KEY (id_serveur) REFERENCES serveur(id_serveur);

ALTER TABLE serveur
ADD FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur);