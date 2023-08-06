### Programmed by Michael Warmbier ###

### Libraries ###

import re 
import sys

##### Data Storage #####

with open('Dictionary.txt') as file:
    wordList = file.read().splitlines()

## Constant letter point values
class letterValue:
  values = [[' '], 
            ['A','E','I','L','N','O','R','S','T','U'],
            ['D','G'],
            ['B','C','M','P'],
            ['F','H','V','W','Y'],
            ['K'],
            [],
            [],
            ['J','X'],
            [],
            ['Q','Z']];

class tempMemory:
  def __init__(self):
    self.storedLetters = []
    self.scannedLetters = []

##### Methods #####

## Returns point value of a specific letter
def getLetterValue(letter):
  for value in letterValue.values:
    if letter.upper() in letterValue.values[letterValue.values.index(value)]:
      return letterValue.values.index(value);
  raise Exception('Argument is NOT a valid Scrabble letter.');

def getWordValue(word):
  finalValue = 0;
  for char in word:
    finalValue += getLetterValue(char);
  return finalValue;

## Create table of letters and appearances
def createLetterTable(string):
  letterTable = [];
  index = 0;
  for letter in string: 
    letterTable.append([])
    letterTable[index].append(letter);
    letterTable[index].append(1)
    for entry in letterTable:
      if letterTable[index][0] == entry[0] and index != letterTable.index(entry):
        letterTable.remove(letterTable[index]);
        letterTable[letterTable.index(entry)][1] += 1;
        index -= 1;
    index += 1;
  return letterTable;

## Filters letters based on total
def filterRepeats(wordList, letters):
  table = createLetterTable(letters);
  for word in wordList[:]:
    validWord = True;
    wordTable = createLetterTable(word);
    
    for wordEntry in wordTable:
      for entry in table:
        if wordEntry[0] == entry[0] and wordEntry[1] != entry[1]:
          validWord = False;
    if not validWord: 
      wordList.remove(word);
  return wordList;

## Gets all possible words given provided letters
def getScrabbleWords(letters):
  if (len(letters)< 7 or len(letters) > 15):
    raise Exception ('Error: Letter count must be between seven and fifteen.');
    
  regex = re.compile('^([' + letters.upper() + '])*$');
  validWords = [];
  for word in wordList:
    if regex.match(word):
      validWords.append(word);
  for word in validWords:
    tLetters = letters;
    for char in word:
      tLetters.replace(char, '');
  validWords = filterRepeats(validWords, letters);
  for word in validWords[:]:
    validWords[validWords.index(word)] = [word, getWordValue(word)];
  return validWords;

# If run from the console, print results based off arguments

try:
  if (sys.argv == None or sys.argv[1] == None):
    raise IndexError;
  else:
    results = getScrabbleWords(sys.argv[1]);
    for index in results:
      print ('[' + index[0] + ']: ' + str(index[1]) + 'pts');
except IndexError:
  print('Error: No argument provided');