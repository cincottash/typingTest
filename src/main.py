from globals import * 
from setup import *
import time
import math

def calculateResults(wordBankStripped, timeRan, wordsTyped):
    totalCharsTyped = 0

    wordsTypedCorrectly = 0

    charsTypedCorrectly = 0

    for i, word in enumerate(wordsTyped):
        totalCharsTyped += len(word)
        if(word == wordBankStripped[i]):
            wordsTypedCorrectly += 1
    totalWordsTyped = totalCharsTyped/5

    totalChars = 0

    try:
        for i, typedWord in enumerate (wordsTyped):
            for j, char in enumerate(typedWord):
                if char == wordBankStripped[i][j]:
                    charsTypedCorrectly += 1
                totalChars += 1
    #For when the word we type is longer than the expected word        
    except IndexError:
        pass

    #divide by 0 catch
    if(totalCharsTyped == 0):
        charAccuracy = 0
    else:
        charAccuracy = round(100 * charsTypedCorrectly/totalChars, 2)

    #Every 5 chars is a word according to google
    WPM = round(totalCharsTyped/5 * 60/timeRan, 2)
    print("Char accuracy: {} %\nTotal Chars typed: {}\nChars typed correctly: {}\nWords typed: {}\nWords typed correctly: {}\nWords Per Minute: {}".format(charAccuracy, totalCharsTyped, charsTypedCorrectly, totalWordsTyped, wordsTypedCorrectly, WPM))

    return totalWordsTyped, wordsTypedCorrectly, charsTypedCorrectly, totalCharsTyped, charAccuracy, WPM

def resultsLoop(canvas, canvasWidth, canvasHeight, inactiveColor, font, wordBankStripped, timeRan, wordsTyped):
    totalWordsTyped, wordsTypedCorrectly, charsTypedCorrectly, totalCharsTyped, charAccuracy, WPM = calculateResults(wordBankStripped, timeRan, wordsTyped)

    exitResults = False

    while(not exitResults):

        for event in pygame.event.get():
            #Escape will exit the test
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exitResults = True

        canvas.fill((30, 30, 30))

        wpmText = font.render("Words per minute: {}".format(WPM), True, inactiveColor)
        totalWordsTypedText = font.render("Total words typed: {}".format(totalWordsTyped), True, inactiveColor)
        wordsTypedCorrectlyText = font.render("Words typed correctly: {}".format(wordsTypedCorrectly), True, inactiveColor)
        charsTypedCorrectlyText = font.render("Chars typed correctly: {}".format(charsTypedCorrectly), True, inactiveColor)
        totalCharsTypedText = font.render("Total chars typed: {}".format(totalCharsTyped), True, inactiveColor)
        charAccuracyText = font.render("Char accuracy: {} %".format(charAccuracy), True, inactiveColor)

        canvas.blit(wpmText, (canvasWidth/10, canvasHeight*0.1))
        canvas.blit(charAccuracyText, (canvasWidth/10, canvasHeight*0.2))
        canvas.blit(totalWordsTypedText, (canvasWidth/10, canvasHeight*0.5))
        #canvas.blit(wordsTypedCorrectlyText, (canvasWidth/10, canvasHeight*0.3))
        canvas.blit(charsTypedCorrectlyText, (canvasWidth/10, canvasHeight*0.4))
        canvas.blit(totalCharsTypedText, (canvasWidth/10, canvasHeight*0.3))

        pygame.display.update()

def main(done, runTime, firstRun, active):

    canvasWidth, canvasHeight, timeToRun = argParse()

    canvas, font, clock, boxHeight, boxWidth, boxStartX, boxStartY = pygameSetup(canvasWidth, canvasHeight)
    
    inputBox, wordBox, inactiveColor, activeColor = boxSetup(boxStartX, boxStartY, boxWidth, boxHeight)

    wordQueueList, count, wordBankStripped, text, wordsTyped = populateQueue()

    timeLeft = timeToRun

    while not done:

        #Run for x seconds but don't start keeping track of time until we start typing
        if(timeToRun != "Infinite" and runTime != 0 and (time.time() - runTime >= timeToRun)):
            done = True

        for event in pygame.event.get():
            #Escape will exit the test
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                #If we exited early by hitting escape, adjust how long we ran the test for
                timeRan = time.time() - runTime
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the inputBox rect.
                if inputBox.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            
            elif event.type == pygame.KEYDOWN:
                if active:
                    #Don't start the timer until we start typing and only set the runtime if we're on the first run
                    if(firstRun):
                        runTime = time.time()
                        firstRun = False
                    if event.key == pygame.K_SPACE:
                        #After typing a word, remove it from the queue and add it to our list of words we typed
                        #Dont count just hitting space as a word or char
                        if(text != ""):
                            wordQueueList.remove(wordQueueList[0])
                            wordsTyped.append(text)

                            #Reset the text variable to hold the next word 
                            text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        #Clear the text in the boxs
        canvas.fill((30, 30, 30))

        if(timeToRun != "Infinite" and not firstRun and runTime):
            timeLeft = timeToRun - (time.time() - runTime)
            if(timeLeft < 0):
                timeLeft = 0
            timeLeft = round(timeLeft, 2)

        timeLeftLabel = font.render("Time remaining:", True, activeColor if active else inactiveColor) 
        
        #TODO: Figure out how to use the unicode value for inifnity (221)
        # if(timeLeft == "Infinite"):
        #     timeLeftText = font.render(221, True, activeColor if active else inactiveColor)
        # else:
        timeLeftText = font.render(str(timeLeft), True, activeColor if active else inactiveColor)
        
        canvas.blit(timeLeftLabel, (canvasWidth/20, canvasHeight/12 - boxHeight/2)) 
        canvas.blit(timeLeftText, (canvasWidth/20, canvasHeight/12)) 

        # Render the current text.  
        userInputText = font.render(text, True, (255, 0, 0) if text != wordQueueList[0] else (0, 255, 0))

        # Blit the text.
        canvas.blit(userInputText, (inputBox.x + boxWidth/30, inputBox.y + boxHeight/3))

        #Always make sure there are 5 words in the queue at all times
        if(len(wordQueueList) != 5):
            while(len(wordQueueList) < 5):
                wordQueueList.append(wordBankStripped[count])
                count+=1
        
        wordQueueString = ""
        for word in wordQueueList:
            wordQueueString += "{} ".format(word)

        # Render the current words to be typed.
        wordQueueString = font.render(wordQueueString, True, inactiveColor)

        instructions = font.render("Click me and begin typing to start the test", True, inactiveColor)

        if(not active):
            canvas.blit(instructions, (inputBox.x + boxWidth/30, inputBox.y + boxHeight/3))


        # Blit the words to be displayed from the queue
        canvas.blit(wordQueueString, (wordBox.x + boxWidth/30, wordBox.y + boxHeight/3))
        
        # Blit the inputBox and wordbox.
        pygame.draw.rect(canvas, activeColor if active else inactiveColor, inputBox, 4)
        pygame.draw.rect(canvas, inactiveColor, wordBox, 4)

        pygame.display.update()
        clock.tick(60)

    timeRan = time.time() - runTime

    #If time is done, get the chars we were in the middle of typing (but didn't hit space yet) so they count towards the WPM
    if(text != ""):
        wordsTyped.append(text)

    resultsLoop(canvas, canvasWidth, canvasHeight, inactiveColor, font, wordBankStripped, timeRan, wordsTyped)

if __name__ == '__main__':
    pygame.init()
    main(done, runTime, firstRun, active)
    pygame.quit()