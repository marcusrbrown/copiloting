// Quickstart using LLMs
// This tutorial is a quick walkthrough about building an end-to-end language model application using LangChain.

import {PromptTemplate} from '@langchain/core/prompts'
import {ChatOpenAI} from '@langchain/openai'

const llm = new ChatOpenAI({temperature: 0})

const prompt = PromptTemplate.fromTemplate(
  'How old was {person} when they died? What is that age raised to the 0.23 power?',
)

const chain = prompt.pipe(llm)

const result = await chain.invoke({person: 'Prince'})
console.log(`Result: ${result.content}`)
