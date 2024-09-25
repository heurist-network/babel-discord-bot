# Babel Bot for Discord translation and moderation

![babel](https://github.com/user-attachments/assets/534d9434-b818-466b-adde-5fa5e93e970a)

Babel Bot provides seamless two-way language translation for your Discord server. It enables automatic translation of messages from international channels to an English channel, ensuring that all users can understand the conversations. Additionally, users can use a command to translate English messages and send them to international channels, facilitating communication across language barriers.

## Features

- Automatic Translation: All messages posted in the designated international channels are automatically translated to English and sent to a specified English channel. This allows users who don't speak the original language to follow the conversations.
- Command-based Translation: Users can use the /translate command followed by the target language and the message text to translate English messages and send them to the corresponding international channel. This enables users to actively participate in discussions in different languages.
- Content Moderation: The bot incorporates content moderation to ensure a safe and respectful environment. It filters out any inappropriate or offensive language during the translation process.
- OpenAI Compatible: Any OpenAI-compatible API can be easily plugged in. We recommend Mixtral-8x7b deployed on Heurist, a decentralized GPU network for AI inference, to perform accurate and efficient translations. You can use `https://llm-gateway.heurist.xyz` as the `LLM_API_URL`. API documentations: https://docs.heurist.ai/integration/heurist-llm-gateway

## Usage

### Automatic Translation

Simply post messages in the designated international channels, and they will be automatically translated and sent to the specified English channel.

### Command-based Translation

Use the `/translate` command followed by the target language and the message text.

Example: `/translate Spanish Hello, how are you?`

The translated message will be sent to the corresponding international channel.

## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License
This project is licensed under the MIT License.
