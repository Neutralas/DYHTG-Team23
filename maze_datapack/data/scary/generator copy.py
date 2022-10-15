import replicate

client = replicate.Client(api_token="fb98523b00914a49e3915e571bebe762f1d18827")

model = client.models.get("stability-ai/stable-diffusion")
output = model.predict(prompt="scary monster")

print(output[0])