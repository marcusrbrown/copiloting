import config from '@bfra.me/prettier-config'

export default {
  ...config,
  plugins: ['prettier-plugin-svelte'],
  overrides: [...(config.overrides || []), {files: '*.svelte', options: {parser: 'svelte'}}],
}
