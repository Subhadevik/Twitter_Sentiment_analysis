document.getElementById('tweetForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const tweet = document.getElementById('tweetInput').value;

    if (tweet) {
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ tweet })
            });

            const data = await response.json();

            if (response.ok) {
                document.getElementById('result').innerHTML = `The sentiment is: <strong>${data.sentiment}</strong>`;
            } else {
                document.getElementById('result').innerHTML = 'Error: Could not analyze the sentiment.';
            }
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('result').innerHTML = 'Error: Could not analyze the sentiment.';
        }
    } else {
        document.getElementById('result').innerHTML = 'Please enter a tweet.';
    }
});
