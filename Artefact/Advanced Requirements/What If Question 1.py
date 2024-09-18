import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


df = pd.read_csv('applesdataset.csv')

#Creates three datasets from the three Categorical data points under the variable 'osaseveritypostqc' in the main database
mildData = df[df['osaseveritypostqc'] == '1) mild']
moderateData = df[df['osaseveritypostqc'] == '2) moderate']
severeData = df[df['osaseveritypostqc'] == '3) severe']

#Calculates the mean of the two numerical variables 'rdinrempsg' and 'desatindextot' from the three datasets
avgXMild = mildData['rdinrempsg'].mean()
avgXModerate = moderateData['rdinrempsg'].mean()
avgXSevere = severeData['rdinrempsg'].mean()
avgYMild = mildData['desatindextot'].mean()
avgYModerate = moderateData['desatindextot'].mean()
avgYSevere = severeData['desatindextot'].mean()

#Calculates Standard Deviation
stdDevXmild = mildData['rdinrempsg'].std()
stdDevXmoderate = moderateData['rdinrempsg'].std()
stdDevXsevere = severeData['rdinrempsg'].std()
stdDevYmild = mildData['desatindextot'].std()
stdDevYmoderate = moderateData['desatindextot'].std()
stdDevYsevere = severeData['desatindextot'].std()

# Reads columns and converts to NumPy matrixes
mildMatrix = mildData[['rdinrempsg', 'desatindextot']].to_numpy()
moderateMatrix = moderateData[['rdinrempsg', 'desatindextot']].to_numpy()
severeMatrix = severeData[['rdinrempsg', 'desatindextot']].to_numpy()

mildCorrelationMatrix = np.corrcoef(mildMatrix, rowvar=False) # Calculates correlation coefficient with 'np.corrcoef'.
mildCorrelationCoefficient = mildCorrelationMatrix[0, 1] #specifies the correllation between the 0th and 1st variables
modCorrelationMatrix = np.corrcoef(moderateMatrix, rowvar=False)
modCorrelationCoefficient = modCorrelationMatrix[0, 1]
sevCorrelationMatrix = np.corrcoef(severeMatrix, rowvar=False) 
sevCorrelationCoefficient = sevCorrelationMatrix[0, 1] 


selectedColumns = ['rdinrempsg', 'desatindextot']
columnNames = df.columns   #Stores all column names from the Dataframe to columnNames
selectedColumnNames = columnNames[columnNames.isin(selectedColumns)].tolist()  # Displays the matrices and column names


print('Mild Matrix:')
print(pd.DataFrame(mildMatrix, columns=selectedColumnNames))  # prints mild matrix
print(f"Correlation Coefficient: {mildCorrelationCoefficient}")
print(f"X average: {avgXMild}")
print(f"Y average: {avgYMild}")
print(f"X Standard Deviation: {stdDevXmild}")
print(f"Y Standard Deviation: {stdDevYmild}")

# Duplicate code with different variables
print('Moderate Matrix:')
print(pd.DataFrame(moderateMatrix, columns=selectedColumnNames))
print(f" Correlation Coefficient: {modCorrelationCoefficient}")
print(f"X average: {avgXModerate}")
print(f"Y average: {avgYModerate}")
print(f"X Standard Deviation: {stdDevXmoderate}")
print(f"Y Standard Deviation: {stdDevYmoderate}")

print('Severe Matrix:')
print(pd.DataFrame(severeMatrix, columns=selectedColumnNames))
print(f"Correlation Coeffiecient: {sevCorrelationCoefficient}") 
print(f"X average: {avgXSevere}")
print(f"Y average: {avgYSevere}")
print(f"X Standard Deviation: {stdDevXsevere}")
print(f"Y Standard Deviation: {stdDevYsevere}")


while True:  #Infinite Loop
    var1 = int(input('Which array would you like to analyze? (1 = mild, 2 = moderate, 3 = severe)'))

    if var1 == 1:
        plt.scatter(mildMatrix[:, 0], mildMatrix[:, 1], label='Mild', marker='o') # creates a scatter plot, extracts the values from both variables, sets the label, and sets the marker type as circles
        slope, intercept = np.polyfit(mildMatrix[:, 0], mildMatrix[:, 1], 1)        # Fits the linear regression model (np.polyfit())
        plt.plot(mildMatrix[:, 0], slope * mildMatrix[:, 0] + intercept, color='red', label='Line of Best Fit')   # Plot original line of best fit

        n = float(input('What would you like the data to be changed by?'))  
        mildChangeAvgY = mildCorrelationCoefficient*(n/stdDevXmild)*stdDevYmild  #Calculates the modified average of the Y value if the X values are changed by n 
        modifiedAvgYMild = avgYMild + mildChangeAvgY
        print(f"The original average of the ODI values in the 'Mild' dataset was {avgYMild}, but after your modification to the AHI values, the average of the ODI values is now {modifiedAvgYMild}.")
        print (f"Original Average Points: ({avgXMild}, {avgYMild})")
        print (f"Modified Average Points: ({(avgXMild+n)}, {modifiedAvgYMild})")
        avgydif = modifiedAvgYMild - avgYMild
        print (f"The average difference between the original and modified data is ({n}, {avgydif})")
        modifiedMildMatrix = mildMatrix.copy()   # Copies the original matrix
        modifiedMildMatrix[:, 0] = (modifiedMildMatrix[:, 0] + n).astype(int)  # Extracts values from the first column of the matrix and multiplies them by n
        modifiedMildMatrix[:, 1] = (modifiedMildMatrix[:, 1] + mildChangeAvgY)
        plt.scatter(modifiedMildMatrix[:, 0], modifiedMildMatrix[:, 1], label='ModifiedMild', marker='o', color = 'purple')  # Creates the modified scatter plot
        slopeModified, interceptModified = np.polyfit(modifiedMildMatrix[:, 0], modifiedMildMatrix[:, 1], 1)  #Fits the linear regression model
        plt.plot(modifiedMildMatrix[:, 0], slopeModified * modifiedMildMatrix[:, 0] + interceptModified, color='red', label='Modified Line of Best Fit')  # Plots modified line of best fit
        plt.scatter(avgXMild, avgYMild, color = 'red', marker = 'x', label = 'Original Average', s = 150)
        plt.text(avgXMild, avgYMild, 'Original Average Point', color='red', fontsize=12, ha='left', va = 'top')
        plt.scatter((avgXMild+n), modifiedAvgYMild, color = 'red', marker = 'x', label = 'Modified Average', s = 150)
        plt.text((avgXMild+n), modifiedAvgYMild, 'Modified Average Point', color='red', fontsize=12, ha='left', va = 'top')
        plt.annotate(f'Correlation Coefficient: {mildCorrelationCoefficient}',  xy=(0.5, 0), xycoords='axes fraction', xytext=(0, 290), textcoords='offset points', ha='center', va='bottom') # Uses annotate function in matplotlib to display the Correlation Coeficient
        break       # Exit loop if a valid input is provided

    #Duplicate code, with different variables
    elif var1 == 2:
        plt.scatter(moderateMatrix[:, 0], moderateMatrix[:, 1], label='Moderate', marker='s')
        slope, intercept = np.polyfit(moderateMatrix[:, 0], moderateMatrix[:, 1], 1)
        plt.plot(moderateMatrix[:, 0], slope * moderateMatrix[:, 0] + intercept, color='red', label='Line of Best Fit')

        n = float(input('What would you like the data to be changed by?'))
        moderateChangeAvgY = modCorrelationCoefficient*(n/stdDevXmoderate)*stdDevYmoderate
        modifiedAvgYModerate = avgYModerate + moderateChangeAvgY
        print(f"The original average of ODI values in the 'Moderate' dataset was {avgYModerate}, but after your modification to the AHI values, the average of the ODI values is now {modifiedAvgYModerate}.")
        print (f"Original Average Points: ({avgXModerate}, {avgYModerate})")
        print (f"Modified Average Points: ({(avgXModerate+n)}, {modifiedAvgYModerate})")
        avgydif = modifiedAvgYModerate - avgYModerate
        print (f"The average difference between the original and modified data is ({n}, {avgydif})")
        
        modifiedModerateMatrix = moderateMatrix.copy()
        modifiedModerateMatrix[:, 0] = (modifiedModerateMatrix[:, 0] + n).astype(int)
        modifiedModerateMatrix[:, 1] = (modifiedModerateMatrix[:, 1] + moderateChangeAvgY)
        plt.scatter(modifiedModerateMatrix[:, 0], modifiedModerateMatrix[:, 1], label='ModifiedModerate', marker='o', color = 'purple')
        slopeModified, interceptModified = np.polyfit(modifiedModerateMatrix[:, 0], modifiedModerateMatrix[:, 1], 1)
        plt.plot(modifiedModerateMatrix[:, 0], slopeModified * modifiedModerateMatrix[:, 0] + interceptModified, color='red', label='Modified Line of Best Fit')
        plt.scatter(avgXModerate, avgYModerate, color = 'red', marker = 'x', label = 'Original Average', s = 150)
        plt.text(avgXModerate, avgYModerate, 'Original Average Point', color='red', fontsize=12, ha='left', va = 'top')
        plt.scatter((avgXModerate+n), modifiedAvgYModerate, color = 'red', marker = 'x', label = 'Modified Average', s = 150)
        plt.text((avgXModerate+n), modifiedAvgYModerate, 'Modified Average Point', color='red', fontsize=12, ha='left', va = 'top')
        plt.annotate(f'Correlation Coefficient: {modCorrelationCoefficient}', xy=(0.5, 0), xycoords='axes fraction', xytext=(0, 290), textcoords='offset points', ha='center', va='bottom')
        break


    elif var1 == 3:
        plt.scatter(severeMatrix[:, 0], severeMatrix[:, 1], label='Severe', marker='^')
        slope, intercept = np.polyfit(severeMatrix[:, 0], severeMatrix[:, 1], 1)
        plt.plot(severeMatrix[:, 0], slope * severeMatrix[:, 0] + intercept, color='red', label='Line of Best Fit')

        n = float(input('What would you like the data to be changed by?'))
        severeChangeAvgY = sevCorrelationCoefficient*(n/stdDevXsevere)*stdDevYsevere
        modifiedAvgYSevere = avgYSevere + severeChangeAvgY
        print(f"The original average of ODI values in the 'Severe' dataset was {avgYSevere}, but after your modification to the AHI values, the average of the ODI values is now {modifiedAvgYSevere}.")
        print (f"Original Average Points: ({avgXSevere}, {avgYSevere})")
        print (f"Modified Average Points: ({(avgXSevere+n)}, {modifiedAvgYSevere})")
        avgydif = modifiedAvgYSevere - avgYSevere
        print (f"The average difference between the original and modified data is ({n}, {avgydif})")
        modifiedSevereMatrix = severeMatrix.copy()
        modifiedSevereMatrix[:, 0] = (modifiedSevereMatrix[:, 0] + n).astype(int)
        modifiedSevereMatrix[:, 1] = (modifiedSevereMatrix[:, 1] + severeChangeAvgY)
        plt.scatter(modifiedSevereMatrix[:, 0], modifiedSevereMatrix[:, 1], label='ModifiedSevere', marker='o', color = 'purple')
        slopeModified, interceptModified = np.polyfit(modifiedSevereMatrix[:, 0], modifiedSevereMatrix[:, 1], 1)
        plt.plot(modifiedSevereMatrix[:, 0], slopeModified * modifiedSevereMatrix[:, 0] + interceptModified, color='red', label='Modified Line of Best Fit')
        plt.scatter(avgXSevere, avgYSevere, color = 'red', marker = '+', label = 'Original Average', s = 200)
        plt.text(avgXSevere, avgYSevere, 'Original Average Point', color='black', fontsize=15, ha='left', va = 'top')
        plt.scatter((avgXSevere+n), modifiedAvgYSevere, color = 'red', marker = '+', label = 'Modified Average', s = 200)
        plt.text((avgXSevere+n), modifiedAvgYSevere, 'Modified Average Point', color='black', fontsize=15, ha='left', va = 'top')
        plt.annotate(f'Correlation Coefficient: {sevCorrelationCoefficient}', xy=(0.5, 0), xycoords='axes fraction', xytext=(0, 350), textcoords='offset points', ha='center', va='bottom')
        break 


    else:
        print('Invalid Input. Please enter 1, 2, or 3.')

plt.xlabel('Apnea-Hypopnea Index (AHI)')
plt.ylabel('Oxygen Desaturation Index (ODI)')
plt.title('Scatter Plot of Apnea-Hypopnea Index vs Oxygen Desaturation Index with line of best fit (Including modified data)')



# Show the plot
plt.show()