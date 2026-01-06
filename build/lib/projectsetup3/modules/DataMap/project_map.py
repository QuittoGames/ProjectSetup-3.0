from projectsetup3.modules.Interfaces.BaseProject import BaseProject
from projectsetup3.modules.Enums.ProjectType import ProjectType
from pathlib import Path

class ProjectMaps:
    project_map = {}

    for pt in ProjectType:
        # Cria dinamicamente a classe
        cls_name = f"{pt.name.capitalize()}Project"
        cls = type(
            cls_name,
            (BaseProject,),
            {
                "language": pt,
                "basestruture": {}  # JSON carregável depois
            }
        )
        # Mapear pelo nome do tipo (recomendado)
        project_map[pt.name.lower()] = cls

        # Mapear pelo valor do Enum também (opcional)
        project_map[pt.value.lower()] = cls
