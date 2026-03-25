import {api, getErrorMessage} from '$api'
import {get, writable} from 'svelte/store'

export type User =
  | {
      id: string
      email: string
    }
  | null
  | false

interface AuthInfo {
  user: User
  error: string
  loading: boolean
}

const INITIAL_STATE = {
  user: null,
  error: '',
  loading: false,
}

const auth = writable<AuthInfo>(INITIAL_STATE)

const set = (val: Partial<AuthInfo>) => {
  auth.update(state => ({...state, ...val}))
}

const getUser = async () => {
  const {loading, user} = get(auth)

  if (loading) {
    return user
  }
  set({loading: true})
  try {
    const {data} = await api.get('/auth/user')
    if (data) {
      set({user: data, error: ''})
    } else {
      set({user: false, error: ''})
    }
    return data
  } catch {
    set({user: false})
    return false
  } finally {
    set({loading: false})
  }
}

const signin = async (email: string, password: string) => {
  set({error: '', loading: true})

  try {
    const {data} = await api.post('/auth/signin', {email, password})
    set({
      user: data,
      error: '',
    })
  } catch (error) {
    set({error: getErrorMessage(error)})
  } finally {
    set({loading: false})
  }
}

const signout = async () => {
  set({loading: true})
  try {
    await api.post('/auth/signout')
    set(INITIAL_STATE)
  } catch (error) {
    set({error: getErrorMessage(error)})
  } finally {
    set({loading: false})
  }
}

const signup = async (email: string, password: string) => {
  set({error: '', loading: true})

  try {
    const {data} = await api.post('/auth/signup', {email, password})
    set({user: data, error: ''})
  } catch (error) {
    set({error: getErrorMessage(error)})
  } finally {
    set({loading: false})
  }
}

const clearErrors = () => {
  set({error: '', loading: false})
}

export {auth, clearErrors, getUser, signin, signout, signup}
