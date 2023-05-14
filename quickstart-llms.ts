// Quickstart using LLMs
// This tutorial is a quick walkthrough about building an end-to-end language model application using LangChain.

import {OpenAI} from 'langchain/llms/openai';
import {initializeAgentExecutorWithOptions} from 'langchain/agents';
import {SerpAPI} from 'langchain/tools';
import {Calculator} from 'langchain/tools/calculator';

const llm = new OpenAI({temperature: 0});
const tools = [
  new SerpAPI(process.env['SERPAPI_API_KEY'], {
    location: 'Maricopa, Arizona, United States',
    hl: 'en',
    gl: 'us',
  }),
  new Calculator(),
];
const executor = await initializeAgentExecutorWithOptions(tools, llm, {
  agentType: 'zero-shot-react-description',
});
const input =
  'How old was Prince when he died?' +
  ' What is his age raised to the 0.23 power?';
console.log(`Executing agent with input: ${input}`);

const result = await executor.call({input});
console.log(`Result: ${result['output']}`);
