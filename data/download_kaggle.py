import kagglehub

# Download latest version
path = kagglehub.dataset_download("amderakhshan/persiantelegrammessages")

print("Path to dataset files:", path)