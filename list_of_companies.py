def loadListOfCompanies():
	companiesCsv = file("The Really Big Hugely Ginormous Tech Company List - Sheet1.csv")
	companyNames = []
	for line in companiesCsv:
		company = line.split(",")[1]
		companyNames.append(company)
	companiesCsv.close()
	return set(companyNames) #remove duplicates		


def main():
	companies = loadListOfCompanies()

