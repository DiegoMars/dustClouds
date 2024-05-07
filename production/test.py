def reverse_search(string):
    # Reverse the string to search from the end
    reversed_string = string[::-1]
    
    # Find the index of the first "\" from the end
    slash_index = reversed_string.find("/")
    
    if slash_index == -1:
        print("No '\\' found in the string.")
        return
    
    # Get the substring after the "\" and reverse it back
    after_slash = reversed_string[:slash_index][::-1]
    
    # Split the string by "_" and return the result
    parts = after_slash.split("_")
    return parts

# Example usage:
input_string = "some/path/to/file_name1_name2_name3.txt"
result = reverse_search(input_string)
print("After '/' and split by '_':", result)