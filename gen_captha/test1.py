from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha

# audio = AudioCaptcha(voicedir='/path/to/voices')
image = ImageCaptcha(fonts=['arial.ttf'])
image.character_rotate = (-40, 40)
image.character_warp_dx = (0.1, 0.5)
image.character_warp_dy = (0.1, 0.5)
image.character_offset_dx = (0, 4)
image.character_offset_dy = (0, 6)
image.word_space_probability = 0
# data = audio.generate('1234')
# audio.write('1234', 'out.wav')

data = image.generate('2131')
image.write('cszm7g', 'out.png')

https://stackoverflow.com/questions/5549562/running-php-script-php-function-in-linux-bash
user PHP максимальная схожесть
нарезать буквы

https://proglib.io/p/lomay-menya-polnostyu-kak-odni-algoritmy-generiruyut-kapchu-a-drugie-ee-vzlamyvayut-2020-03-05
LSTM (256, 6-7-8), 
samples: 100 000 - 150 000, 94%, 97%