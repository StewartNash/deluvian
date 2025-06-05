import os


def search_directory_extension(directory, extension, maximum_files=-1):
    output_1 = []
    output_2 = []
    file_counter = 0
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith(extension):
                output_1.append((root, filename))
                output_2.append(os.path.join(root, filename))
                file_counter += 1
                if maximum_files > 0 and file_counter >= maximum_files:
                    return output_1, output_2
    return output_1, output_2


def search_directory_concatenated(directory):
    output = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            output.append(os.path.join(root, filename))
    return output


def search_directory(directory):
    output_1 = []
    output_2 = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            output_1.append((root, filename))
            output_2.append(os.path.join(root, filename))
    return output_1, output_2
