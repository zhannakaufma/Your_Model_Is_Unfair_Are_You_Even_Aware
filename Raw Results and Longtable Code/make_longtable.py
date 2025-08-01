
import sys
import os
from libs.long_table import ResultsTable

input_file_path = os.path.abspath(sys.argv[1])
output_file_path = os.path.abspath(sys.argv[2])
results_table = ResultsTable(input_file_path, sys.argv[3])
df = results_table.default_long_table_df()
df.to_csv(output_file_path, index=False)


