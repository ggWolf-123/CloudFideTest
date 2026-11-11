import operator
import ast
import pandas as pd

OPERATORS={
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul
}

def is_valid_label(label: object)->bool:
    if (isinstance(label,str) and bool(label) 
        and all(character.isalpha() or character =="_" for character in label)):
        return True
    return False

def evaluation_of_expression(node: ast.AST, df: pd.DataFrame)->pd.Series:
    if not isinstance(node,ast.BinOp):
        raise ValueError("Expression must have one binary operation")
    operation=OPERATORS.get(type(node.op))
    if operation is None:
        raise ValueError("Operation is unsupported")
    if not (isinstance(node.left, ast.Name)
            or isinstance(node.right, ast.Name)):
        raise ValueError("Only names of columns are allowed")

    l_name=node.left.id
    r_name=node.right.id

    if l_name not in df.columns or l_name not in df.columns:
        raise ValueError("Column unknown")

    return operation(df[l_name],df[r_name])

def add_virtual_column(
        df:pd.DataFrame,
        role:str,
        new_column_name:str,
)->pd.DataFrame:
    if not isinstance(df,pd.DataFrame):
        return pd.DataFrame([])
    if not isinstance(role,str):
        return pd.DataFrame([])
    if not df.columns.is_unique:
        return pd.DataFrame([])
    if not is_valid_label(new_column_name):
        return pd.DataFrame([])
    if not all(is_valid_label(label) for label in df.columns):
        return pd.DataFrame([])

    try:
        syntax_tree=ast.parse(role.strip(), mode="eval")
        result=evaluation_of_expression(syntax_tree.body, df=df)
    except(SyntaxError,ValueError,TypeError,KeyError, ZeroDivisionError):
        return pd.DataFrame([])
    out=df.copy()
    out[new_column_name]=result
    return out