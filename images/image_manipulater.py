from PIL import Image, ImageDraw, ImageFont

def update_image(heading, tech_talk, register_link):
    # Open the existing image
    img_path = '1.jpeg'
    image = Image.open(img_path)
    draw = ImageDraw.Draw(image)

    # Define the position for the new text
    # You will need to adjust these based on your image
    heading_position = (100, 50)  # Example position for heading
    tech_talk_position = (100, 100)  # Example position for tech talk
    register_link_position = (100, 150)  # Example position for registration link

    # Define the font and size
    # You will need to have a .ttf font file on your system
    font_path = '1.otf'
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)

    # Update the text
    # It will overwrite anything that is currently at the specified positions
    draw.text(heading_position, heading, font=font, fill="black")
    draw.text(tech_talk_position, tech_talk, font=font, fill="black")
    draw.text(register_link_position, register_link, font=font, fill="black")

    # Save the image
    output_path = 'image1.jpg'
    image.save(output_path)

# Inputs for the text changes
heading_input = input("Enter the new heading: ")
tech_talk_input = input("Enter the new tech talk details: ")
register_link_input = input("Enter the new register link: ")

# Call the function with the user inputs
update_image(heading_input, tech_talk_input, register_link_input)

