import pandas as pd
from googleapiclient.discovery import build

# List of YouTube API keys
YOUTUBE_API_KEYS = [
    "AIzaSyD5m_h5H8nApN94roOA9JbZ8KtPqWaJPYU",
    "AIzaSyA-ERHQRa3NkWGWNQUgpTnT_aWDTXZc4NQ",
    "AIzaSyAVuUiEIHL4FTn3x2n5bEqaTnUEmjvf6Kk",
    "AIzaSyDFUoMTGkzBng7-tRJ7jMYsgCz5GF_4lzw",
    "AIzaSyBii9HPujRbCRmIVzds9nHIJBWaVVMR-uU",
    "AIzaSyBavY7p3qPzOHxkXtmBtibM3adctnFj_GY",
    "AIzaSyCYaFUZf3Gjc-zoLk3Re13_m3bdQfpfcpc",
    "AIzaSyBswMsCFgXBvyZMbTVX9eNTqPI0jgDH1YI",
    "AIzaSyAe-ISKMidAnCZVVD7Va4tFLoI3lAQCxHk",








]

# Initialize YouTube API key index and query count
youtube_api_key_index = 0
queries_count = 0

# Function to fetch YouTube video links for a given search query
def get_youtube_links(search_query):
    global youtube_api_key_index
    global queries_count
    try:
        # Build the YouTube API service
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEYS[youtube_api_key_index])
        
        # Execute the search request
        search_response = youtube.search().list(
            part='snippet',
            q=search_query,
            type='video',
            maxResults=2  # Fetch 2 video links
        ).execute()
        
        # Increment query count
        queries_count += 1
        
        # If 95 queries have been made, switch to the next API key
        if queries_count >= 95:
            queries_count = 0
            youtube_api_key_index = (youtube_api_key_index + 1) % len(YOUTUBE_API_KEYS)
        
        # Extract video links
        video_links = []
        if 'items' in search_response:
            for item in search_response['items']:
                video_id = item['id']['videoId']
                video_link = f"https://www.youtube.com/watch?v={video_id}"
                video_links.append(video_link)
        return video_links
    except Exception as e:
        print(f"An error occurred with YouTube API: {str(e)}")
        return []

if __name__ == "__main__":
    # Input and output Excel file paths
    input_excel = "C:\\Users\\likit\\Downloads\\Travel_Destination_Answers01.xlsx"
    output_excel = "C:\\Users\\likit\\Downloads\\Travel_Destination_Answers01.xlsx"

    try:
        # Read questions from Excel file
        questions_df = pd.read_excel(input_excel)

        # Fetch YouTube video links for each question
        youtube_video_links = []
        for question in questions_df["Questions"]:
            youtube_links = get_youtube_links(question)
            youtube_video_links.append(", ".join(youtube_links))

        # Update DataFrame with YouTube links
        questions_df["YouTube Video Links"] = youtube_video_links

        # Save the DataFrame to Excel file
        questions_df.to_excel(output_excel, index=False)
        print(f"Data saved to '{output_excel}'")

    except Exception as e:
        print("An error occurred:", str(e))
