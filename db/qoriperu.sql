-- Crear tabla ROL primero
CREATE TABLE ROL (
    idRol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Luego crear la tabla USUARIO
CREATE TABLE USUARIO (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono CHAR(9) NOT NULL,
    nroDocIde VARCHAR(20) NOT NULL UNIQUE,
    contrasena VARCHAR(50) NOT NULL,
    direccion VARCHAR(100),
    idRol INT NOT NULL,
    FOREIGN KEY (idRol) REFERENCES ROL(idRol)
);

-- Tabla CATEGORIA
CREATE TABLE CATEGORIA (
    idCategoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla RESEÑA, con ON DELETE CASCADE en la clave foránea
CREATE TABLE RESENA (
    idResena INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    idUsuario INT NOT NULL,
    FOREIGN KEY (idUsuario) REFERENCES USUARIO(idUsuario) ON DELETE CASCADE
);

-- Tabla PRODUCTO (falta en tu ejemplo original, la añado aquí)
CREATE TABLE PRODUCTO (
    idProducto INT AUTO_INCREMENT PRIMARY KEY,
    nombredeproducto VARCHAR(100) NOT NULL,
    autor VARCHAR(100),
    precio DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2),
    stock INT NOT NULL,
    nombredeTienda VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    caracteristicas TEXT NOT NULL,
    idCategoria INT NOT NULL,
    imagen VARCHAR(255),  -- Nueva columna para almacenar el nombre del archivo de la imagen
    FOREIGN KEY (idCategoria) REFERENCES CATEGORIA(idCategoria) ON DELETE CASCADE
);

-- Tabla TARJETA
CREATE TABLE TARJETA (
    idTarjeta INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    nroTarjeta VARCHAR(16),
    fecha DATE,
    ccv VARCHAR(3),
    idUsuario INT,
    FOREIGN KEY (idUsuario) REFERENCES USUARIO(idUsuario) ON DELETE CASCADE
);

-- Tabla PEDIDO
CREATE TABLE PEDIDO (
    idPedido INT AUTO_INCREMENT PRIMARY KEY,
    fechainicio DATE,
    fechafinalizado DATE,
    estado VARCHAR(50),
    idUsuario INT,
    FOREIGN KEY (idUsuario) REFERENCES USUARIO(idUsuario) ON DELETE CASCADE
);

-- Tabla PAGO
CREATE TABLE PAGO (
    idPago INT AUTO_INCREMENT PRIMARY KEY,
    fechapago DATE,
    monto DECIMAL(10,2),
    metodopago VARCHAR(50),
    idPedido INT,
    idTarjeta INT,
    FOREIGN KEY (idPedido) REFERENCES PEDIDO(idPedido) ON DELETE CASCADE,
    FOREIGN KEY (idTarjeta) REFERENCES TARJETA(idTarjeta) ON DELETE CASCADE
);

-- Tabla DETALLE_PEDIDO
CREATE TABLE DETALLE_PEDIDO (
    idPedido INT,
    idProducto INT,
    cantidad INT,
    precio DECIMAL(10,2),
    descuento DECIMAL(5,2),
    igv DECIMAL(5,2),
    subtotal DECIMAL(10,2),
    total DECIMAL(10,2),
    PRIMARY KEY (idPedido, idProducto),
    FOREIGN KEY (idPedido) REFERENCES PEDIDO(idPedido) ON DELETE CASCADE,
    FOREIGN KEY (idProducto) REFERENCES PRODUCTO(idProducto) ON DELETE CASCADE
);


-- Insertar roles iniciales en la tabla ROL
INSERT INTO ROL (nombre) VALUES ('Administrador');
INSERT INTO ROL (nombre) VALUES ('Cliente');

-- Insertar usuarios de ejemplo en la tabla USUARIO
INSERT INTO USUARIO (nombres, apellidos, email, telefono, nroDocIde, contrasena, direccion, idRol) 
VALUES ('Rodrigho', 'Pupuche', 'admin@example.com', '981339485', '75062816', 'admin123', 'Sta Cruz de Pachacutec 294', 1);

INSERT INTO USUARIO (nombres, apellidos, email, telefono, nroDocIde, contrasena, direccion, idRol) 
VALUES ('Estela', 'Diaz', 'estela@gmail.com', '987654321', '87654321', 'cliente123', 'JLO Girasoles 123', 2);

-- Insertar categorías iniciales en la tabla CATEGORIA
INSERT INTO CATEGORIA (nombre) VALUES ('Cerámica');
INSERT INTO CATEGORIA (nombre) VALUES ('Joyería Artesanal');
INSERT INTO CATEGORIA (nombre) VALUES ('Retablos');
INSERT INTO CATEGORIA (nombre) VALUES ('Textiles');

-- Inserts de productos para la categoría 'Cerámica'
INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Cerámica Circular', 'Juan Perez', 120.00, 10.00, 50, 'Tienda de Arte', 'Cerámica con forma circular decorada con motivos andinos.', 'Hecho a mano, resistente al calor', 1, 'ceramica_circular.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Cerámica Flor', 'Ana Martinez', 150.00, 15.00, 30, 'Tienda de Arte', 'Cerámica en forma de flor con detalles coloridos.', 'Hecho a mano, diseño único', 1, 'ceramica_flor.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Cerámica Portal', 'Luis Garcia', 200.00, 20.00, 20, 'Tienda de Arte', 'Cerámica decorativa con un diseño de portal.', 'Hecho a mano, ideal para decoración', 1, 'ceramica_portal.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Cerámica Sagrado', 'Maria Lopez', 180.00, 15.00, 25, 'Tienda de Arte', 'Figura cerámica representando un símbolo sagrado.', 'Resistente y decorativo', 1, 'ceramica_sagrado.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Cerámica Vasija', 'Carlos Diaz', 220.00, 20.00, 15, 'Tienda de Arte', 'Vasija cerámica tradicional andina.', 'Diseño exclusivo, hecho a mano', 1, 'ceramica_vasija.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Cerámica Viva', 'Patricia Gomez', 250.00, 25.00, 10, 'Tienda de Arte', 'Cerámica con un diseño vibrante y colores vivos.', 'Durable, diseño auténtico', 1, 'ceramica_viva.webp');

-- Inserts de productos para la categoría 'Joyería Artesanal'
INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Collar Chakana en Plata', 'Victor Torres', 320.00, 30.00, 40, 'Joyería Artesanal', 'Collar con símbolo Chakana en plata.', 'Hecho a mano, detalles en turquesa', 2, 'joyeria_collar.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Pulsera Alpaca Andina', 'Paola Rivera', 150.00, 10.00, 60, 'Joyería Artesanal', 'Pulsera de alpaca con motivos andinos.', 'Decoración geométrica andina', 2, 'joyeria_pulseraalpaca.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Anillo de Oro Sodalita', 'Roberto Sanchez', 600.00, 50.00, 20, 'Joyería Artesanal', 'Anillo de oro con piedra sodalita.', 'Piedra semipreciosa de los Andes', 2, 'joyeria_anillooro.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Aretes Filigrana Plata', 'Daniela Vargas', 350.00, 35.00, 25, 'Joyería Artesanal', 'Aretes de filigrana con diseño floral.', 'Técnica de filigrana peruana', 2, 'joyeria_aretes.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Pulsera Tejido con Cuentas', 'Miguel Ortiz', 180.00, 15.00, 30, 'Joyería Artesanal', 'Pulsera con cuentas de piedras semipreciosas.', 'Tejida a mano con alpaca', 2, 'joyeria_pulseratejido.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Collar Oro y Turquesa', 'Lucía Mendoza', 520.00, 45.00, 15, 'Joyería Artesanal', 'Collar de oro decorado con motivos incas.', 'Detalles de turquesa y oro', 2, 'joyeria_oroturquesa.webp');

-- Inserts de productos para la categoría 'Retablos'
INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Retablo Fiesta Andina', 'Alberto Ramirez', 450.00, 40.00, 10, 'Galería Andina', 'Retablo que representa una fiesta andina.', 'Colores vivos y personajes tradicionales', 3, 'retablo_fiesta.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Retablo Nacimiento Andino', 'Soledad Castro', 500.00, 50.00, 8, 'Galería Andina', 'Retablo que muestra un nacimiento andino.', 'Personajes vestidos con trajes típicos', 3, 'retablo_nacimiento.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Retablo de la Cosecha', 'Ramiro Paredes', 420.00, 35.00, 12, 'Galería Andina', 'Retablo que celebra la cosecha andina.', 'Escena campesina tradicional', 3, 'retablo_cosecha.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Retablo Música Andina', 'Gloria Huerta', 480.00, 45.00, 10, 'Galería Andina', 'Escena musical tradicional andina.', 'Músicos con trajes típicos', 3, 'retablo_musica.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Retablo Procesión Andina', 'Alfredo Quispe', 460.00, 40.00, 9, 'Galería Andina', 'Retablo de una procesión religiosa andina.', 'Colores vibrantes y detalles finos', 3, 'retablo_procesion.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Retablo San Juan Bautista', 'María Espinoza', 520.00, 50.00, 7, 'Galería Andina', 'Retablo que representa a San Juan Bautista.', 'Figuras y detalles religiosos', 3, 'retablo_san_juan.webp');

-- Inserts de productos para la categoría 'Textiles'
INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Aguayo', 'Elias Cardenas', 250.00, 30.00, 50, 'Artesanías Andinas', 'Tejido tradicional andino, lleno de colores.', 'Hecho de lana de alpaca o de oveja', 4, 'textil_aguayo.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Lliclla', 'Rosa Flores', 300.00, 25.00, 30, 'Artesanías Andinas', 'Manto tradicional usado por las mujeres andinas.', 'Patrones geométricos y colores brillantes', 4, 'textil_lliclla.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Unku', 'Javier Contreras', 350.00, 30.00, 20, 'Artesanías Andinas', 'Túnica tradicional inca con patrones geométricos.', 'Hecho de algodón o lana de alpaca', 4, 'textil_unku.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Jaqi', 'Gabriela Figueroa', 280.00, 25.00, 40, 'Artesanías Andinas', 'Tejido aymara tradicional.', 'Colores vivos y patrones geométricos', 4, 'textil_jaqi.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Poncho Andino', 'Hector Vilchez', 400.00, 35.00, 15, 'Artesanías Andinas', 'Prenda tradicional andina con colores vibrantes.', 'Hecho de lana de alpaca o vicuña', 4, 'textil_poncho.webp');

INSERT INTO PRODUCTO (nombredeproducto, autor, precio, descuento, stock, nombredeTienda, descripcion, caracteristicas, idCategoria, imagen)
VALUES ('Chullo Andino', 'Angela Ramos', 180.00, 15.00, 50, 'Artesanías Andinas', 'Gorro tradicional peruano con orejeras.', 'Hecho de lana de alpaca', 4, 'textil_chullo.webp');


-- Insertar reseñas de ejemplo en la tabla RESEÑA
INSERT INTO RESENA (descripcion, idUsuario) 
VALUES ('Reseña del producto 1 por el cliente', 2);

INSERT INTO RESENA (descripcion, idUsuario) 
VALUES ('Reseña del producto 2 por el cliente', 2);

INSERT INTO RESENA (descripcion, idUsuario) 
VALUES ('Reseña del producto 3 por el cliente', 2);