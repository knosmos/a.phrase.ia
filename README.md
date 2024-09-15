# a.phrase.ia
helping speech-impaired patients communicate through natural language, using multimodal AI | HackMIT 2024
---

## What it does
Gives a voice to aphasia patients by converting pictorial sequences (i.e., emojis) into natural English speech. There’s 97 million people that suffer from speech or communication disorders, and currently, state of the art assistive technology is $400 communication boards that literally say a word when you press a button. Our solution synthesizes and speaks natural sentences, uses a recommendation algorithm to predict the most relevant phrases, and is extensible with custom AI-generated emoji that can be made just by taking a photo.

## How we built it
We use Tune Studio’s powerful Blob AI Assistant via Langchain to generate English sentences from emoji sequences. We also use it to generate synthetic emoji sequence data to train the recommendation algorithm: people normally don’t communicate entirely using emoji, so we instead use twitter messages (chosen because they are relatively simple compared to other forms of text) and convert them into emojis. From there, we can run a lightweight n-gram Markov chain to generate recommendations; this approach ensures that the recommendation is lightning-fast while also being relevant.

Our custom emoji generation is done in two steps: the multimodal Pixtral-12B analyzes the camera feed to generate image descriptions that are used internally, and a computer vision pipeline using Flux.1-schnell takes the descriptions to create a visual emoji that is displayed to the user.

To learn and adapt to each user, we store user histories in MongoDB that are used to finetune the recommendation system; each user is authenticated using Clerk. The app is built with React-Native, with a FastAPI backend.

## Challenges we ran into
Building an intuitive app without any text. Fighting react-native (WHY does it not have CSS-grid. Or a canvas). Fighting 22434 different AI models. Trying to parse emoji.

## Accomplishments that we're proud of
Pulling together so many different systems and technologies in a short period of time. Building an app that (we think) uses LLMs without just being yet another ChatGPT wrapper (in fact, LLM text outputs are never displayed). Resisting the urge to down multiple RedBulls during the dark hours of the night.
