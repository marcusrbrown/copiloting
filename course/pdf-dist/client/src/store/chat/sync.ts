import type {Message} from './store'
import {api, getErrorMessage} from '$api'
import {insertMessageToActive, removeMessageFromActive, set, store} from './store'

const _addPendingMessage = (message: Message, pendingId: number) => {
  insertMessageToActive(message)
  insertMessageToActive({
    id: pendingId,
    role: 'pending',
    content: '...',
  })
}

export const sendMessage = async (message: Message) => {
  set({loading: true})
  const pendingId = Math.random()
  try {
    _addPendingMessage(message, pendingId)

    const conversationId = store.get().activeConversationId
    const {data: responseMessage} = await api.post<Message>(
      `/conversations/${conversationId}/messages`,
      {
        input: message.content,
      },
    )

    removeMessageFromActive(pendingId)
    insertMessageToActive(responseMessage)
    set({error: '', loading: false})
  } catch (error) {
    set({error: getErrorMessage(error), loading: false})
  }
}
