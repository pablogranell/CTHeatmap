import pandas as pd
import random

competencias = [
    "CT01", "CT02", "CT03", "CT04", "CT05", "CT06",
    "CT07", "CT08", "CT09", "CT10", "CT11", "CT12"
]

asignaturas_1 = [
    "Algebra",
    "Análisis matemático",
    "Estadística",
    "Fundamentos de computadores",
    "Fundamentos de organización de empresas",
    "Fundamentos Físicos de la Informática",
    "Introducción a la informática y a la programación",
    "Matemática discreta",
    "Programación",
    "Tecnología de computadores"
]

asignaturas_2 = [
    "Concurrencia y sistemas distribuidos",
    "Deontología y profesionalismo",
    "Estructura de computadores",
    "Estructuras de datos y algoritmos",
    "Fundamentos de sistemas operativos",
    "Interfaces persona computador",
    "Lenguajes, tecnologías y paradigmas de la programación",
    "Redes de computadores",
    "Teoría de autómatas y lenguajes formales"
]

asignaturas_3 = [
    "Administración de sistemas",
    "Agentes inteligentes",
    "Análisis de requisitos de negocio",
    "Automatización y Robótica para la Industria Digital",
    "Calidad de software",
    "Ciberseguridad",
    "Comportamiento organizativo y gestión del cambio",
    "Computabilidad y complejidad",
    "Desarrollo de software dirigido por modelos",
    "Desarrollo web",
    "Diseño, configuración y evaluación de los sistemas informáticos",
    "Diseño de software",
    "Diseño y configuración de redes de área local",
    "Gestión de las tecnologías de la información",
    "Gestión de Recursos en la nube",
    "Gestión de servicios de SI TI",
    "Gestión y configuración de la arquitectura de los sistemas de información",
    "Intercambio académico IX",
    "Intercambio académico VII",
    "Intercambio académico X",
    "Internet de las Cosas",
    "Métodos formales industriales",
    "Percepción",
    "Proceso de software",
    "Sistemas basados en Deep Learning para la Industria",
    "Sistemas de almacenamiento y recuperación de información",
    "Técnicas de optimización",
    "Tecnología de bases de datos"
]

asignaturas_4 = [
    "Alemán académico y profesional A1",
    "Alemán académico y profesional A1.1",
    "Alemán académico y profesional A1.2",
    "Alemán académico y profesional A2",
    "Alemán académico y profesional B1",
    "Alemán académico y profesional B2",
    "Algorítmica",
    "Análisis avanzado de datos en Ingeniería Informática",
    "Análisis, validación y depuración de software",
    "Análisis y especificación de requisitos",
    "Animation and design of videogames",
    "Aprendizaje automático",
    "Arquitectura y entornos de desarrollo para videoconsolas",
    "Bioinformática",
    "Calidad y optimización",
    "Ciberseguridad en dispositivos móviles",
    "Competición de programación",
    "Computación científica",
    "Computación en la Nube y de Altas Prestaciones",
    "Criptografía",
    "Desarrollo centrado en el usuario",
    "Desarrollo de aplicaciones para dispositivos móviles",
    "Desarrollo de Videojuegos 2D",
    "Desarrollo de Videojuegos 3D",
    "Diseño de sistemas basados en FPGA",
    "Diseño de sitios web",
    "Diseño y gestión de bases de datos",
    "Diseño y gestión de sistemas de información genómicos",
    "Diseño y Modelado 3D",
    "Edición y postproducción de vídeo digital",
    "Français scientifique et technique - A2",
    "Français scientifique et technique - B1",
    "Francés académico y profesional A1",
    "Francés académico y profesional A2",
    "Francés académico y profesional B1",
    "Francés académico y profesional B2",
    "Gestión de la innovación y tecnología en salud",
    "Hacking ético",
    "Impresión 3D",
    "Informática médica",
    "Integración de aplicaciones",
    "Integración e interoperabilidad",
    "Intercambio académico I",
    "Intercambio académico II",
    "Intercambio académico III",
    "Intercambio académico IV",
    "Intercambio académico IX",
    "Intercambio académico V",
    "Intercambio académico VI",
    "Intercambio académico VIII",
    "Introducción a los sistemas gráficos interactivos",
    "Italiano académico y profesional A1",
    "Italiano académico y profesional A2",
    "Lenguajes de programación y procesadores de lenguajes",
    "Mantenimiento y evolución de software",
    "Mecatrónica",
    "Modelos de negocio y áreas funcionales de la organización",
    "Programación de Sistemas Distribuidos",
    "Programación de Sistemas Empotrados",
    "Proyecto de ingeniería de software",
    "Quantum computing",
    "Redes corporativas",
    "Redes multimedia",
    "Seguridad en los sistemas informáticos",
    "Seguridad en redes y sistemas informáticos",
    "Seguridad web",
    "Sistemas de información estratégicos",
    "Sistemas integrados de información en las organizaciones",
    "Sistemas multimedia interactivos e inmersivos",
    "Sistemas robotizados",
    "Sistemas y servicios en red",
    "Social web behaviour & network analysis",
    "Técnicas, entornos y aplicaciones de inteligencia artificial",
    "Tecnologías avanzadas para redes corporativas y Datacenters",
    "Valencià tècnic - C1",
    "Valencià tècnic - C2"
]

def crear_columnas(asignaturas, curso, max_asignaturas=10):
    n = min(max_asignaturas, len(asignaturas))
    seleccion = random.sample(asignaturas, n)
    cols = {}
    for asig in seleccion:
        colname = f"{curso}_{asig}"
        cols[colname] = {ct: random.randint(0, 3) for ct in competencias}
    return cols

columns_data = {}
columns_data.update(crear_columnas(asignaturas_1, 1))
columns_data.update(crear_columnas(asignaturas_2, 2))
columns_data.update(crear_columnas(asignaturas_3, 3))
columns_data.update(crear_columnas(asignaturas_4, 4))

df = pd.DataFrame(columns_data)
df = df.reindex(competencias) 
df.index.name = 'Competencia'

with pd.ExcelWriter('ejemplo2.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='CT_Asignaturas', index=True)