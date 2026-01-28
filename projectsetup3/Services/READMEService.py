from dataclasses import dataclass
from projectsetup3.Services.GeminiClient import GeminiClient

@dataclass
class READMEService:
    @staticmethod
    def genereteREADME(content:str,project_name:str,language:str,strutureProject:dict):
        # Formata a estrutura do projeto em formato de árvore
        structure_tree = "```\n"
        structure_tree += f"{project_name}/\n"
        for file_path in sorted(strutureProject.keys()):
            if "/" in file_path:
                # Arquivo em subpasta
                parts = file_path.split("/")
                indent = "    " * (len(parts) - 1)
                structure_tree += f"{indent}├── {parts[-1]}\n"
            else:
                # Arquivo na raiz
                structure_tree += f"├── {file_path}\n"
        structure_tree += "```"
        
        README_PROMPT = f"""
                Você é um gerador profissional de README.md para projetos open-source.

                Crie um README.md COMPLETO, BEM FORMATADO e PROFISSIONAL em Markdown para o projeto abaixo.

                Nome do projeto:
                {project_name}

                Descrição do projeto:
                {content}

                Linguagem principal:
                {language}

                ESTRUTURA DO PROJETO QUE SERÁ GERADA:
                Esta é a estrutura de arquivos e pastas que o projeto terá. Use isso para entender a organização e arquitetura do projeto.
                
                {structure_tree}

                IMPORTANTE: Use esta estrutura na seção "📁 Estrutura de pastas" do README. 
                Analise os arquivos presentes para entender melhor o propósito e funcionalidade do projeto.
                Por exemplo:
                - Se há requirements.txt ou pyproject.toml → é um projeto Python com dependências
                - Se há src/ ou app/ → código fonte organizado em módulos
                - Se há tests/ → projeto com testes automatizados
                - Se há docker-compose.yml → projeto containerizado
                - Se há .github/workflows/ → CI/CD configurado

                BANCO DE DADOS DE BADGES DISPONÍVEIS:
                Escolha APENAS os badges relevantes para o projeto baseado na descrição fornecida.

                Linguagens:
                - Python: [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
                - JavaScript: [![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
                - TypeScript: [![TypeScript](https://img.shields.io/badge/TypeScript-4.0+-blue.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
                - Java: [![Java](https://img.shields.io/badge/Java-11+-red.svg?logo=java&logoColor=white)](https://www.oracle.com/java/)
                - Go: [![Go](https://img.shields.io/badge/Go-1.18+-00ADD8.svg?logo=go&logoColor=white)](https://golang.org/)
                - Rust: [![Rust](https://img.shields.io/badge/Rust-1.60+-orange.svg?logo=rust&logoColor=white)](https://www.rust-lang.org/)
                - C++: [![C++](https://img.shields.io/badge/C++-17+-blue.svg?logo=cplusplus&logoColor=white)](https://isocpp.org/)
                - C#: [![C#](https://img.shields.io/badge/C%23-10.0+-purple.svg?logo=csharp&logoColor=white)](https://docs.microsoft.com/en-us/dotnet/csharp/)
                - Ruby: [![Ruby](https://img.shields.io/badge/Ruby-3.0+-red.svg?logo=ruby&logoColor=white)](https://www.ruby-lang.org/)
                - PHP: [![PHP](https://img.shields.io/badge/PHP-8.0+-purple.svg?logo=php&logoColor=white)](https://www.php.net/)

                Frameworks:
                - React: [![React](https://img.shields.io/badge/React-18+-61DAFB.svg?logo=react&logoColor=black)](https://reactjs.org/)
                - Vue: [![Vue](https://img.shields.io/badge/Vue-3+-4FC08D.svg?logo=vue.js&logoColor=white)](https://vuejs.org/)
                - Angular: [![Angular](https://img.shields.io/badge/Angular-14+-DD0031.svg?logo=angular&logoColor=white)](https://angular.io/)
                - Django: [![Django](https://img.shields.io/badge/Django-4.0+-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
                - Flask: [![Flask](https://img.shields.io/badge/Flask-2.0+-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
                - FastAPI: [![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
                - Spring: [![Spring](https://img.shields.io/badge/Spring-5.3+-6DB33F.svg?logo=spring&logoColor=white)](https://spring.io/)
                - Express: [![Express](https://img.shields.io/badge/Express-4.18+-000000.svg?logo=express&logoColor=white)](https://expressjs.com/)
                - Next.js: [![Next.js](https://img.shields.io/badge/Next.js-13+-black.svg?logo=next.js&logoColor=white)](https://nextjs.org/)

                Bibliotecas UI/CLI:
                - Rich: [![Rich](https://img.shields.io/badge/UI-Rich-cyan.svg?logo=python)](https://github.com/Textualize/rich)
                - Tailwind: [![Tailwind](https://img.shields.io/badge/Tailwind-3.0+-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
                - Bootstrap: [![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-7952B3.svg?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
                - Material-UI: [![Material-UI](https://img.shields.io/badge/Material--UI-5.0+-0081CB.svg?logo=material-ui&logoColor=white)](https://mui.com/)

                Banco de Dados:
                - PostgreSQL: [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
                - MongoDB: [![MongoDB](https://img.shields.io/badge/MongoDB-5.0+-47A248.svg?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
                - MySQL: [![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1.svg?logo=mysql&logoColor=white)](https://www.mysql.com/)
                - Redis: [![Redis](https://img.shields.io/badge/Redis-7.0+-DC382D.svg?logo=redis&logoColor=white)](https://redis.io/)
                - SQLite: [![SQLite](https://img.shields.io/badge/SQLite-3.36+-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

                Inteligência Artificial:
                - Gemini: [![AI](https://img.shields.io/badge/AI-Gemini-orange.svg?logo=google)](https://ai.google.dev/)
                - OpenAI: [![OpenAI](https://img.shields.io/badge/AI-OpenAI-412991.svg?logo=openai&logoColor=white)](https://openai.com/)
                - TensorFlow: [![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-FF6F00.svg?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
                - PyTorch: [![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org/)
                - Hugging Face: [![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-FFD21E.svg?logo=huggingface&logoColor=black)](https://huggingface.co/)

                Plataformas/Deploy:
                - Docker: [![Docker](https://img.shields.io/badge/Docker-20.10+-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
                - Kubernetes: [![Kubernetes](https://img.shields.io/badge/Kubernetes-1.24+-326CE5.svg?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
                - AWS: [![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900.svg?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
                - Azure: [![Azure](https://img.shields.io/badge/Azure-Cloud-0078D4.svg?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)
                - Heroku: [![Heroku](https://img.shields.io/badge/Heroku-Deploy-430098.svg?logo=heroku&logoColor=white)](https://www.heroku.com/)

                Status/Outros:
                - Licença MIT: [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
                - Plataforma: [![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)]()
                - Status Beta: [![Beta](https://img.shields.io/badge/Status-Beta-yellow.svg)]()
                - Em Desenvolvimento: [![Dev](https://img.shields.io/badge/Status-In%20Development-blue.svg)]()
                - Produção: [![Production](https://img.shields.io/badge/Status-Production-green.svg)]()
                - Build: [![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()

                REQUISITOS DO README:
                1. Título com emoji discreto e profissional
                2. Badges REAIS - SELECIONE do banco de dados acima APENAS os badges relevantes para o projeto
                3. Descrição clara, objetiva e profissional baseada na descrição fornecida
                4. GIF/screenshot de demonstração (use placeholder: https://via.placeholder.com/800x400.png?text=Project+Demo)
                5. ✨ Funcionalidades principais (baseadas na descrição)
                6. 📦 Instalação passo a passo (comandos reais)
                7. 🚀 Como usar (exemplos práticos de código/comandos)
                8. 📁 Estrutura de pastas (tree structure simplificada)
                9. 🛠️ Tecnologias utilizadas (liste as principais)
                10. 🤝 Como contribuir
                11. 📄 Licença MIT

                REGRAS CRÍTICAS:
                ✅ Use APENAS Markdown padrão do GitHub (sem HTML desnecessário)
                ✅ Selecione badges do banco de dados acima - NÃO invente badges
                ✅ Use URLs reais dos badges fornecidos
                ✅ NÃO invente nomes de empresas, organizações ou autores
                ✅ NÃO crie links quebrados - use apenas os fornecidos ou placeholders óbvios
                ✅ Mantenha tom profissional e técnico
                ✅ Seja conciso mas completo (evite texto excessivo)
                ✅ Base TODO o conteúdo na descrição fornecida pelo usuário
                ✅ Verifique a sintaxe Markdown (links, listas, código)
                ✅ Use blocos de código com linguagem especificada: ```python, ```bash, etc.
                ✅ Estruture o README de forma lógica e fácil de navegar

                IMPORTANTE: Analise a descrição do projeto e escolha SOMENTE os badges relevantes. 
                Exemplo: Se é um projeto Python com FastAPI e PostgreSQL, use APENAS os badges de Python, FastAPI, PostgreSQL, Licença e Plataforma.
                NÃO adicione badges de tecnologias que não são mencionadas na descrição.
        """

        IAService = GeminiClient() #Modify Model if you want
        return IAService.generteText(README_PROMPT)
