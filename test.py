import pandas as pd

input_excel = 'exam_responses_with_marks.xlsx'  # your Excel file
output_excel = 'total_marks_per_student(1).xlsx'

# Read Excel file
df = pd.read_excel(input_excel, engine='openpyxl')

# Ensure 'Marks Obtained' is numeric
df['Marks Obtained'] = pd.to_numeric(df['Marks Obtained'], errors='coerce').fillna(0)

# Group by RollNo and sum marks
total_marks = df.groupby('RollNo')['Marks Obtained'].sum().reset_index()

# Add 2 bonus marks to everyone who exists in data
total_marks['Marks Obtained'] = total_marks['Marks Obtained'] + 2

# Generate full list of roll numbers
roll_numbers = [f"2311CS040{str(i).zfill(3)}" for i in range(91, 181)]
roll_numbers.append("2211CS040008")  # exception roll number

# Create full DataFrame
full_df = pd.DataFrame({'RollNo': roll_numbers})

# Merge with actual marks
full_df = full_df.merge(total_marks, on='RollNo', how='left')

# Fill absent students with 0 or "Absent"
full_df['Marks Obtained'] = full_df['Marks Obtained'].fillna('Absent')

# Save to Excel
full_df.to_excel(output_excel, index=False)

print(f"Complete class report saved to {output_excel}")
