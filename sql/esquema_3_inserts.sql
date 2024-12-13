INSERT INTO administrador (id, nombres_completos, usuario, clave)
VALUES 
    (1,'Alicia Lizet Niño Effio','alicia123','alicia123'),
    (2,'César Eduardo Bravo Díaz','cesar456','cesar456');

INSERT INTO elemento (id, nomElemento)
VALUES (1, 'Fuego'),
    (2, 'Agua'),
    (3, 'Aire'),
    (4, 'Tierra');
    

INSERT INTO cualidad (id, nombre, descripcion, ELEMENTOid)
VALUES (1, 'acepta riesgos', 'arriesgado/a, intrépido/a', 1),
    (2, 'agresivo/a', 'combativo/a, provocador/a', 1),
    (3, 'atrevido/a', 'osado/a, audaz', 1),
    (4, 'audaz', 'valiente, intrépido/a', 1),
    (5, 'auto suficiente', 'independiente, autónomo/a', 1),
    (6, 'competitivo/a', 'ambicioso/a, rival', 1),
    (7, 'tenaz', 'persistente, obstinado/a', 1),
    (8, 'decidido/a', 'resuelto/a, determinado/a', 1),
    (9, 'decisivo/a', 'determinante, concluyente', 1),
    (10, 'valeroso/a', 'bravo/a, heroico/a', 1),
    (11, 'vigoroso/a', 'enérgico/a, robusto/a', 1),
    (12, 'directo/a', 'franco/a, claro/a', 1),
    (13, 'enérgico/a', 'activo/a, dinámico/a', 1),
    (14, 'osado/a', 'atrevido/a, audaz', 1),
    (15, 'dominante', 'autoritario/a, controlador/a', 1),
    (16, 'habla directo', 'franco/a, sincero/a', 1),
    (17, 'ideas firmes', 'convicciones, decisiones sólidas', 1),
    (18, 'impaciente', 'inquieto/a, ansioso/a', 1),
    (19, 'exigente', 'demandante, riguroso/a', 1),
    (20, 'independiente', 'autónomo/a, libre', 1),
    (21, 'rápido/a', 'veloz, ágil', 1),
    (22, 'inquieto/a', 'nervioso/a, intranquilo/a', 1),
    (23, 'insistente', 'persistente, perseverante', 1),
    (24, 'resuelto/a', 'determinado/a, decidido/a', 1),
    (25, 'franco/a', 'sincero/a, directo/a', 1),
    (26, 'le agrada discutir', 'controversial, argumentador/a', 1),
    (27, 'persistente', 'tenaz, constante', 1),
    (28, 'pionero, iniciador', 'innovador/a, precursor/a', 1),
    (29, 'adaptable', 'flexible, maleable', 2),
    (30, 'amable', 'cordial, gentil', 2),
    (31, 'ameno/a', 'agradable, entretenido/a', 2),
    (32, 'amistoso/a', 'afable, sociable', 2),
    (33, 'bondadoso/a', 'caritativo/a, generoso/a', 2),
    (34, 'calmado/a', 'tranquilo/a, sereno/a', 2),
    (35, 'apacible', 'plácido/a, sosegado/a', 2),
    (36, 'colaborador', 'cooperador/a, ayudante', 2),
    (37, 'comedido/a', 'cortés, atento/a', 2),
    (38, 'atento/a', 'solícito/a, considerado/a', 2),
    (39, 'complaciente', 'concesivo/a, servicial', 2),
    (40, 'comprensivo/a', 'empático/a, tolerante', 2),
    (41, 'considerado/a', 'respetuoso/a, amable', 2),
    (42, 'constante', 'perseverante, firme', 2),
    (43, 'contento/a', 'feliz, alegre', 2),
    (44, 'sensible', 'emocional, delicado/a', 2),
    (45, 'tolerante', 'paciente, indulgente', 2),
    (46, 'tranquilo/a', 'calmado/a, sereno/a', 2),
    (47, 'ecuánime', 'imparcial, equilibrado/a', 2),
    (48, 'obediente', 'disciplinado/a, sumiso/a', 2),
    (49, 'leal', 'fiel, devoto/a', 2),
    (50, 'paciente', 'tolerante, resignado/a', 2),
    (51, 'pacifico', 'sereno/a, calmado/a', 2),
    (52, 'generoso/a', 'altruista, desprendido/a', 2),
    (53, 'gentil', 'educado/a, cortés', 2),
    (54, 'moderado/a', 'mesurado/a, prudente', 2),
    (55, 'alegre', 'jovial, animado/a', 3),
    (56, 'alentador/a', 'motivador/a, inspirador/a', 3),
    (57, 'amigable', 'sociable, cordial', 3),
    (58, 'anima a los demás', 'inspirador/a, motivador/a', 3),
    (59, 'animado/a', 'vivaz, entusiasta', 3),
    (60, 'cautivador/a', 'encantador/a, fascinante', 3),
    (61, 'comunicativo/a', 'expresivo/a, locuaz', 3),
    (62, 'sociable', 'amigable, extrovertido/a', 3),
    (63, 'vivaz', 'dinámico/a, animado/a', 3),
    (64, 'de trato fácil', 'afable, agradable', 3),
    (65, 'elocuente', 'persuasivo/a, expresivo/a', 3),
    (66, 'encantador/a', 'atractivo/a, fascinante', 3),
    (67, 'desenvuelto/a', 'seguro/a, espontáneo/a', 3),
    (68, 'impetuoso/a', 'arrojado/a, impulsivo/a', 3),
    (69, 'impulsivo/a', 'irreflexivo/a, espontáneo/a', 3),
    (70, 'promotor/a', 'iniciador/a, incentivador/a', 3),
    (71, 'entusiasta', 'apasionado/a, fervoroso/a', 3),
    (72, 'espontáneo/a', 'natural, irreflexivo/a', 3),
    (73, 'estimulante', 'motivador/a, inspirador/a', 3),
    (74, 'expresivo/a', 'elocuente, comunicativo/a', 3),
    (75, 'extrovertido/a', 'abierto/a, sociable', 3),
    (76, 'receptivo/a', 'abierto/a, comprensivo/a', 3),
    (77, 'ingenioso/a', 'creativo/a, perspicaz', 3),
    (78, 'popular', 'famoso/a, conocido/a', 3),
    (79, 'jovial', 'alegre, vivaz', 3),
    (80, 'analítico/a', 'crítico/a, evaluador/a', 4),
    (81, 'apego a normas', 'disciplinado/a, reglamentado/a', 4),
    (82, 'cauteloso/a', 'precavido/a, prudente', 4),
    (83, 'cauto/a', 'cuidadoso/a, reservado/a', 4),
    (84, 'certero/a', 'preciso/a, acertado/a', 4),
    (85, 'concienzudo/a', 'meticuloso/a, detallista', 4),
    (86, 'controlado/a', 'moderado/a, reservado/a', 4),
    (87, 'cuida los detalles', 'minucioso/a, perfeccionista', 4),
    (88, 'cuidadoso/a', 'cauto/a, atento/a', 4),
    (89, 'sistemático/a', 'metódico/a, organizado/a', 4),
    (90, 'discerniente', 'perspicaz, sagaz', 4),
    (91, 'discreto/a', 'reservado/a, prudente', 4),
    (92, 'reflexivo/a', 'pensativo/a, meditabundo/a', 4),
    (93, 'reservado/a', 'discreto/a, cauteloso/a', 4),
    (94, 'preciso/a', 'exacto/a, certero/a', 4),
    (95, 'prevenido/a', 'precavido/a, prudente', 4),
    (96, 'evaluador/a', 'analítico/a, crítico/a', 4),
    (97, 'prudente', 'cauto/a, razonable', 4),
    (98, 'lógico/a', 'racional, analítico/a', 4),
    (99, 'meticuloso/a', 'detallista, perfeccionista', 4),
    (100, 'metódico/a', 'sistemático/a, organizado/a', 4),
    (101, 'perceptivo/a', 'perspicaz, observador/a', 4),
    (102, 'perfeccionista', 'detallista, exigente', 4),
    (103, 'investigador/a', 'indagador/a, explorador/a', 4),
    (104, 'sagaz', 'astuto/a, perspicaz', 4),
    (105, 'precavido/a', 'cauteloso/a, prevenido/a', 4);


INSERT INTO grupo (id, nomgrupo)
VALUES
    (1, 'pregunta #1'),
    (2, 'pregunta #2'),
    (3, 'pregunta #3'),
    (4, 'pregunta #4'),
    (5, 'pregunta #5'),
    (6, 'pregunta #6'),
    (7, 'pregunta #7'),
    (8, 'pregunta #8'),
    (9, 'pregunta #9'),
    (10, 'pregunta #10'),
    (11, 'pregunta #11'),
    (12, 'pregunta #12'),
    (13, 'pregunta #13'),
    (14, 'pregunta #14'),
    (15, 'pregunta #15'),
    (16, 'pregunta #16'),
    (17, 'pregunta #17'),
    (18, 'pregunta #18'),
    (19, 'pregunta #19'),
    (20, 'pregunta #20'),
    (21, 'pregunta #21'),
    (22, 'pregunta #22'),
    (23, 'pregunta #23'),
    (24, 'pregunta #24'),
    (25, 'pregunta #25'),
    (26, 'pregunta #26'),
    (27, 'pregunta #27'),
    (28, 'pregunta #28');


INSERT INTO agrupacion (grupoid, cualidadid) 
VALUES
    (1, 71),
    (1, 21),
    (1, 98),
    (1, 35),
    (2, 57),
    (2, 94),
    (2, 25),
    (2, 46),
    (3, 3),
    (3, 85),
    (3, 61),
    (3, 54),
    (4, 74),
    (4, 88),
    (4, 15),
    (4, 44),
    (5, 91),
    (5, 39),
    (5, 66),
    (5, 23),
    (6, 62),
    (6, 89),
    (6, 11),
    (6, 45),
    (7, 60),
    (7, 43),
    (7, 19),
    (7, 81),
    (8, 82),
    (8, 8),
    (8, 76),
    (8, 33),
    (9, 65),
    (9, 86),
    (9, 45),
    (9, 9),
    (10, 31),
    (10, 77),
    (10, 103),
    (10, 1),
    (11, 75),
    (11, 105),
    (11, 42),
    (11, 18),
    (12, 10),
    (12, 58),
    (12, 51),
    (12, 102),
    (13, 22),
    (13, 30),
    (13, 65),
    (13, 88),
    (14, 97),
    (14, 28),
    (14, 72),
    (14, 36),
    (15, 93),
    (15, 38),
    (15, 14),
    (15, 55),
    (16, 62),
    (16, 50),
    (16, 5),
    (16, 84),
    (17, 29),
    (17, 24),
    (17, 95),
    (17, 63),
    (18, 2),
    (18, 68),
    (18, 32),
    (18, 90),
    (19, 64),
    (19, 40),
    (19, 83),
    (19, 16),
    (20, 96),
    (20, 52),
    (20, 59),
    (20, 27),
    (21, 69),
    (21, 87),
    (21, 13),
    (21, 46),
    (22, 73),
    (22, 53),
    (22, 101),
    (22, 20),
    (23, 6),
    (23, 41),
    (23, 55),
    (23, 104),
    (24, 99),
    (24, 48),
    (24, 17),
    (24, 56),
    (25, 78),
    (25, 92),
    (25, 7),
    (25, 34),
    (26, 80),
    (26, 4),
    (26, 49),
    (26, 70),
    (27, 26),
    (27, 100),
    (27, 37),
    (27, 67),
    (28, 79),
    (28, 94),
    (28, 12),
    (28, 47);


INSERT INTO `participante` (`id`, `nombres`, `fecha_nacimiento`, `telefono`, `correo`, `fecha_registro`)
 VALUES (NULL, 'Fabi', '2005-01-06', '906300962', 'fabianapm060126@gmail.com', '2024-12-13 02:44:58');




