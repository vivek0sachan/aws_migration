import os
import difflib
cwd = os.getcwd()

primary_file_path = os.path.join(cwd,'main_files')
secondary_file_path = os.path.join(cwd,'secondary_files')
comparison_path = os.path.join(cwd,'comparison_files')

os.makedirs(comparison_path, exist_ok=True)

file_list=os.listdir(primary_file_path)
comparer_list=[]
for file in file_list:
    comparer_list.append(
        {
            "source_file": os.path.join(primary_file_path,file),
            "destination_file": os.path.join(secondary_file_path,file.split('.')[0]+"-v1.txt"),
            "comparison_file": os.path.join(comparison_path,file.split('.')[0]+"_comparison.txt"),
        }
    )
    
for file in comparer_list:
    with open(file['source_file'], 'r') as f:
        source_data = f.read().splitlines()
    with open(file['destination_file'], 'r') as f:
        destination_data = f.read().splitlines()

    missing_files = set(source_data) - set(destination_data)

    if missing_files:
        print(f"The following files are missing in {file['destination_file']}:")
        print('\n'.join(missing_files))

        with open(file['comparison_file'], 'w') as f:
            for file in missing_files:
                if file.endswith('/'):
                    pass
                else:
                    f.write(file + '\n')
    else:
        print(f"{file['source_file']} and {file['destination_file']} have the same files")
        
#delete empty comparison files


#this programm compares 2 buckets for file names , which will be later used to check if buckets have synced properly