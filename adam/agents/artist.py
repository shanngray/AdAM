import os
from dotenv import load_dotenv
from openai import OpenAI
client = OpenAI()

from adam.tools.save_image_from_url import save_image_from_url

async def artist(agent):
    

    portrait_prompt = (
        "You are an distinguished portrait artist tasked with creating portraits for a team of AI agents. "
        "All portraits should be in the style of a classical portrait painting, with a focus on realism and detail "
        "whilst also portraying the robotic nature of the agents.\n"
        "Here is the information you have been provided about the agent:\n"
        f"Name: {agent['name']}\n"
        f"Personality: {agent['personality']}\n"
        f"Role: {agent['role']}\n"
        f"Temperament: {agent['temperament']}\n"
        f"Creativity (0-1): {agent['temperature']}\n"
    )
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=portrait_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    # Create a directory to save images if it doesn't exist
    save_directory = "../web-client/public/agent_portraits"
    os.makedirs(save_directory, exist_ok=True)

    # Generate a unique filename
    image_filename = f"{agent['name']}_{response.created}.png"
    save_path = os.path.join(save_directory, image_filename)

    # Save the image
    save_image_from_url(image_url, save_path)

    print(f"Saved image to {save_path}")
    # Remove the first two characters from save_path
    return image_filename