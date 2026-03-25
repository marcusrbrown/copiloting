import {defineConfig} from '@bfra.me/eslint-config'

export default defineConfig(
  {
    name: 'copiloting',
    ignores: [
      '**/AGENTS.md',
      'course/pdf-dist/client/build/',
      'course/pdf-dist/client/.svelte-kit/',
      'dist/',
      '.venv/',
      '.worktrees/',
    ],
    typescript: true,
  },
  {
    rules: {
      'node/prefer-global/process': 'off',
      '@typescript-eslint/no-use-before-define': 'off',
    },
  },
  {
    files: ['**/*.json', '**/*.json5', '**/*.jsonc'],
    rules: {
      'jsonc/indent': 'off',
      'jsonc/quotes': 'off',
      'jsonc/quote-props': 'off',
      'jsonc/object-curly-spacing': 'off',
      'jsonc/comma-dangle': 'off',
    },
  },
  {
    files: ['**/*.yaml', '**/*.yml'],
    rules: {
      'yml/quotes': 'off',
    },
  },
  {
    files: ['tutorials/**'],
    rules: {
      'no-console': 'off',
    },
  },
)
