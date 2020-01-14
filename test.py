import playlistBuilder as p

print("TESTING TESTING TESTING")
print()

# Test removals (set-up)
def setUpRemovals():
    test1 = ['one (1)', 'two (2)', 'three (3)']
    testA = ['A (a)', 'B (b)', 'C (c)']
    test = [test1, testA]

# Test Removals from single lists
def testRemoveFromList():
    test1 = ['one (1)', 'two (2)', 'three (3)']
    testA = ['A (a)', 'B (b)', 'C (c)']
    test = [test1, testA]
    print("'Testing 'removeFromList() : ")
    print(test)
    p.removeFromList(test1)
    p.removeFromList(testA)
    print(test)
    print()

# Test removals from a list of lists (1 item in list)
def testRemoveFromAllOne():
    test1 = ['one (1)', 'two (2)', 'three (3)']
    test = [test1]
    print("'Testing 'removeFromAll() : (1 item in list) ")
    print(test)
    p.removeFromAll(test)
    print(test)
    print()

# Test removals from a list of lists (2 items in list)
def testRemoveFromAllTwo():
    test1 = ['one (1)', 'two (2)', 'three (3)']
    testA = ['A (a)', 'B (b)', 'C (c)']
    test = [test1, testA]
    print("'Testing 'removeFromAll() : (2 items in list) ")
    print(test)
    p.removeFromAll(test)
    print(test)
    print()

def testRemoveFromAll():
    test = [['The Blueprint (Explicit Version)', 'Watch The Throne (Deluxe)', '4:44', 'Watch The Throne', 'The Blueprint (Edited Version)', 'The Blueprint', 'Watch The Throne', 'Magna Carta... Holy Grail', 'The Blueprint 3', 'Watch The Throne'], ['The Christmas Song (Expanded Edition)', 'The Christmas Song (Expanded Edition)', 'Hail to the King', 'The Lion King', 'The King', 'The Christmas Song (Expanded Edition)', 'The Lion King', 'Dancing in the Moonlight', 'The Christmas Song (Expanded Edition)', 'The Lion King'], ['Burn The Ships', 'The King (with Dzeko)', 'Elvis 30 #1 Hits', "Elvis' Christmas Album", 'From Elvis in Memphis', 'Christmas With Nat And Dean', 'Mobile Estates', 'Rhymes & Reasons', 'King Arthur: Legend of the Sword (Original Motion Picture Soundtrack)', 'Cole, Christmas & Kids'], ["The Wiggles' Big Ballet Day!", 'We Too Are One', 'Full Circle', 'The End of an Era', 'The Original Rude Girl', 'The Three Musketeers (Original Motion Picture Soundtrack)', 'Love Is King Love Is Queen', 'The World of Robin and Marion, Songs and Motets from the Time of Adam De La Halle (1240-1287) (Le Chant De Robin Et Marion, Chansons Et Mote', 'The Complete Studio Albums', 'Boxed']]
    print("'Testing 'removeFromAll() : ")
    print()
    print(test)
    print()
    p.removeFromAll(test)
    print(test)
    print()

#testRemoveFromList()
#testRemoveFromAllOne()
#testRemoveFromAllTwo()
testRemoveFromAll()
