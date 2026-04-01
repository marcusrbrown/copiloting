// Quickstart using LLMs
// This tutorial is a quick walkthrough about building an end-to-end language model application using LangChain.

import {PromptTemplate} from '@langchain/core/prompts'
import {OpenAI} from '@langchain/openai'
import {LLMChain} from 'langchain/chains'

const llm = new OpenAI({temperature: 0})

const prompt = PromptTemplate.fromTemplate(
  'How old was {person} when they died? What is that age raised to the 0.23 power?',
)

const chain = new LLMChain({llm, prompt})

const result = await chain.call({person: 'Prince'})
console.log(`Result: ${result.text}`)
