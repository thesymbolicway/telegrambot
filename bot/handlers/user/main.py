from aiogram import Dispatcher
from aiogram.types import Message
import openai
from elevenlabs import generate, set_api_key
import io

MAX_MESSAGE_LENGTH = 400  

API_KEY = '0a75c82123947e8cb147ec2afea99a18'
VOICE_NAME = 'Rachel'  

# Set your API key for ElevenLabs
set_api_key(API_KEY)

def register_user_handlers(dp: Dispatcher):

    @dp.message_handler(commands='start')
    async def start(message: Message):
        await message.answer('Hello there!')

    @dp.message_handler(lambda message: len(message.text) <= MAX_MESSAGE_LENGTH)
    async def message_from_user(message: Message):
        # Truncate user's message if it's too long
        user_message = message.text[:MAX_MESSAGE_LENGTH] + (message.text[MAX_MESSAGE_LENGTH:] and '...')

        # Use a more open-ended prompt and include user's truncated message
        prompt = f"You are pornstar Lisa Ann. Chat as if you were pornstar Lisa Ann. User says: '{user_message}'"
        
        try:
            # Send the prompt to OpenAI's API
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.9,
                max_tokens=1090,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=["You:"]
            )

            # Extract the model's response
            bot_response = response['choices'][0]['text'].strip()
            await message.answer(bot_response)
            
        # Convert the bot's response to speech
            audio = generate(text=bot_response, voice=VOICE_NAME, model="eleven_multilingual_v2")
            
            audio_file = io.BytesIO(audio)
            audio_file.name = "response.ogg"
            await message.answer_voice(voice=audio_file)


        except Exception as e:
            await message.answer("Sorry, I encountered an issue. Please try again later.")
            # Log the error for debugging
            print(f"Error: {e}")

    @dp.message_handler(lambda message: len(message.text) > MAX_MESSAGE_LENGTH)
    async def long_message(message: Message):
        await message.answer("Your message is too long! Please send a shorter message.")
