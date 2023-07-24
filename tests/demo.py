from tree_sitter_languages import get_language, get_parser


example = """
#!shebang
# License blah blah (Apache 2.0)
"This is a module docstring."

a = 1

'''This
is
not
a
multiline
comment.'''

b = 2

class Test:
    "This is a class docstring."

    'This is bogus.'

    def test(self):
        "This is a function docstring."

        "Please, no."

        return 1

c = 3

d = "select * from demo;"

d = f"select * from {demo};"

run("select * from demo;")
"""


language = get_language("python")
parser = get_parser("python")


tree = parser.parse(example.encode())
node = tree.root_node
print(node.sexp())


stmt_str_pattern = "(expression_statement (string)) @stmt_str"
stmt_str_query = language.query(stmt_str_pattern)
stmt_strs = stmt_str_query.captures(node)
print("-------")
for node, _ in stmt_strs:
    print(node, _)
stmt_str_points = set((node.start_point, node.end_point) for node, _ in stmt_strs)
print("=======")
print(stmt_str_points)
print("=======")

doc_str_pattern = """
    (module . (comment)* . (expression_statement (string)) @module_doc_str)

    (class_definition
        body: (block . (expression_statement (string)) @class_doc_str))

    (function_definition
        body: (block . (expression_statement (string)) @function_doc_str))
"""
doc_str_query = language.query(doc_str_pattern)
doc_strs = doc_str_query.captures(node)
doc_str_points = set((node.start_point, node.end_point) for node, _ in doc_strs)

comment_strs = stmt_str_points - doc_str_points
print(sorted(comment_strs))


string_pattern = """
[
(call
  function: (identifier)
  arguments: (argument_list (string) @the-string))
 
(assignment
  left: (identifier)
  right: (string) @the-string)
] 
"""
stmt_str_query = language.query(string_pattern)
stmt_strs = stmt_str_query.captures(tree.root_node)
print("----xxx---")
for node, _ in stmt_strs:
    print(node, _, node.text)
stmt_str_points = set((node.start_point, node.end_point) for node, _ in stmt_strs)
print("=======")