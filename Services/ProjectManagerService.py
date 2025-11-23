# from dataclasses import dataclass

# @dataclass
# class ProjectManagerService:
#     @staticmethod
#     def create_project(name, language):
#         if language not in PROJECTS:
#             raise ValueError("Language not supported.")

#         project_class = PROJECTS[language]
#         return project_class.create(name)