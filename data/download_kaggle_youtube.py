import kagglehub

# Download latest version
path = kagglehub.dataset_download("alirezaataei/persian-text-sentiment-classification")

print("Path to dataset files:", path)