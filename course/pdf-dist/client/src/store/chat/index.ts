import type {Conversation, Message, MessageOpts} from './store'
import {
  createConversation,
  fetchConversations,
  getActiveConversation,
  resetAll,
  resetError,
  scoreConversation,
  set,
  setActiveConversationId,
  store,
} from './store.js'
import {sendMessage as sendStreamingMessage} from './stream'
import {sendMessage as sendSyncMessage} from './sync'

const sendMessage = (message: Message, opts: MessageOpts) => {
  return opts.useStreaming
    ? sendStreamingMessage(message /* , opts */)
    : sendSyncMessage(message /* , opts */)
}

export {
  Conversation,
  createConversation,
  fetchConversations,
  getActiveConversation,
  resetAll,
  resetError,
  scoreConversation,
  sendMessage,
  set,
  setActiveConversationId,
  store,
}
