# from pathlib import Path
# import ast
#
#
# def find_evaluator_scripts():
#     evaluator_scripts = set()
#     path = Path(__file__).parent
#     for file_path in path.rglob('*.py'):
#         if file_path.is_file():
#             with file_path.open('r', encoding='utf-8') as file:
#                 file_content = file.read()
#                 try:
#                     tree = ast.parse(file_content)
#                     has_imports = any(
#                         isinstance(node, (ast.Import, ast.ImportFrom))
#                         for node in ast.walk(tree)
#                     )
#                     has_eval_main = any(
#                         isinstance(node, ast.FunctionDef) and node.name == 'eval_main'
#                         for node in ast.walk(tree)
#                     )
#                     if has_eval_main or has_imports:
#                         module_name = file_path.relative_to(path).with_suffix('').as_posix().replace('/', '.')
#                         evaluator_scripts.add(module_name)
#                 except SyntaxError:
#                     continue
#     return sorted(list(evaluator_scripts))
#
#
# de_scripts = find_evaluator_scripts()
__all__ = ['CRS02']