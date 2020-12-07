def getAnswer(data, question): 
    index = data.find(question)
    data = data[(index):]
    gapText = '<br> <br><br>Please select the best answer from the choices provided.</div></div></div></div></div><div class="CardsItem-legendBox"><div class="CardsItem-legendBoxClick"><span class="UIText UIText--specialThree">Click card to see definition 👆</span></div><div class="CardsItem-legendBoxTap"><span class="UIText UIText--specialThree">Tap card to see definition 👆</span></div></div></div><div aria-hidden="true" class="CardsItemSide CardsItemSide--secondSide CardsItemSide--lastSide has-text" role="presentation"><div class="CardsItemInner CardsItemInner--showBox"><div class="CardsItemInner-cell"><div class="FormattedTextWithImage"><div aria-label="True" class="FormattedText notranslate lang-en" style="font-size: 30px;"><div style="display: block;">'
    index = data.find(gapText)
    data = data[(index + len(gapText)):]
    index = data.find('</div>')
    data = data[:index]
    text_file = open("answer.txt", "w")
    text_file.write(data)
    text_file.close()
    return data

with open('Output.txt','r') as file:
    text = file.read()

questionSearch = 'Over the past 20 years, the efforts of the United States have decreased the amount of pollutants in the environment.'
getAnswer(text, questionSearch)