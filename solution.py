import json
import sys
from operator import attrgetter
from datetime import datetime, timedelta
from Offer import Offer

# Read JSON and return an array of offers
def readJSON(fileName):
    with open(fileName, "r") as readFile:
        data = json.load(readFile)
        offersArr = []
        for item in data["offers"]:
            offersArr.append(Offer.convertFromDict(item))
    return offersArr


# Write the result offers in a json file
def writeJSON(fileName, result):
    with open(fileName, "w") as writeFile:
        offers = []
        for item in result:
            offers.append(item.serialize())
        writeFile.writelines(json.dumps({"offers": offers}))


# Filter available offers to satisfy the customer's check in date and location
def filterOffers(offersArr, checkInDate):
    resultArr = []
    comparedDate = checkInDate + timedelta(days=5)

    for item in offersArr:
        # Rule 1: Only select offers with category that is Restaurant, Retail or Activity
        # Rule 2: Offer needs to be valid till checkin date + 5 days
        if item.category in [1,2,4] and item.valid_to >= comparedDate:
            # Rule 3: If an offer is available in multiple merchants, only select the closest merchant
            if len(item.merchants) > 1:
                minDistanceMerchant = min(item.merchants, key=attrgetter("distance"))
                item.merchants = [minDistanceMerchant]
            resultArr.append(item)
    
    # Rule 4: This class should only return 2 offers even though there are several eligible offers
    # Rule 5: If there are multiple offers in the same category give priority to the closest merchant offer.
    # Rule 6: If there are multiple offers with different categories, select the closest merchant offers when selecting 2 offers
    # => Combine these rules by sorting the array by distance and find two closest offers with different categories
    if len(resultArr) > 2:
        resultArr = sorted(resultArr, key=lambda arr: arr.merchants[0].distance)
        for idx in range(1, len(resultArr)):
             # Find the second closest offer which have a different category than the closest one
            if resultArr[idx].category != resultArr[0].category:
                return [resultArr[0], resultArr[idx]]
    return resultArr


# Check the format of check in date
def validateCheckInDate(checkInDate):
        try:
            datetime.strptime(checkInDate, "%Y-%m-%d").date
        except ValueError:
            raise ValueError("Invalid format. The check-in date should be in YYYY-MM-DD")


def main():
    try:
        # Check the number of arguments and its format
        if len(sys.argv) != 2:
            raise SyntaxError("Please only input check-in date.")
        validateCheckInDate(sys.argv[1])

        inputFileName = "input.json"
        outputFileName = "output.json"
        checkInDate = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        offersArr = readJSON(inputFileName)
        resultArr = filterOffers(offersArr, checkInDate)
        writeJSON(outputFileName, resultArr)
    except Exception as e:
        print(e)
    


if __name__ == "__main__":
    main()