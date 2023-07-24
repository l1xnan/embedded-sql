// const Parser = require("web-tree-sitter");
import * as Parser from "web-tree-sitter";

async function pyParser(code: string) {
  await Parser.init();
  const parser = new Parser();
  const Lang = await Parser.Language.load("tree-sitter-python.wasm");
  parser.setLanguage(Lang);
  const tree = parser.parse(code);
  tree.getEditedRange;
  console.log(tree.rootNode.toString());

  let cur = tree.walk();
  while (cur) {
    cur.gotoFirstChild();
    console.log(cur.nodeIsNamed, cur.startPosition, cur.endPosition);
  }
}

const code = `
x = """
select * from demo
"""
`;
pyParser(code).then((res) => {});
