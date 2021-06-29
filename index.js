const SlackBot = require('slackbots');
const axios = require('axios');

const bot = new SlackBot({
	token: 'xoxb-2231900078929-2235211543121-6BJRGkSwkIw84eLSccMnxcDb',
	name: 'jokebot2'
});

// Start Handler
bot.on('start', () => {
	const params = {
		icon_emoji: ':smiley'
	}

	bot.postMessageToChannel('general', 'Get ready to laugh with @JokeBot2!', params);
})

// Error Handler
bot.on('error', (err) => {
	console.log(err)
});

// Message Handler
bot.on('message', (data) => {
	if (data.type !== 'message') {
		return;
	}

	console.log(data);
})

// Respond to mentions
function handleMessage(message) {
	if(message.includes(' chucknorris')) {
		chuckJoke();
	}
}

// Tell a Chuck Norris Joke
function chuckJoke() {
	const params = {
		icon_emoji: ':laughing:'
	}
	bot.postMessageToChannel('general', 'insert funny chuck norris joke', params)
}