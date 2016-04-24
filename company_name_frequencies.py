import praw
import time

already_seen_posts = []

def load_list_of_companies():
    companies_csv = file("The Really Big Hugely Ginormous Tech Company List - Sheet1.csv")
    company_names = []
    for line in companies_csv:
        company = line.split(",")[1].lower()
        company_names.append(company)
    companies_csv.close()
    all_companies = list(set(company_names)) #remove duplicates  
    return all_companies

def fetch_posts():
    global already_seen_posts
    reddit = praw.Reddit(user_agent='cscareerquestions_company_mentions')
    cscq = reddit.get_subreddit('cscareerquestions')
    posts = cscq.get_top_from_all(limit="none")
    newPosts = []
    
    for post in posts: #go through every post
        if post not in already_seen_posts:
            newPosts.append(post)
            already_seen_posts.append(post)
    return newPosts
    
def search_post_for_companies(posts, all_companies, company_counts):
    for post in posts:
        words_in_post = post.selftext.split() + post.title.split()
        for word in words_in_post: #go through every word in the comment
            word = tokenize_word(word)
            if word in all_companies:
                company_counts[word] = company_counts.get(word, 0) + 1

def tokenize_word(word):
    #convert from unicode to ascii
    word = word.encode('ascii','ignore')
    punctuation = [".",",","!","?",'"']
    #remove punctiation
    tokenized_word = ''.join(char for char in word if char not in punctuation)
    tokenized_word = tokenized_word.lower()
    #if possesive, drop the 's
    tokenized_word = tokenized_word.replace("'s","")
    return tokenized_word

def main():
    all_companies = load_list_of_companies()
    company_counts = {}
    while True:
        new_posts = fetch_posts()
        if len(new_posts) > 0:
            search_post_for_companies(new_posts, all_companies, company_counts)
            print company_counts
        else:
            print "nothing new"
        time.sleep(2)

if __name__ == "__main__":
    main()


