**AGRO-IQ*** 
AGRO-IQ es una plataforma inteligente orientada a la analítica, simulación y toma de
decisiones estratégicas para el sector agropecuario. El sistema implementa una arquitectura
basada en agentes inteligentes autónomos (orquestador, estrategia, auditoría y analítica)
combinada con un potente dashboard interactivo.
️ Estructura del Proyecto
El repositorio está organizado como un monorepo dividido en dos componentes principales:
● backend-agro/: Sistema de backend desarrollado en Python. Implementa arquitectura
hexagonal (puertos y adaptadores) y un ecosistema de agentes basados en LLMs para
procesamiento y auditoría de datos agrícolas.
● frontend-agro/: Interfaz de usuario web construida con Next.js, React y TypeScript,
diseñada para visualizar dashboards analíticos, métricas de resiliencia y controles de
simulación en tiempo real.
 *Tecnologías Utilizadas*
Backend
● Lenguaje: Python 3.14+
● Base de Datos: SQLite (agro_iq.db)
● Core: Arquitectura de Agentes Inteligentes (Orchestrator, Strategy Agent, Auditor Agent,
Analytics).
● Integraciones: Microsoft IQ API para ingesta y validación de datos del sector.
Frontend
● Framework: Next.js (App Router)
● Lenguaje: TypeScript
● Estilos: Tailwind CSS / Custom Design Tokens
● Herramientas de Calidad: ESLint

*Configuración e Instalación*
Requisitos Previos
● Python 3.14 o superior instalado.
● Node.js (versión LTS recomendada) y npm/pnpm.

1. Configuración del Backend 
1. Navega al directorio del backend:
cd backend-agro
2. Crea tu archivo de configuración ambiental a partir de la plantilla:
cp .env.example .env.local
Nota: Asegúrate de configurar tus llaves de API para los servicios de LLM y Microsoft IQ en
.env.local.
3. Si necesitas reiniciar o limpiar la base de datos local SQLite para pruebas, puedes ejecutar:
python clear_bd.py
4. Ejecuta el archivo principal o las pruebas rápidas de agentes para verificar que todo
funcione:
python main.py
python quick_test.py

2. Configuración del Frontend 🌐
1. Navega al directorio del frontend:
cd ../frontend-agro
2. Instala todas las dependencias requeridas:
npm install
3. Inicia el servidor de desarrollo local:
npm run dev
4. Abre tu navegador e ingresa a http://localhost:3000 para interactuar con la plataforma.
🧠 Arquitectura de Agentes (Backend)
El backend delega las tareas complejas a un pipeline especializado de agentes interactivos:
● Orchestrator: Coordina el flujo de información entre el usuario, la base de conocimientos
y los agentes secundarios.
● Strategy Agent: Analiza escenarios económicos y agrícolas para proponer planes de
acción optimizados.
● Auditor Agent: Verifica la consistencia de los datos e historiales antes de consolidar
reportes financieros o de rendimiento.
● Analytics Engine: Procesa simulaciones estadísticas de ROI y distribuciones de riesgo.
Puedes consultar más detalles técnicos sobre el comportamiento de los agentes en el archivo

específico frontend-agro/AGENTS.md.
