const SlackBot = require('slackbots');
const axios = require('axios');
const {spawn} = require('child_process');

const bot = new SlackBot({
	token: 'xoxb-2231900078929-2235211543121-uOzFqHuffIIggjd8xxFyGWGd',
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
	handleMessage(data);
})

// Respond to mentions
function handleMessage(data) {
	message = data['text']
	if(message.includes(' chucknorris')) {
		chuckJoke();
	} else if(message.includes(' report')) {
		sendReport();
	}
}

// Compile and send report
function sendReport() {
	const params = {
		icon_emoji: ':bar_chart:'
	}
	const python = spawn('python', ['test.py']);
	python.stdout.on('data', function (data) {
		bot.postMessageToChannel('general', data.toString(), params);
	});
}

// Tell a Chuck Norris Joke
function chuckJoke() {
	const params = {
		icon_emoji: ':laughing:'
	}
	bot.postMessageToChannel('general', 'insert funny chuck norris joke', params)
}