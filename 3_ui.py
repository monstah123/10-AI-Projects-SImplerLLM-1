# Import necessary libraries
import streamlit as st  # Streamlit is used to create the web app
import json  # For validating and parsing JSON data
from SimplerLLM.language.llm import LLM, LLMProvider  # Importing the custom LLM class and provider

# Create an instance of the LLM class with the specified provider and model (GPT-4 in this case)
llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-4o")

# Function to generate hooks based on user input
def generate_hooks(topic, usage):
    """
    Function to generate hooks using the LLM instance. It takes user input (topic and usage)
    and creates a prompt to pass to the language model for hook generation.
    """
    # Define the template for the hook generation prompt
    hook_generator_prompt = """
    as an expert copywriter specialized in hook generation, your task is to 
    analyze the [Provided_Hook_Examples].

    Use the templates that fit most to generate 3 new Hooks 
    for the following topic: {user_input} and Usage in: {usage}. 

    The output should be ONLY valid JSON as follows:
    [
      {{
        "hook_type": "The chosen hook type",
        "hook": "the generated hook"
      }},
      {{
        "hook_type": "The chosen hook type",
        "hook": "the generated hook"
      }},
      {{
        "hook_type": "The chosen hook type",
        "hook": "the generated hook"
      }}
    ]

    [Provided_Hook_Examples]:
    "Hook Type,Template,Use In
    Strong sentence,"[Topic] won’t prepare you for [specific aspect].",Social posts, email headlines, short content
    ...
    The JSON object:\n\n"""

    # Format the prompt with user-provided topic and usage context
    input_prompt = hook_generator_prompt.format(user_input=topic, usage=usage)

    # Generate the response using the LLM instance
    generated_text = llm_instance.generate_response(prompt=input_prompt)
    
    return generated_text

# Function to clean and validate JSON response
def clean_and_validate_json(raw_data):
    """
    Cleans the raw data by removing any backticks or markdown-like syntax
    and attempts to parse it as JSON. Returns parsed JSON if successful.
    """
    # Remove any leading/trailing code block markers like ```json or ``` (if present)
    cleaned_data = raw_data.strip().strip('```').strip('json').strip()

    try:
        # Try to load the cleaned response as a JSON object
        parsed_json = json.loads(cleaned_data)
        return parsed_json
    except json.JSONDecodeError:
        # If there's a JSON error, return None for handling
        return None

# Main function to define the Streamlit UI
def main():
    """
    This is the main function that sets up the Streamlit web app.
    It includes input fields, buttons, and displays the generated hooks.
    """

    # Set the title of the Streamlit application
    st.title("AI Hook Generator using GPT-4")
    
    # Provide a brief description or instructions for the app
    st.write("""
    Use this tool to generate marketing hooks based on a given topic and usage context.
    Powered by GPT-4, this app will create hooks in different formats (questions, facts, etc.).
    """)

    # Create an input field for the user to enter the topic (default value is "AI tools")
    topic = st.text_input("Enter the topic for hook generation:", "AI tools")

    # Create an input field for the user to specify the usage context (default value is "short video")
    usage = st.text_input("Enter the usage context (e.g., social media, email headline, etc.):", "short video")

    # Create a button that triggers the hook generation process when clicked
    if st.button("Generate Hooks"):
        # Display a loading spinner while the hooks are being generated
        with st.spinner('Generating hooks...'):
            hooks = generate_hooks(topic, usage)  # Call the function to generate hooks
            
            # Clean and validate the generated hooks to ensure they are valid JSON
            parsed_hooks = clean_and_validate_json(hooks)
            
            if parsed_hooks:
                # If the JSON is valid, display it in JSON format
                st.success("Hooks generated successfully!")
                st.json(parsed_hooks)  # Display the parsed JSON data
            else:
                # If the JSON is invalid, show an error message and display the raw output
                st.error("Error: The response is not valid JSON.")
                st.text("Raw response from the model:")
                st.code(hooks)  # Display the raw, unparsed text for debugging purposes

# Run the main function to start the Streamlit app
if __name__ == "__main__":
    main()

