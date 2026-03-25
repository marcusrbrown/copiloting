import type {Message} from './store'
import {getErrorMessage} from '$api'
import {addError} from '$s/errors'
import {getActiveConversation, insertMessageToActive, set, store} from './store'

const _addMessage = (message: Message) => {
  insertMessageToActive(message)
}

const _appendResponse = (id: number, text: string) => {
  store.update(state => {
    const conv = state.conversations.find(c => c.id === state.activeConversationId)
    if (!conv) {
      return
    }
    conv.messages = conv.messages.map(message => {
      if (message.id === id) {
        message.content += text
        message.role = 'assistant'
      }
      return message
    })
  })
}

export const sendMessage = async (userMessage: Message) => {
  const conversation = getActiveConversation()

  if (!conversation) {
    return
  }

  set({loading: true})

  const responseMessage = {
    role: 'pending',
    content: '',
    id: Math.random(),
  } as Message

  try {
    _addMessage(userMessage)
    _addMessage(responseMessage)

    const response = await fetch(`/api/conversations/${conversation.id}/messages?stream=true`, {
      method: 'POST',
      body: JSON.stringify({
        input: userMessage.content,
      }),
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    const reader = response.body?.getReader()
    if (!reader) {
      return
    }
    if (response.status >= 400) {
      await readError(response.status, reader)
    } else {
      await readResponse(reader, responseMessage)
    }
  } catch (error) {
    set({error: getErrorMessage(error), loading: false})
  }
}

const readResponse = async (
  reader: ReadableStreamDefaultReader<Uint8Array>,
  responseMessage: Message,
) => {
  let inProgress = true

  while (inProgress) {
    const {done, value} = await reader.read()
    if (done) {
      inProgress = false
      break
    }
    const text = new TextDecoder().decode(value)

    if (responseMessage.id) {
      _appendResponse(responseMessage.id, text)
    }
  }
}

const readError = async (statusCode: number, reader: ReadableStreamDefaultReader<Uint8Array>) => {
  let inProgress = true
  let message = ''
  while (inProgress) {
    const {done, value} = await reader.read()
    if (done) {
      inProgress = false
      break
    }
    const text = new TextDecoder().decode(value)
    message += text
  }

  if (statusCode >= 500) {
    addError({
      message,
      contentType: message.includes('<!doctype html>') ? 'text/html' : '',
    })
  } else {
    try {
      set({error: getErrorMessage(JSON.parse(message))})
    } catch {
      set({error: getErrorMessage(message)})
    }
  }
}
