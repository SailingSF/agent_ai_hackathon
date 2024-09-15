'use client';

import { useState } from 'react';

interface ITweet {
  text: string;
  image_url?: string;
}

export default function Home() {
  const [results, setResults] = useState<ITweet[]>([]);
  const [subject, setSubject] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const onSubmit = async () => {
    setResults([]);
    setIsLoading(true);
    try {
      console.log(`Sending request to: http://localhost:5001/generate_tweets`);
      const startTime = performance.now();
      const response = await fetch(`http://localhost:5001/generate_tweets?subject=${encodeURIComponent(subject)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',
      });
      const endTime = performance.now();
      console.log(`Call to generate_tweets took ${endTime - startTime} milliseconds.`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result: { tweets: string } = await response.json();
      console.log(`Generated tweets:`, result.tweets);
      
      // Ensure result.tweets is a string and split it into an array
      const tweetsArray = result.tweets.split('\n').filter(tweet => tweet.trim() !== '');
      
      // Map each tweet to an ITweet object
      setResults(tweetsArray.map((tweet: string) => ({ text: tweet.trim() })));
    } catch (error) {
      console.error(`Error fetching data:`, error);
    } finally {
      setIsLoading(false);
    }
  };

  const postTweet = async (tweetText: string) => {
    try {
      // Placeholder function for posting a tweet
      console.log(`Posting tweet: ${tweetText}`);
      // TODO: Implement the actual API call to post the tweet
      // const response = await fetch('http://localhost:5001/post_tweet', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ text: tweetText }),
      // });
      // if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      // const result = await response.json();
      // console.log('Tweet posted successfully:', result);
    } catch (error) {
      console.error('Error posting tweet:', error);
    }
  };

  return (
     <div className="grid grid-rows-[20px_1fr_20px] min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 items-center sm:items-start">
        <div className="mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="relative isolate overflow-hidden bg-gray-900 px-6 py-24 shadow-2xl sm:rounded-3xl sm:px-24 xl:py-32">
            <h2 className="mx-auto max-w-2xl text-center text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Social media posts for your business.
            </h2>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="Enter a subject"
                className="rounded-md bg-white/5 px-3.5 py-2.5 text-white shadow-sm ring-1 ring-inset ring-white/10"
              />
              <button
                onClick={onSubmit}
                disabled={isLoading}
                className="rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white disabled:opacity-50"
              >
                {isLoading ? 'Generating...' : 'Generate'}
              </button>
            </div>
          </div>
        </div>
        <div className="w-full max-w-7xl grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {results.map((tweet, index) => (
            <div key={index} className="p-4 bg-gray-100 rounded-lg flex flex-col justify-between">
              <p className="mb-4">{tweet.text}</p>
              {tweet.image_url && <img src={tweet.image_url} alt="Tweet image" className="mb-4 max-w-full h-auto" />}
              <button
                onClick={() => postTweet(tweet.text)}
                className="self-end rounded-md bg-blue-500 px-3.5 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-500"
              >
                Post
              </button>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}