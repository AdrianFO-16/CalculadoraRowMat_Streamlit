import streamlit as st
import operator
import numpy as np
import re
import pandas as pd


st.set_page_config(
     #layout="wide",
     page_title="Calculadora RowMat"
 )

def matrix_row_operations(query):  
  temp_res = None

  row = re.findall(rows, query)
  coefs = re.findall(coef, query)
  opes = re.findall(op, query)

  if re.search(two_row_op, query) != None:
    #print("Two Row Operation")
    type_op.success("Operación con dos filas")
    temp_res = matrix.copy().astype("float32")
    if len(coefs)!= 0: #There is coeficient
      coef_ = coefs[0].split("/")
      if len(coef_)==1:#Single number
        coef_ = float(coefs[0][:-1])
        temp_res[int(row[0][1])-1][:] = ops[opes[0][0]](matrix[int(row[1][1])-1][:],coef_*matrix[int(row[2][1])-1][:])
      else:#Fraction
        coef_num =  int(coef_[0])
        coef_denom = int(coef_[1][0])
        temp_res[int(row[0][1])-1][:] = ops[opes[0][0]](matrix[int(row[1][1])-1][:],coef_num/coef_denom*matrix[int(row[2][1])-1][:])
    else:#There is not coeficient
      coef_ = 1
      coefs = ["1*"]
      temp_res[int(row[0][1])-1][:] = ops[opes[0][0]](matrix[int(row[1][1])-1][:], matrix[int(row[2][1])-1][:])
      
      
    #print(f"Row {row[0][1]}->Row {row[1][1]} {opes[0][0]} {coefs[0]} Row {row[2][1]}")
    
  elif re.search(one_row_op, query) != None:
    #print("One Row Operation")
    type_op.success("Operación con una fila")
    if row[0][1] == row[1][1]:
      temp_res = matrix.copy().astype("float32")
      if len(coefs)!= 0: #There is coeficient
        coef_ = coefs[0].split("/")
        if len(coef_)==1:#Single number
          coef_ = float(coefs[0][:-1])
          temp_res[int(row[0][1])-1][:] = coef_*matrix[int(row[1][1])-1][:]
        else:#Fraction
          coef_num =  int(coef_[0])
          coef_denom = int(coef_[1][0])
          temp_res[int(row[0][1])-1][:] = coef_num/coef_denom*matrix[int(row[1][1])-1][:]
      else:#There is not coeficient
        if len(opes)!=0:
          coef_ = -1
          coefs = ["-1*"]
        else: 
          coef_ = 1
          coefs = ["1*"]
        temp_res[int(row[0][1])-1][:] =  coef_*matrix[int(row[1][1])-1][:]

      #print(f"Row {row[0][1]}->{coefs[0]}Row {row[1][1]}")
    else:
      #print("Operacion invalida")
      type_op.error("Operación inválida")
    
  elif re.search(row_sust, query) != None:
    #print("Row Substitution")
    type_op.success("Sustitución de filas")
    temp_res = matrix.copy().astype("float32")
    temp_row = matrix[int(row[0][1])-1][:]
    temp_res[int(row[0][1])-1][:] = matrix[int(row[1][1])-1][:]
    temp_res[int(row[1][1])-1][:] = temp_row

    #print(f"Row {row[0][1]}<->Row {row[1][1]}")

  else:
    #print("Formato de entrada invalido")
    type_op.error("Formato de entrada invalido")

  return temp_res
  #print("---------------------------------------------")
  #print(matrix)
  #print("---------------------------------------------")
  #print(temp_res)
  #print("=============================================")

ops = {
    '+' : operator.add,
    '-' : operator.sub
}

rows = "R[0-9]+"

coef = "([0-9]+\*|[0-9]+/[0-9]+\*|[0-9]+\.[0-9]+\*)"

op = "([+\-][0-9]|[+\-]R)"

matrix = np.array([
                   [6,6,1],
                   [2,3,0],
                   [4,5,9]
]).astype("float32")

columns_ = [x+1 for x in range(len(matrix[0]))]
index_ = [x+1 for x in range(len(matrix))]

two_row_op= "R[0-9]+->R[0-9]+[+\-](([0-9]+\*|[0-9]+/[0-9]+\*)|[0-9]+\.[0-9]+\*|)R[0-9]+"

one_row_op = "R[0-9]+->[-]*(([0-9]+\*|[0-9]+/[0-9]+\*)|[0-9]+\.[0-9]+\*|)R[0-9]+"

row_sust = "R[0-9]+<->R[0-9]+"


st.markdown("<h1 style='text-align: center; color: black; font-family: timesnewroman;'>Calculadora de operaciones con filas de matrices</h1>", unsafe_allow_html=True)



query = st.text_input("Operación", value= "R1->R1")
type_op = st.empty()


st.header("Original")
st.dataframe(pd.DataFrame(matrix, columns =columns_, index = index_ ))


st.header("Resultante")
res = matrix_row_operations(query)
st.dataframe(pd.DataFrame(res, columns = columns_, index = index_))






