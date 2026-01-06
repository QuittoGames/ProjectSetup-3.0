from dataclasses import dataclass
from projectsetup3.Services.GeminiClient import GeminiClient

@dataclass
class READMEService:
    def genereteREADME(content:str,project_name:str,language:str):
        README_PROMPT = """
                Você é um gerador profissional de README.md para projetos open-source.

                Crie um README.md COMPLETO e BEM FORMATADO em Markdown para o projeto abaixo.

                Nome do projeto:
                {project_name}

                Descrição do projeto:
                {project_description}

                Linguagem principal:
                {language}

                Requisitos do README:
                - Título com emoji discreto
                - Badges (linguagem, versão, licença MIT)
                - Descrição clara e objetiva
                - GIF ou animação de demonstração (use um placeholder de imagem/GIF)
                - Seção de funcionalidades
                - Instalação passo a passo
                - Como usar (exemplos de comandos)
                - Estrutura de pastas (genérica)
                - Tecnologias utilizadas
                - Contribuição
                - Licença MIT

                Regras:
                - Use Markdown padrão do GitHub
                - Não invente links reais, use placeholders quando necessário
                - Use um tom profissional e moderno
                - Não seja excessivamente longo
        """

        IAService = GeminiClient() #Modify Model if you want
        return IAService.generteText(README_PROMPT)
