import requests  
  
def fetch_top_stories(limit=10):  
    """Fetches the top stories from Hacker News."""  
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"  
    response = requests.get(top_stories_url)  
    story_ids = response.json()  
    top_stories = story_ids[:limit]  
    return top_stories  
  
def fetch_item(item_id):  
    """Fetches an item by its ID."""  
    item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"  
    response = requests.get(item_url)  
    item = response.json()  
    return item  
  
def fetch_top_posts_with_comments(posts_limit=10, comments_limit=5):  
    """Fetches top posts and their comments."""  
    top_stories = fetch_top_stories(limit=posts_limit)  
    for story_id in top_stories:  
        story = fetch_item(story_id)  
        print(f"Headline: {story['title']}")  
        print(f"URL: {story.get('url', 'No URL')}")  
        print("Summary: This post is among the top stories on Hacker News, attracting significant attention and discussion.")  
        print("Comments:")  
        if 'kids' in story:  
            comment_ids = story['kids'][:comments_limit]  
            for comment_id in comment_ids:  
                comment = fetch_item(comment_id)  
                # Ensure the comment is not deleted and has text  
                if comment and 'text' in comment:  
                    print(f"- {comment['text']}")  
        else:  
            print("No comments available.")  
        print("\n" + "-"*80 + "\n")  
  
if __name__ == "__main__":  
    fetch_top_posts_with_comments()  