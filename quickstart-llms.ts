// Quickstart using LLMs
// This tutorial is a quick walkthrough about building an end-to-end language model application using LangChain.

import {OpenAI} from 'langchain/llms/openai';
import {PromptTemplate} from 'langchain/prompts';
import {LLMChain} from 'langchain/chains';

const llm = new OpenAI({temperature: 0.9});
const template =
  'What is a good name for a {product} that is powered by AI and ML? Come up with at least 40 names.';
const prompt = new PromptTemplate({
  template,
  inputVariables: ['product'],
});
const chain = new LLMChain({llm, prompt});
const response = await chain.call({product: 'personal assistant'});
console.log(response);
