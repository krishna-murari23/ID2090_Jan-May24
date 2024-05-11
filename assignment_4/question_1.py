import yaml
from sympy import * #Imports all functions from the sympy library
import re
import sys

def check_hermitian(matrix): #Hermitian Matrices are ones which satisfy A = ComplexConjugateTranspose(A)
    return matrix.is_hermitian

def check_unitary(matrix):
    return matrix * matrix.adjoint() == eye(matrix.shape[0]) #Unitary Matrices are those that satisfy A*ComplexConjugateTranspose(A) = I

def check_positive_semidefinite(matrix):
    return all(eigenvalue >= 0 for eigenvalue in matrix.eigenvals().keys())

def check_positive_definite(matrix):
    return all(eigenvalue > 0 for eigenvalue in matrix.eigenvals().keys())

def matrix_classification(matrix):
    classifications = []
    if check_hermitian(matrix):
        classifications.append("Hermitian")
    if check_unitary(matrix):
        classifications.append("Unitary")
    if check_positive_semidefinite(matrix):
        classifications.append("Positively Semidefinite")
    if check_positive_definite(matrix):
        classifications.append("Positively Definite")
    if not classifications:
        classifications.append("Normal")
    return classifications

# Put the data in the YAML file from obj.yml using the function yaml.load()U
with open('obj.yml', "r") as file:
    yaml_data = yaml.load(file, Loader=yaml.Loader)

# Define a function to convert nested dictionaries to MutableDenseMatrix(in sympy)
def convert_to_sympy_matrix(data):
    if '_rep' in data and 'state' in data['_rep'] and 'rep' in data['_rep']['state'] and 'dictitems' in data['_rep']['state']['rep']:
        rows, cols = data['rows'], data['cols']
        matrix_data = data['_rep']['state']['rep']['dictitems']
        matrix_list = [[complex(matrix_data[i][j]) if isinstance(matrix_data[i][j], Number) else matrix_data[i][j] for j in range(cols)] for i in range(rows)]
        return MutableDenseMatrix(matrix_list)
    else:
        return None

# Define a function to convert dictionaries to DomainMatrix
def convert_to_domain_matrix(data):
    if 'args' in data and data['args']:
        args = data['args'][0]
        rows, cols = data['_rep']['state']['shape']
        matrix = DomainMatrix(args, rows=rows, shape=(rows, cols))
        return matrix
    else:
        return None

# Convert the YAML file to SymPy matrix or DomainMatrix so it can be operated on by matrix operations
if isinstance(yaml_data, MutableDenseMatrix):
    matrix = yaml_data
elif isinstance(yaml_data, dict):
    matrix = convert_to_sympy_matrix(yaml_data)
    if matrix is None:
        matrix = convert_to_domain_matrix(yaml_data)
else:
    matrix = None

#Eigenvalue List
eigen= matrix.eigenvects(simplify=True)
eigenvecs=[]
eigenvalslist=[]
for eigenvalue,multiplicity,vecs in eigen:
    for i in range(0,multiplicity):
        eigenvecs.append(vecs[i])
    for i in range(0,multiplicity):
        eigenvalslist.append(eigenvalue)

#Eigenvalues
eigenvals=Matrix([eigenvalslist])
print("Eigenvalues:\n")
pprint(eigenvals)
print("\n")

eigenvecsmatrix = eigenvecs[0]
for col in eigenvecs[1:]:
    eigenvecsmatrix = eigenvecsmatrix.row_join(col)

U_cols=Matrix.orthogonalize(*eigenvecs,normalize=True)

#Unitary
U=U_cols[0]
for col in U_cols[1:]:
    U=U.row_join(col)
print("U:\n")
pprint(U)
print("\n")

Ut=U.conjugate().transpose()
D=Ut*matrix*U
print("D:\n")
pprint(D)
print("\n")
print("\nDecomposition:")


dict2={}
for i in range(0,3):
    if eigenvals[i] not in dict2:
        dict2[eigenvals[i]]=U_cols[i] * U_cols[i].transpose()
    else:
        dict2[eigenvals[i]]+=U_cols[i] * U_cols[i].transpose()

for key in dict2:
    print(key,'*')
    pprint(dict2[key])



# Check if the matrix is Hermitian
check_hermitian = matrix == matrix.conjugate().transpose()

# Check if the matrix is Unitary
check_unitary = matrix*matrix.conjugate().transpose() == matrix.conjugate().transpose()*matrix == eye(matrix.shape[0])

# Check if the matrix is Positively Semidefinite
check_pos_semidefinite = all(eigenvalue >= 0 for eigenvalue in matrix.eigenvals().keys())

# Check if the matrix is Positively Definite
check_pos_definite = all(eigenvalue > 0 for eigenvalue in matrix.eigenvals().keys())

# Check if the matrix is Normal
check_normal = matrix*matrix.transpose() == matrix.transpose()*matrix

# Output classification of the matrix
classification = "Classification:\n"
if check_hermitian:
    classification += "A is Hermitian"
if check_unitary:
    classification += ", Unitary"
if check_pos_semidefinite:
    classification += ", Positively Semidefinite"
if check_pos_definite:
    classification += ", Positively Definite"
if not any([check_hermitian, check_unitary, check_pos_semidefinite, check_pos_definite]):
    classification += "A is Normal"
classification += "."
print(classification)

