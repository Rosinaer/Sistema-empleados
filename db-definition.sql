CREATE DATABASE if not exists Proyecto_CAC;
USE Proyecto_CAC;

CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    Doc INT NOT NULL UNIQUE,
    dirección VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL UNIQUE,
    foto VARCHAR(1000)
);
