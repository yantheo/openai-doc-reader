import openai
import datetime

# Initialize the OpenAI client
client = openai.OpenAI()

def delete_all_files():
    confirmation = input(
        "This will delete all OpenAI files with purpose 'assistants'.\n Type 'YES' to confirm: "
    )
    if confirmation == "YES":
        response = client.files.list(purpose="assistants")
        count = 0
        for file in response.data:
            client.files.delete(file.id)
            count +=1
            print(count)
        print("All files with purpose 'assistants' have been deleted.")
    else:
        print("Operation cancelled.")

delete_all_files()
