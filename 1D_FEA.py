import matplotlib.pyplot as plt
import numpy as np

length = int(input("length of the bar: "))
elem_num = int(input("total element in bar: "))
elem_length = length/elem_num
total_nodes = elem_num + 1

#Material Data
Area = 15
Elasticity = 2000000000
stiffness = Area*Elasticity/elem_length

#creating stiffness matrix

def formSM(elemnum):
    n = elemnum+1
    
    matrix = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(n):
            
            if i == 0:
                if j == 0:
                    matrix[i, j] = 1
                elif j == 1:
                    matrix[i, j] = -1
                    
            elif i == n - 1:
                if j == n - 2:    # Represents column n-1
                    matrix[i, j] = -1
                elif j == n - 1:  # Represents column n
                    matrix[i, j] = 1
                    
            else:
                if i == j:
                    matrix[i, j] = 2
                elif i - j == 1:
                    matrix[i, j] = -1
                elif i - j == -1:
                    matrix[i, j] = -1

    # Print the resulting matrix with stiffness data
    return stiffness*matrix


stiffness_matrix = formSM(elem_num)


#Boundary Condition


bar_matrix = np.zeros((1, elem_num+1), dtype=int)
force_matrix = np.transpose(bar_matrix)
fixed_node = int(input("Which node number is fixed: "))
force_node = int(input("Which node number will experience force: "))
force = input("How much force (N) is being applied to the node: ")

#FEA Calculation


if force_node > elem_num+1:
    print("Node doesn't exist, please enter node as per defined element number (In 1-D Bar, node number = element number +1)")
else:
    force_matrix[force_node-1, 0] = force

fextract = np.concatenate((force_matrix[:fixed_node-1, :], force_matrix[fixed_node:, :]), axis=0)

#reducing those rows who have no calculative effect on acutal FEA calculation due to fixed node having zero deformation to make the solution easy
SM_extracted_no_row = np.delete(stiffness_matrix, fixed_node-1, axis=0)
SM_extracted = np.delete(SM_extracted_no_row, fixed_node-1, axis=1)


deform = np.linalg.solve(SM_extracted, fextract)

print(deform.shape)

finaldeform = np.insert(deform, obj=fixed_node-1, values=0, axis=0)

print(finaldeform)

finalforce = stiffness_matrix @ finaldeform

#print(finalforce)



#contour Visualization


x_coords = np.linspace(0, length, total_nodes)
u_values = finaldeform.flatten()
y_coords = np.linspace(-0.5, 0.5, 10)
X, Y = np.meshgrid(x_coords, y_coords)
Z = np.tile(u_values, (len(y_coords), 1))
print(Z)
plt.figure(figsize=(10, 4)) #opens a contour dialogue box of 10X4 inxin size
contour = plt.contourf(X, Y, Z, levels=21100, cmap='jet') #defines the color mapping
plt.title("Displacement Contour Plot (1D Bar under Axial Load)", fontsize=14, fontweight='bold')
plt.xlabel("Position along the bar (m)", fontsize=11)
plt.ylabel("Bar Thickness Profile", fontsize=11)
plt.yticks([]) 
plt.ylim(-1.5, 1.5) # Add some padding

plt.tight_layout()
plt.show()
