# course/pdf-dist/client/AGENTS.md

## OVERVIEW

SvelteKit frontend for the PDF chat app. Communicates with Flask backend via axios (`/api/*`). Built as static site (adapter-static) and served by Flask from `client/build/`. Uses Svelte 5 + Tailwind + Preline UI.

## STRUCTURE

```
client/src/
├── routes/                     # SvelteKit file-based routing
│   ├── +layout.svelte          # Root layout: Navbar + auth guard
│   ├── +layout.ts              # Load function: fetch user role
│   ├── +page.svelte            # Home/redirect page
│   ├── auth/                   # signin, signout, signup pages
│   ├── chat/+page.svelte       # Main chat UI
│   ├── documents/              # PDF list, upload, single PDF view ([id])
│   └── scores/+page.svelte     # A/B score visualization (BarChart)
├── components/
│   ├── chat/                   # ChatPanel, ChatList, ChatInput, messages, ConversationSelect
│   ├── auth/                   # AuthLinks
│   └── {Alert, AuthGuard, BarChart, Button, FormGroup, Icon, Navbar,
│          PdfViewer, Progress, TextInput, ErrorMessage, ErrorModal}.svelte
├── store/
│   ├── auth.ts                 # Auth state (user session)
│   ├── chat/                   # Chat state: store.ts, stream.ts, sync.ts, index.ts
│   ├── documents.ts            # PDF list state
│   ├── errors.ts               # Global error store (addError)
│   ├── role.ts                 # User role store
│   ├── scores.ts               # A/B score data
│   ├── store.ts                # Root Svelte store exports
│   └── writeable.ts            # Base writable store helpers
└── api/
    └── axios.ts                # Axios instance (/api base URL) + error interceptor
```

## WHERE TO LOOK

| Task              | Location                                                    |
| ----------------- | ----------------------------------------------------------- |
| Page routes       | `src/routes/` — SvelteKit `+page.svelte` files              |
| Chat UI           | `src/routes/chat/+page.svelte` + `src/components/chat/`     |
| PDF management UI | `src/routes/documents/`                                     |
| API calls         | `src/api/axios.ts` — `api` instance; use `api.get/post/...` |
| Global errors     | `src/store/errors.ts` — `addError()`                        |
| Auth state        | `src/store/auth.ts`                                         |
| Streaming chat    | `src/store/chat/stream.ts`                                  |

## CONVENTIONS

- **Path aliases** (do not use relative paths for these):
  - `$c` → `src/components`
  - `$s` → `src/store`
  - `$api` → `src/api/axios.js`
- All API calls use the `api` axios instance from `$api` — never raw `fetch` for backend
- Tailwind for styling; Preline for UI components; Material Icons for icons
- `svelte-check` for type checking — run `pnpm check` to validate
- ESLint + Prettier enforced; `.svelte` files use svelte parser (tabWidth 2)
- Adapter-static with `fallback: 'index.html'` — SPA routing handled by Flask catch-all

## ANTI-PATTERNS

- Do not use raw `fetch` for `/api/*` calls — use the `api` axios instance
- Do not import from `src/store` using relative paths — use `$s/...`
- Do not import from `src/components` using relative paths — use `$c/...`
- Do not import from `src/api/axios.ts` using relative paths — use `$api`
- Do not build with `npm` or `yarn` — this is a pnpm workspace

## COMMANDS

```bash
# From repo root
pnpm -C course/pdf-dist/client run dev      # dev server (requires Flask running)
pnpm -C course/pdf-dist/client run build    # build static → client/build/
pnpm -C course/pdf-dist/client run check    # svelte-check type validation
pnpm -C course/pdf-dist/client run lint     # Prettier + ESLint check
```

## NOTES

- `build/` output is committed and served by Flask — run `pnpm build` before deploying
- Chat supports both streaming (SSE via `@microsoft/fetch-event-source`) and sync modes
- `PdfViewer` uses `pdfjs-dist` for in-browser PDF rendering
- Svelte 5 (5.54.0) — uses runes-era APIs if any new components are added
