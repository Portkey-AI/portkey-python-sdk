#!/bin/bash

# Function to replace words in a file using the provided mapping
replace_words_in_file() {
    local file_path=$1
    local virtual_keys=("${!2}")
    local virtual_keys_values=("${!3}")

    # Read the file content
    local file_content=$(< "$file_path")

    # Iterate over the mapping and replace words
    for (( i=0; i<${#virtual_keys[@]}; i++ )); do
        file_content=$(echo "$file_content" | sed "s/${virtual_keys[$i]}/${virtual_keys_values[$i]}/g")
    done

    # Write the modified content back to the file
    echo "$file_content" > "$file_path"
}

# Function to process files in a directory
process_files_in_directory() {
    local directory=$1
    local virtual_keys=("${!2}")
    local virtual_keys_values=("${!3}")

    # Find all .json files in the directory and its subdirectories
    find "$directory" -type f -name "*.json" | while read -r file; do
        replace_words_in_file "$file" virtual_keys virtual_keys_values
        echo "Processed file: $file"
    done
}

# Main script

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq could not be found. Please install jq to use this script."
    exit 1
fi

# Hardcoded directory path
directory="tests/configs"

# Hardcoded mapping of words to be replaced and their replacements
virtual_keys=("openai-virtual-key" "anyscale-virtual-key" "azure-virtual-key" "cohere-virtual-key" "anthropic-virtual-key" "stability-virtual-key")
virtual_keys_values=("openai_value" "anyscale_value" "azure_value" "cohere_value" "anthropic_value" "stability_value")


# Check if the directory exists
if [[ ! -d "$directory" ]]; then
    echo "Directory does not exist. Please provide a valid directory path."
    exit 1
fi

# Check for --undo parameter
if [[ "$1" == "--undo" ]]; then
    echo "Undoing word replacement..."
    # Swap virtual_keys and virtual_keys_values for undo
    temp_words=("${virtual_keys[@]}")
    virtual_keys=("${virtual_keys_values[@]}")
    virtual_keys_values=("${temp_words[@]}")
fi


process_files_in_directory "$directory" virtual_keys virtual_keys_values
echo "Virutal Key replacement completed."
