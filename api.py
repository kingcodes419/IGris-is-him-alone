import google.generativeai as genai

genai.configure(api_key="AIzaSyD80E6_Q2D50mTwW_o3OEHVNnDEqwLGYMU")
model = genai.GenerativeModel("gemini-2.0-flash-lite")
response = model.generate_content("You are king")
print(response.text)
