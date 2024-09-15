"use client";
import Image from "next/image";
import config from "../../config.json";
import { useState } from "react";
import { ITweet } from "./types/types";

export default function Home() {
  const [results, setResults] = useState<ITweet[]>([]);
  const [subject, setSubject] = useState<string>("");
  const onSubmit = () => {
    setResults([]);
    config.agents.forEach(async (agent) => {
      try {
        const startTime = performance.now();
        const response = await fetch(`${agent.url}?subject=${subject}`);
        const endTime = performance.now();
        console.log(
          `Call to ${agent.url} took ${endTime - startTime} milliseconds.`
        );
        const result = await response.json();
        setResults((prevResults) => prevResults.concat(result));
      } catch (error) {
        console.error(`Error fetching data from ${agent.url}:`, error);
      }
    });
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 items-center sm:items-start">
        <div className="mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="relative isolate overflow-hidden bg-gray-900 px-6 py-24 shadow-2xl sm:rounded-3xl sm:px-24 xl:py-32">
            <h2 className="mx-auto max-w-2xl text-center text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Social media posts for your business.
            </h2>
            <p className="mx-auto mt-2 mb-4 max-w-xl text-center text-lg leading-8 text-gray-300">
              Please describe what your business is doing, and our agents will
              handle the rest.
            </p>

            <div className="flex">
              <label htmlFor="subject" className="sr-only">
                Subject
              </label>
              <input
                id="subject"
                name="subject"
                type="text"
                required
                placeholder="Subject"
                value={subject}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault(); // Prevent the default form submission
                    onSubmit();
                  }
                }}
                onChange={(e) => {
                  setSubject(e.target.value);
                }}
                className="min-w-0 flex-auto rounded-md border-0 bg-white/5 px-3.5 py-2 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-white sm:text-sm sm:leading-6 flex mr-4"
              />
              <button
                className="flex-none rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
                onClick={onSubmit}
              >
                Get started
              </button>
            </div>

            <div className="mt-10">
              {results?.map((result, id) => (
                <div
                  key={id}
                  className="tweet p-4 border-b border-gray-200 bg-white rounded mt-3"
                >
                  <div className="tweet-header flex items-center space-x-2">
                    <span className="username font-bold">SocialsSwarm</span>
                    <span className="handle text-gray-500">@socialsswarm</span>
                    <span className="time text-gray-500">· 1h</span>
                  </div>
                  <div className="tweet-content mt-2 text-gray-900">
                    {result.text}
                  </div>
                  {result.link_url && (
                    <div className="newspaper-skeleton mt-4 p-4 border border-gray-300 bg-gray-100 rounded">
                      <div className="skeleton-header h-6 bg-gray-300 rounded w-3/4 mb-2"></div>
                      <div className="skeleton-content space-y-2">
                        <div className="h-4 bg-gray-300 rounded w-full"></div>
                        <div className="h-4 bg-gray-300 rounded w-5/6"></div>
                        <div className="h-4 bg-gray-300 rounded w-2/3"></div>
                        <div className="mt-2 text-blue-500">
                          <a
                            href={result.link_url}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {result.link_url}
                          </a>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            <svg
              viewBox="0 0 1024 1024"
              aria-hidden="true"
              className="absolute left-1/2 top-1/2 -z-10 h-[64rem] w-[64rem] -translate-x-1/2"
            >
              <circle
                r={512}
                cx={512}
                cy={512}
                fill="url(#759c1415-0410-454c-8f7c-9a820de03641)"
                fillOpacity="0.7"
              />
              <defs>
                <radialGradient
                  r={1}
                  cx={0}
                  cy={0}
                  id="759c1415-0410-454c-8f7c-9a820de03641"
                  gradientUnits="userSpaceOnUse"
                  gradientTransform="translate(512 512) rotate(90) scale(512)"
                >
                  <stop stopColor="#7775D6" />
                  <stop offset={1} stopColor="#E935C1" stopOpacity={0} />
                </radialGradient>
              </defs>
            </svg>
          </div>
        </div>
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        Pizza2Agents
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://lablab.ai/event/ai-agents-hack-with-lablab-and-mindsdb/pizza2agents"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="https://nextjs.org/icons/globe.svg"
            alt="Globe icon"
            width={16}
            height={16}
          />
          AI Agent Hackathon SF, September 2024 →
        </a>
      </footer>
    </div>
  );
}
