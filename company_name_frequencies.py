import praw
from collections import defaultdict
import time

all_companies = []
already_seen_posts = []
company_counts = defaultdict(int)

def loadListOfCompanies():
	global all_companies
	companiesCsv = file("The Really Big Hugely Ginormous Tech Company List - Sheet1.csv")
	companyNames = []
	for line in companiesCsv:
		company = line.split(",")[1].lower()
		companyNames.append(company)
	companiesCsv.close()
	all_companies = list(set(companyNames)) #remove duplicates	

def fetchPosts():
	global already_seen_posts
	reddit = praw.Reddit(user_agent='cscareerquestions_company_mentions')
	cscq = reddit.get_subreddit('cscareerquestions')
	posts = cscq.get_hot()
	newPosts = []
	
	for post in posts: #go through every post
		if post not in already_seen_posts:
			newPosts.append(post)
			already_seen_posts.append(post)
	return newPosts
	
def searchPostForCompanies(posts):
	global company_counts
	for post in posts:
		wordsInPost = post.selftext.split() + post.title.split()
		for word in wordsInPost: #go through every word in the comment
			word = tokenizeWord(word)
			if word in all_companies:
				company_counts[word] += 1

def tokenizeWord(word):
	#convert from unicode to ascii
	word = word.encode('ascii','ignore')
	punctuation = [".",",","!","?",'"']
	#remove punctiation
	tokenizedWord = ''.join(char for char in word if char not in punctuation)
	tokenizedWord = tokenizedWord.lower()
	#if possesive, drop the 's
	tokenizedWord = tokenizedWord.replace("'s","")
	return tokenizedWord

def main():
	global company_counts
	loadListOfCompanies()
	while True:
		newPosts = fetchPosts()
		if len(newPosts) > 0:
			searchPostForCompanies(newPosts)
			print company_counts
		else:
			print "nothing new"
		time.sleep(2)

main()

