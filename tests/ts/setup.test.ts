import {describe, expect, it} from 'vitest'

describe('project setup', () => {
  it('should have correct Node.js version range', () => {
    const major = Number.parseInt(process.version.slice(1).split('.')[0] ?? '0', 10)
    expect(major).toBeGreaterThanOrEqual(16)
  })

  it('should have required environment support for ES modules', () => {
    expect(typeof import.meta.url).toBe('string')
  })
})
