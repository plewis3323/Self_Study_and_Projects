


import numpy as np

def gaussian_elimination(A):
    n = A.shape[0]
    for i in range(n):
        # Search for maximum in this column
        max_el = abs(A[i][i])
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > max_el:
                max_el = abs(A[k][i])
                max_row = k

        # Swap maximum row with current row (column by column)
        A[[i, max_row]] = A[[max_row, i]]

        # Make all rows below this one 0 in current column
        for k in range(i+1, n):
            c = -A[k][i] / A[i][i]
            for j in range(i, n):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]
    return A

def main():
    # Input the size of the square matrix
    n = int(input("Enter the size of the square matrix: "))

    # Input the elements of the matrix
    print(f"Enter the elements of the {n}x{n} matrix row by row:")
    A = np.zeros((n, n))
    for i in range(n):
        row = input().split()
        A[i] = [float(num) for num in row]

    # Perform Gaussian elimination
    A_echelon = gaussian_elimination(A.copy())
    print("Row echelon form of the matrix:")
    print(A_echelon)

    # Calculate eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(A)
    print("Eigenvalues of the matrix:")
    print(eigenvalues)
    print("Eigenvectors of the matrix:")
    print(eigenvectors)

if __name__ == "__main__":
    main()

