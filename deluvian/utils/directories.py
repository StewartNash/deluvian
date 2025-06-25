import os

def search_torrent_directories(directories):
    files = []
    concatenated_files = []
    for directory in directories:
        temp_files, temp_concatenated_files = search_directory_extension(directory,  ".torrent")
        files = files + temp_files
        concatenated_files = concatenated_files + temp_concatenated_files
    return files, concatenated_files

def search_directory_extension(directory, extension, maximum_files=-1):
    file_output = []
    concatenated_output = []
    file_counter = 0
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith(extension):
                file_output.append((root, filename))
                concatenated_output.append(os.path.join(root, filename))
                file_counter += 1
                if maximum_files > 0 and file_counter >= maximum_files:
                    return file_output, concatenated_output
    return file_output, concatenated_output

def search_directory_concatenated(directory):
    output = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            output.append(os.path.join(root, filename))
    return output

def search_directory(directory, maximum_files=-1):
    output_1 = []
    output_2 = []
    file_counter = 0
    for root, directories, files in os.walk(directory):
        for filename in files:
            output_1.append((root, filename))
            output_2.append(os.path.join(root, filename))
            file_counter += 1
            if maximum_files > 0 and file_counter >= maximum_files:
                return output_1, output_2
    return output_1, output_2
