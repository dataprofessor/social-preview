import streamlit as st
import cairosvg
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="🏞️ Social Preview Image Generator")
st.title('🏞️ Social Preview Image Generator')
st.write('An app to generate social preview images for the [Streamlit blog](https://blog.streamlit.io/).')

# Convert to Twitter social preview image
def img2twitter(image_input):
  img = Image.open(image_input)

  # Create LinkedIn social preview image (1.91:1 aspect ratio)
  original_height = img.size[1]
  new_height = (img.size[0]*9)/16
  height_difference = new_height - original_height

  # Color gradient border
  color_gradient_img = img.crop(( 0,0,img.size[0], (height_difference/2) ))

  # Create new image
  twitter_img = Image.new("RGB", (img.size[0], int(img.size[1]+height_difference) ) )
  #linkedin_img.paste(color_gradient_img, (0,0) )
  twitter_img.paste(color_gradient_img, (0,0) )
  twitter_img.paste(img, (0,int(height_difference/4)) )
  twitter_img.paste(color_gradient_img, (0,img.size[1]+int(height_difference/4)) )
  twitter_img.paste(color_gradient_img, (0,img.size[1]+int(height_difference/2)) )
  #twitter_img.paste(color_gradient_img, (0,img.size[1]+int(height_difference/2)) )
  return twitter_img

# Convert to LinkedIn social preview image
def img2linkedin(image_input):
  img = Image.open(image_input)

  # Create LinkedIn social preview image (1.91:1 aspect ratio)
  original_height = img.size[1]
  new_height = img.size[0]/1.91
  height_difference = new_height - original_height

  # Color gradient border
  color_gradient_img = img.crop(( 0,0,img.size[0], (height_difference/2) ))

  # Create new image
  linkedin_img = Image.new("RGB", (img.size[0], int(img.size[1]+height_difference) ) )
  #linkedin_img.paste(color_gradient_img, (0,0) )
  linkedin_img.paste(img, (0,0) )
  linkedin_img.paste(color_gradient_img, (0,img.size[1]) )
  linkedin_img.paste(color_gradient_img, (0,img.size[1]+int(height_difference/2)) )
  return linkedin_img

uploaded_file = st.file_uploader("Choose an Image file", type='svg')

if uploaded_file is not None:
  svg_content = uploaded_file.read().decode("utf-8")

  output_buffer = BytesIO()
  cairosvg.svg2png(bytestring=uploaded_file.getvalue(), write_to=output_buffer, scale=5)

  with open("converted.png", "wb") as f:
    f.write(output_buffer.getvalue())

  col1, col2 = st.columns(2)

  
  # Convert to Twitter Social Preview
  with col1:
    st.subheader("Twitter Social Preview")
    twitter_img = img2twitter("converted.png")
    twitter_img.save("twitter.png")
    st.image(twitter_img, use_column_width=True)
    
    with open("twitter.png", "rb") as file:
      btn = st.download_button(
                  label="Download Twitter social preview image",
                  data=file,
                  file_name=f"{uploaded_file.name.rstrip('.svg')}_twitter.png",
                  mime="image/png"
                )

  # Convert to LinkedIn Social Preview
  with col2:
    st.subheader("LinkedIn Social Preview")
    linkedin_img = img2linkedin("converted.png")
    linkedin_img.save("linkedin.png")
    st.image(linkedin_img, use_column_width=True)
    
    with open("linkedin.png", "rb") as file:
      btn = st.download_button(
                  label="Download LinkedIn social preview image",
                  data=file,
                  file_name=f"{uploaded_file.name.rstrip('.svg')}_linkedin.png",
                  mime="image/png"
                )
