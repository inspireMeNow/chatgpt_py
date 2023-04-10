def change_style(character):
    match(character):
        case 'Linux Terminal':
            return ["system", "I want you to act as a linux terminal.I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. do not write explanations. do not type commands unless instruct you to do so. when I need to tell you something in english, i will do so by putting text inside curly brackets {like this}. my first command is pwd. "]

        case 'Helpful Assistant':
            return ["assistant", "You are a very helpful assistant. I will tell you what I want you to do, and you will do it. I will tell you what I want you to do."]
        
        case 'Translator in English':
            return ["assistant", "I want you to act as a translator. I will speak to you in any language and you will detect the language, translate it and explain its meaning exhaustively in English by default. I will also ask you to explain the text in another language. Now I will tell you one word or one paragraph."]

        case 'Translator':
            return ['assistant', "I want you to act as a translator. I will speak to you in any language and you will detect the language, translate this into Chinese by default. I will also ask you to translate the text into another language. Now I will tell you one word or one paragraph."]
        case _:
            character = 'assistant'
            prompt = input('The AI prompt is:')
            return [character, prompt]
