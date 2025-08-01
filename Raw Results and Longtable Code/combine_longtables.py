import sys
import os
import pandas as pd


input_file_path_first = os.path.abspath(sys.argv[1])
input_file_paths = [os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3]), os.path.abspath(sys.argv[4]), os.path.abspath(sys.argv[5]), os.path.abspath(sys.argv[6]), os.path.abspath(sys.argv[7]), os.path.abspath(sys.argv[8]), os.path.abspath(sys.argv[9]), os.path.abspath(sys.argv[10]), os.path.abspath(sys.argv[11])]
output_file_path = os.path.abspath(sys.argv[12])

df = pd.read_csv(input_file_path_first)
max_df = df['Pid'].max()

for input_file_path in input_file_paths:
    df_new = pd.read_csv(input_file_path)
    df_new['Pid'] = df_new['Pid'] + max_df
    df = pd.concat([df, df_new])
    max_df = df['Pid'].max()
df.to_csv(output_file_path, index=False)

df = df.drop_duplicates(subset='Pid', keep="last")
df.to_csv("just_resp.csv",index=False)

total_num =  max_df

print(df['Gender'].value_counts())
print(df['Education'].value_counts())
print(df['Income'].value_counts())
print(df['Race/Ethnicity'].value_counts())
print(df['Familiarity'].value_counts())


print(f"We recruited {total_num} participants with ages ranging from {df['Age'].min()} to {df['Age'].max()}.") 


