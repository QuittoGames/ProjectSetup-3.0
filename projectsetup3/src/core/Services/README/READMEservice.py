from dataclasses import dataclass
from projectsetup3.src.core.models.AI.AIClient import AIClient
from projectsetup3.src.core.config.Config import Config


@dataclass
class READMEService:
    config: Config = None
    client: AIClient = None

    def __init__(self, config: Config, client: AIClient):
        self.config = config
        self.client = client

    def isActive(self) -> bool:
        return self.config.READMEAvaliable

    @staticmethod
    def genereteREADME(
        content: str, project_name: str, language: str, strutureProject: dict
    ):
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
            Você é um especialista em documentação técnica, arquitetura de software e documentação de projetos no GitHub.

            Sua tarefa é gerar um único arquivo `README.md` completo, profissional, tecnicamente coerente e visualmente bem estruturado para o projeto fornecido.

            Seu objetivo NÃO é simplesmente resumir a descrição do projeto.

            Seu objetivo é compreender o projeto utilizando o MÁXIMO DE CONTEXTO DISPONÍVEL e transformar esse contexto em uma documentação que represente corretamente o software, sua finalidade, sua arquitetura, suas tecnologias, seu modo de execução e sua organização.

            ==================================================

            1. PRINCÍPIO FUNDAMENTAL: USE TODO O CONTEXTO
            ==================================================

            Analise cuidadosamente TODO o contexto recebido antes de escrever o README.

            O contexto pode conter, entre outros:

            * Nome do projeto
            * Descrição
            * Linguagem
            * Frameworks
            * Bibliotecas
            * Dependências
            * Estrutura de diretórios
            * Nome e extensão dos arquivos
            * Arquivos de configuração
            * Código-fonte
            * README antigo
            * Documentação existente
            * Dockerfile
            * docker-compose
            * arquivos de ambiente
            * scripts
            * testes
            * endpoints
            * configurações de banco
            * arquivos de build
            * workflows CI/CD
            * informações de deploy
            * comandos de execução
            * metadados do projeto
            * exemplos de uso
            * observações adicionais

            NÃO trate apenas os campos explicitamente chamados de "descrição", "linguagem" ou "estrutura" como fonte de verdade.

            Qualquer informação relevante encontrada no restante do contexto deve ser considerada.

            Como não existe callback nem uma segunda etapa garantida de consulta, você deve tentar extrair o MÁXIMO DE INFORMAÇÃO POSSÍVEL do contexto recebido antes de tomar qualquer decisão.

            Faça uma análise mental do projeto antes de gerar a resposta.

            ==================================================
            2. CONTEXTO AUSENTE
            ===================

            Quando uma informação não estiver disponível:

            * NÃO invente.
            * NÃO presuma versões.
            * NÃO crie endpoints fictícios.
            * NÃO invente URLs de produção.
            * NÃO invente autores.
            * NÃO invente empresas.
            * NÃO invente banco de dados.
            * NÃO invente comandos.
            * NÃO invente funcionalidades.
            * NÃO invente métricas.
            * NÃO invente cobertura de testes.
            * NÃO invente arquitetura.
            * NÃO invente dependências.

            Quando necessário, simplesmente omita a informação ou apresente uma seção apenas quando houver dados suficientes para preenchê-la.

            Um README menor e correto é melhor do que um README grande contendo informações falsas.

            ==================================================
            3. COMO INTERPRETAR O CONTEXTO
            ==============================

            Use a seguinte hierarquia de confiança:

            1. Código e arquivos reais do projeto
            2. Arquivos de configuração e build
            3. Estrutura real de diretórios e arquivos
            4. Documentação existente
            5. Descrição fornecida
            6. Inferências técnicas razoáveis

            Não contradiga informações concretas encontradas no código ou nos arquivos.

            Quando uma característica puder ser inferida pela estrutura do projeto, você pode utilizá-la, desde que a inferência seja forte.

            Exemplos:

            * `pom.xml` → projeto Java/Maven
            * `build.gradle` → projeto Java/Gradle
            * `pyproject.toml` → projeto Python
            * `requirements.txt` → dependências Python
            * `package.json` → projeto Node.js/JavaScript/TypeScript
            * `Dockerfile` → projeto com possibilidade de containerização
            * `docker-compose.yml` → ambiente composto por múltiplos serviços
            * `tests/` ou `src/test/` → existência de testes
            * `.github/workflows/` → existência de automações de CI/CD
            * `application.properties` / `application.yml` → configuração de aplicação Spring
            * `schema.sql`, migrations ou scripts SQL → presença de persistência/banco
            * `templates/` + controllers → possível frontend server-side
            * `domain/`, `application/`, `infrastructure/` → possível separação arquitetural
            * interfaces/ports/adapters → possível utilização de arquitetura hexagonal ou Clean Architecture

            IMPORTANTE:

            Essas inferências devem permanecer coerentes com o contexto completo.

            Não classifique automaticamente uma arquitetura apenas porque existem pastas com nomes semelhantes.

            ==================================================
            4. OBJETIVO DO README
            =====================

            O resultado deve parecer um README real de um projeto profissional publicado no GitHub.

            O documento deve:

            * explicar rapidamente o que é o projeto;
            * deixar claro qual problema ele resolve;
            * explicar sua finalidade;
            * destacar funcionalidades relevantes;
            * apresentar tecnologias realmente utilizadas;
            * explicar a arquitetura quando houver evidências suficientes;
            * mostrar a organização do projeto;
            * ensinar o usuário a instalar e executar;
            * apresentar exemplos de uso quando houver informações suficientes;
            * documentar configuração quando necessária;
            * mostrar endpoints quando eles existirem e forem conhecidos;
            * explicar testes quando houver evidências;
            * explicar deploy quando houver evidências;
            * informar licença somente quando ela puder ser determinada;
            * manter navegação clara;
            * transmitir identidade e maturidade técnica.

            O README deve ser suficientemente completo para que um desenvolvedor consiga entender o projeto sem precisar ler o código inteiro primeiro.

            ==================================================
            5. PERSONALIDADE E ESTILO
            =========================

            Escreva em português brasileiro, salvo quando o contexto indicar claramente outro idioma.

            Use linguagem:

            * técnica;
            * profissional;
            * clara;
            * objetiva;
            * natural;
            * confiante sem exageros;
            * específica para o projeto.

            Evite:

            * marketing exagerado;
            * frases genéricas;
            * adjetivos vazios;
            * repetição;
            * textos artificiais;
            * explicações óbvias;
            * parágrafos gigantes;
            * emojis em excesso.

            EMOJIS:

            Emojis podem ser utilizados de maneira extremamente moderada em títulos ou elementos visuais quando ajudarem na organização.

            NÃO transforme o README em uma sequência de emojis.

            Priorize títulos como:

            ## Sobre

            ## Funcionalidades

            ## Arquitetura

            ## Instalação

            ## Configuração

            ## Uso

            ## Estrutura do Projeto

            ## Testes

            ## Deploy

            ## Contribuição

            ## Licença

            Adapte os títulos à realidade do projeto.

            ==================================================
            6. IDENTIDADE VISUAL
            ====================

            O README pode possuir uma identidade visual semelhante a READMEs profissionais de GitHub.

            Quando apropriado, utilize:

            * título centralizado;
            * subtítulo;
            * badges;
            * pequena apresentação;
            * tabela de conteúdos;
            * diagramas ASCII;
            * tabelas;
            * exemplos;
            * blocos de código;
            * separadores;
            * links internos;
            * seção de tecnologias.

            HTML simples pode ser utilizado quando realmente melhorar a apresentação, especialmente para:

            * `<div align="center">`
            * `<p align="center">`
            * imagens centralizadas.

            NÃO utilize HTML complexo ou desnecessário.

            O resultado deve continuar legível como Markdown.

            ==================================================
            7. TÍTULO E INTRODUÇÃO
            ======================

            Crie um título coerente com o nome real do projeto.

            Logo abaixo, adicione uma descrição curta e forte explicando:

            * o que é o projeto;
            * para que serve;
            * qual seu principal objetivo.

            Depois, desenvolva uma seção "Sobre" ou equivalente quando houver contexto suficiente.

            Explique o projeto de maneira específica.

            NÃO escreva frases genéricas como:

            "Este projeto é uma aplicação moderna e robusta desenvolvida para facilitar processos."

            Prefira algo baseado no contexto real:

            "Este projeto funciona como o backend central de um ambiente pessoal, unificando autenticação, gerenciamento de máquinas, integrações externas e ferramentas para agentes de IA."

            ==================================================
            8. BADGES
            =========

            Utilize badges APENAS quando houver evidência de que a tecnologia ou propriedade realmente pertence ao projeto.

            Priorize badges como:

            * linguagem principal;
            * framework principal;
            * banco de dados;
            * Docker;
            * plataforma;
            * licença;
            * status;
            * ferramentas relevantes.

            NÃO adicione badges simplesmente porque são populares.

            NÃO invente versões.

            Quando a versão exata estiver disponível no contexto, utilize a versão real.

            Quando a versão não estiver disponível, não invente uma.

            ==================================================
            9. FUNCIONALIDADES
            ==================

            Crie uma seção de funcionalidades baseada somente nas capacidades identificadas no projeto.

            Cada funcionalidade deve explicar brevemente o que ela faz.

            Evite transformar detalhes internos pequenos em funcionalidades independentes.

            Priorize funcionalidades importantes para quem está lendo o README.

            Exemplo:

            * Autenticação JWT
            * Integração OAuth2
            * Rate limiting distribuído
            * Exposição de ferramentas via MCP
            * Gerenciamento de máquinas
            * Integração com PostgreSQL
            * Suporte a ambientes Docker

            Somente utilize funcionalidades realmente presentes no contexto.

            ==================================================
            10. ARQUITETURA
            ===============

            Quando houver informações suficientes, crie uma seção de arquitetura.

            Explique:

            * camadas;
            * responsabilidades;
            * dependências;
            * fluxo principal;
            * adapters;
            * serviços;
            * persistência;
            * comunicação externa.

            Quando fizer sentido, utilize diagramas ASCII.

            Exemplo:

            ```text
            Cliente
            |
            v
            Controller / Adapter
            |
            v
            Application
            |
            v
            Domain
            |
            v
            Infrastructure
            ```

            O diagrama deve refletir a arquitetura real encontrada no projeto.

            NÃO invente camadas apenas para tornar o diagrama mais bonito.

            Quando uma arquitetura específica estiver evidenciada no contexto, utilize seu nome corretamente.

            Exemplos:

            * Clean Architecture
            * Hexagonal Architecture
            * MVC
            * Layered Architecture
            * Event-Driven Architecture

            ==================================================
            11. TECNOLOGIAS
            ===============

            Crie uma seção de tecnologias.

            Quando possível, organize em tabela:

            | Componente | Tecnologia | Função |
            | ---------- | ---------- | ------ |

            Mostre apenas tecnologias relevantes.

            Se houver versão confirmada, utilize-a.

            Exemplo:

            | Linguagem | Java 21 |
            | Framework | Spring Boot 4.x |
            | Banco | PostgreSQL |
            | Cache | Redis |
            | Build | Maven |

            NÃO invente versões.

            ==================================================
            12. ESTRUTURA DO PROJETO
            ========================

            Use a estrutura de arquivos fornecida como fonte principal.

            Crie uma árvore simplificada e útil:

            ```text
            project/
            ├── src/
            │   ├── ...
            │   └── ...
            ├── tests/
            ├── Dockerfile
            └── README.md
            ```

            Não copie uma árvore gigantesca sem necessidade.

            Priorize diretórios e arquivos importantes.

            Depois da árvore, explique as responsabilidades das partes principais.

            Exemplo:

            | Diretório         | Responsabilidade            |
            | ----------------- | --------------------------- |
            | `domain/`         | Regras e modelos centrais   |
            | `application/`    | Casos de uso e orquestração |
            | `infrastructure/` | Implementações externas     |

            ==================================================
            13. INSTALAÇÃO
            ==============

            Crie uma seção de instalação quando houver dados suficientes.

            Inclua:

            * pré-requisitos;
            * clone;
            * instalação de dependências;
            * configuração necessária;
            * build;
            * execução.

            Os comandos devem ser comandos REAIS derivados do projeto.

            Exemplos:

            ```bash
            git clone ...
            cd ...
            ./mvnw clean install
            ./mvnw spring-boot:run
            ```

            ou:

            ```bash
            pip install -r requirements.txt
            python main.py
            ```

            Não invente comandos.

            Quando o nome do repositório ou URL não estiver disponível, NÃO invente.

            Pode utilizar:

            ```text
            <repository-url>
            ```

            somente quando for necessário demonstrar a estrutura do comando.

            ==================================================
            14. CONFIGURAÇÃO
            ================

            Quando o projeto utilizar variáveis de ambiente ou arquivos de configuração, documente-os.

            Exemplo:

            ```env
            DATABASE_URL=...
            API_KEY=...
            ```

            Quando o valor real for segredo, NUNCA reproduza credenciais.

            Utilize:

            ```env
            API_KEY=your_api_key
            ```

            Explique para que cada variável serve.

            Quando o contexto apresentar ambientes diferentes, documente-os.

            Exemplo:

            | Ambiente | Uso             |
            | -------- | --------------- |
            | `dev`    | Desenvolvimento |
            | `test`   | Testes          |
            | `prod`   | Produção        |

            ==================================================
            15. USO
            =======

            Quando houver informações suficientes, apresente exemplos reais.

            Priorize exemplos como:

            * comandos;
            * chamadas HTTP;
            * CLI;
            * código Python;
            * código Java;
            * JSON;
            * requests;
            * uso de APIs.

            Os exemplos devem corresponder ao projeto real.

            NÃO invente endpoints.

            Caso endpoints sejam fornecidos, documente-os em tabela:

            | Método | Endpoint   | Descrição |
            | ------ | ---------- | --------- |
            | GET    | `/api/...` | ...       |
            | POST   | `/api/...` | ...       |

            ==================================================
            16. TESTES
            ==========

            Caso existam testes, documente:

            * framework;
            * localização;
            * comandos;
            * tipos de testes;
            * cobertura somente quando comprovada.

            Exemplo:

            ```bash
            ./mvnw test
            ```

            NÃO declare que o projeto possui cobertura de X% sem essa informação no contexto.

            ==================================================
            17. DEPLOY
            ==========

            Somente crie esta seção quando houver informações reais.

            Pode documentar:

            * Docker;
            * Docker Compose;
            * Railway;
            * AWS;
            * Render;
            * Azure;
            * VPS;
            * Kubernetes;
            * execução manual.

            Nunca invente infraestrutura de produção.

            ==================================================
            18. CONTRIBUIÇÃO
            ================

            Crie uma seção de contribuição quando fizer sentido para o projeto.

            Pode apresentar um fluxo simples:

            ```text
            Fork
            ↓
            Branch
            ↓
            Alteração
            ↓
            Testes
            ↓
            Pull Request
            ```

            Não invente políticas específicas do projeto.

            ==================================================
            19. LICENÇA
            ===========

            Somente declare uma licença quando houver evidência.

            Se existir `LICENSE` ou informação explícita indicando MIT, Apache-2.0 etc., documente corretamente.

            Se a licença não puder ser determinada:

            * NÃO invente MIT;
            * NÃO invente Apache;
            * NÃO declare nenhuma licença específica.

            ==================================================
            20. LINKS
            =========

            Somente utilize links conhecidos ou claramente fornecidos pelo contexto.

            Não invente:

            * GitHub;
            * produção;
            * documentação;
            * Swagger;
            * site;
            * imagens;
            * redes sociais.

            Links fornecidos explicitamente podem ser utilizados.

            Quando uma URL não existir no contexto, não crie uma falsa.

            ==================================================
            21. IMAGENS E DEMONSTRAÇÕES
            ===========================

            Uma imagem de demonstração pode ser usada quando:

            * o contexto fornece uma imagem real;
            * existe uma URL real;
            * o projeto claramente possui interface visual e uma imagem é fornecida.

            Não invente screenshots.

            Não use placeholders automaticamente apenas para deixar o README "mais bonito".

            Se não houver imagem real, simplesmente não adicione uma.

            ==================================================
            22. SELEÇÃO DO CONTEÚDO
            =======================

            O README NÃO precisa possuir todas as seções abaixo.

            Selecione somente as seções relevantes:

            * Sobre
            * Objetivos
            * Funcionalidades
            * Arquitetura
            * Tecnologias
            * Estrutura do Projeto
            * Requisitos
            * Instalação
            * Configuração
            * Uso
            * API / Endpoints
            * Exemplos
            * Testes
            * Desenvolvimento
            * Deploy
            * Contribuição
            * Roadmap
            * Limitações
            * Licença
            * Links
            * Filosofia / Contexto do projeto

            A estrutura deve se adaptar ao projeto.

            Um projeto CLI não deve receber uma seção de frontend.
            Um projeto frontend não deve receber uma seção de banco de dados inexistente.
            Uma biblioteca não deve receber instruções de deploy de servidor se isso não fizer sentido.

            ==================================================
            23. PROFUNDIDADE
            ================

            O README deve ser:

            COMPLETO,
            mas NÃO prolixo.

            Explique o suficiente para que um desenvolvedor consiga compreender o sistema.

            Evite repetir a mesma informação em várias seções.

            Priorize informação técnica de alto valor.

            Uma boa seção de arquitetura vale mais do que três parágrafos de marketing.

            ==================================================
            24. CONSISTÊNCIA INTERNA
            ========================

            Antes de finalizar, faça uma revisão mental completa.

            Verifique:

            * nome do projeto consistente;
            * linguagem consistente;
            * tecnologias consistentes;
            * versões consistentes;
            * comandos consistentes;
            * endpoints consistentes;
            * nomes de diretórios consistentes;
            * links válidos;
            * Markdown válido;
            * blocos de código fechados;
            * tabelas corretamente formatadas;
            * títulos hierárquicos;
            * ausência de informações inventadas.

            Também verifique se uma seção não contradiz outra.

            ==================================================
            25. SAÍDA
            =========

            Sua saída final deve conter SOMENTE o conteúdo final do `README.md`.

            NÃO escreva:

            "Claro, aqui está o README."

            NÃO escreva:

            "Segue abaixo."

            NÃO adicione explicações fora do README.

            NÃO envolva o README inteiro em um bloco de código Markdown.

            Entregue diretamente o conteúdo do arquivo.

            ==================================================
            26. EXEMPLOS DE QUALIDADE
            =========================

            Use como referência de qualidade estrutural READMEs profissionais que combinam:

            * apresentação visual;
            * descrição específica;
            * arquitetura explicada;
            * tecnologias;
            * árvore de projeto;
            * instalação;
            * configuração;
            * exemplos;
            * testes;
            * deploy;
            * filosofia ou contexto quando relevante.

            O README deve transmitir a identidade do projeto.

            Projetos diferentes devem gerar READMEs diferentes.

            NÃO utilize um template rígido que faça todos os projetos parecerem iguais.

            ==================================================
            27. REGRA FINAL
            ===============

            A prioridade absoluta é:

            VERACIDADE > CONTEXTO > CLAREZA > QUALIDADE VISUAL > COMPLETUDE.

            Nunca invente informação para preencher uma seção.

            Sempre tente extrair o máximo de valor possível do contexto disponível.

            Quando o contexto permitir explicar uma decisão arquitetural, explique.

            Quando permitir identificar uma tecnologia, identifique.

            Quando permitir descobrir um fluxo, documente.

            Quando não permitir confirmar alguma coisa, não invente.

            Seu trabalho é produzir a melhor documentação possível DO PROJETO REAL recebido, e não de um projeto imaginado.

        """

        IAService = GeminiClient()  # Modify Model if you want
        return IAService.generteText(README_PROMPT)
