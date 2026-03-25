import type {Scores} from '$s/scores'
import type {PageLoad} from './$types'
import {api, getErrorMessage} from '$api'

export const load = (async () => {
  try {
    const {data} = await api.get<Scores>('/scores')

    return {
      scores: data,
    }
  } catch (error) {
    return {
      error: getErrorMessage(error),
    }
  }
}) satisfies PageLoad
