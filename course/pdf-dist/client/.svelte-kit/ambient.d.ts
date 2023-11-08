
// this file is generated — do not edit it


/// <reference types="@sveltejs/kit" />

/**
 * Environment variables [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env`. Like [`$env/dynamic/private`](https://kit.svelte.dev/docs/modules#$env-dynamic-private), this module cannot be imported into client-side code. This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://kit.svelte.dev/docs/configuration#env).
 * 
 * _Unlike_ [`$env/dynamic/private`](https://kit.svelte.dev/docs/modules#$env-dynamic-private), the values exported from this module are statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * ```ts
 * import { API_KEY } from '$env/static/private';
 * ```
 * 
 * Note that all environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * 
 * ```
 * MY_FEATURE_FLAG=""
 * ```
 * 
 * You can override `.env` values from the command line like so:
 * 
 * ```bash
 * MY_FEATURE_FLAG="enabled" npm run dev
 * ```
 */
declare module '$env/static/private' {
	export const NVM_INC: string;
	export const LC_FIG_SET_PARENT: string;
	export const FIG_PID: string;
	export const COREPACK_ROOT: string;
	export const STARSHIP_SHELL: string;
	export const TERM_PROGRAM: string;
	export const NVM_CD_FLAGS: string;
	export const HOMEBREW_NO_INSECURE_REDIRECT: string;
	export const TERM: string;
	export const SHELL: string;
	export const FIGTERM_SESSION_ID: string;
	export const HOMEBREW_SORBET_RUNTIME: string;
	export const TMPDIR: string;
	export const TERM_PROGRAM_VERSION: string;
	export const SRC_ENDPOINT: string;
	export const TERM_SESSION_ID: string;
	export const PMSPEC: string;
	export const NVM_DIR: string;
	export const USER: string;
	export const LS_COLORS: string;
	export const HOMEBREW_DEVELOPER: string;
	export const COMMAND_MODE: string;
	export const HOMEBREW_NO_ANALYTICS: string;
	export const SHPROFILE_LOADED: string;
	export const MANROFFOPT: string;
	export const SSH_AUTH_SOCK: string;
	export const __CF_USER_TEXT_ENCODING: string;
	export const PAGER: string;
	export const LSCOLORS: string;
	export const PATH: string;
	export const FIG_HOSTNAME: string;
	export const LaunchInstanceID: string;
	export const HOMEBREW_BOOTSNAP: string;
	export const __CFBundleIdentifier: string;
	export const npm_command: string;
	export const TTY: string;
	export const PWD: string;
	export const HOMEBREW_INSTALL_CLEANUP: string;
	export const LANG: string;
	export const HOMEBREW_AUTOREMOVE: string;
	export const SRC_ACCESS_TOKEN: string;
	export const ITERM_PROFILE: string;
	export const NODE_PATH: string;
	export const HOMEBREW_CLEANUP_MAX_AGE_DAYS: string;
	export const XPC_FLAGS: string;
	export const XPC_SERVICE_NAME: string;
	export const GPG_TTY: string;
	export const FIG_PARENT: string;
	export const MANPAGER: string;
	export const SHLVL: string;
	export const HOME: string;
	export const COLORFGBG: string;
	export const _ZPM_DIR: string;
	export const GOROOT: string;
	export const LC_TERMINAL_VERSION: string;
	export const HOMEBREW_PREFIX: string;
	export const ZSH_CACHE_DIR: string;
	export const FIG_SET_PARENT: string;
	export const ITERM_SESSION_ID: string;
	export const STARSHIP_SESSION_KEY: string;
	export const LOGNAME: string;
	export const LESS: string;
	export const PNPM_PACKAGE_NAME: string;
	export const HOMEBREW_CLEANUP_PERIODIC_FULL_DAYS: string;
	export const NVM_BIN: string;
	export const GOPATH: string;
	export const npm_config_user_agent: string;
	export const LC_TERMINAL: string;
	export const DISPLAY: string;
	export const SECURITYSESSIONID: string;
	export const HOMEBREW_NO_ENV_HINTS: string;
	export const FIG_TERM: string;
	export const COLORTERM: string;
}

/**
 * Similar to [`$env/static/private`](https://kit.svelte.dev/docs/modules#$env-static-private), except that it only includes environment variables that begin with [`config.kit.env.publicPrefix`](https://kit.svelte.dev/docs/configuration#env) (which defaults to `PUBLIC_`), and can therefore safely be exposed to client-side code.
 * 
 * Values are replaced statically at build time.
 * 
 * ```ts
 * import { PUBLIC_BASE_URL } from '$env/static/public';
 * ```
 */
declare module '$env/static/public' {

}

/**
 * This module provides access to runtime environment variables, as defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/master/packages/adapter-node) (or running [`vite preview`](https://kit.svelte.dev/docs/cli)), this is equivalent to `process.env`. This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://kit.svelte.dev/docs/configuration#env).
 * 
 * This module cannot be imported into client-side code.
 * 
 * ```ts
 * import { env } from '$env/dynamic/private';
 * console.log(env.DEPLOYMENT_SPECIFIC_VARIABLE);
 * ```
 * 
 * > In `dev`, `$env/dynamic` always includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 */
declare module '$env/dynamic/private' {
	export const env: {
		NVM_INC: string;
		LC_FIG_SET_PARENT: string;
		FIG_PID: string;
		COREPACK_ROOT: string;
		STARSHIP_SHELL: string;
		TERM_PROGRAM: string;
		NVM_CD_FLAGS: string;
		HOMEBREW_NO_INSECURE_REDIRECT: string;
		TERM: string;
		SHELL: string;
		FIGTERM_SESSION_ID: string;
		HOMEBREW_SORBET_RUNTIME: string;
		TMPDIR: string;
		TERM_PROGRAM_VERSION: string;
		SRC_ENDPOINT: string;
		TERM_SESSION_ID: string;
		PMSPEC: string;
		NVM_DIR: string;
		USER: string;
		LS_COLORS: string;
		HOMEBREW_DEVELOPER: string;
		COMMAND_MODE: string;
		HOMEBREW_NO_ANALYTICS: string;
		SHPROFILE_LOADED: string;
		MANROFFOPT: string;
		SSH_AUTH_SOCK: string;
		__CF_USER_TEXT_ENCODING: string;
		PAGER: string;
		LSCOLORS: string;
		PATH: string;
		FIG_HOSTNAME: string;
		LaunchInstanceID: string;
		HOMEBREW_BOOTSNAP: string;
		__CFBundleIdentifier: string;
		npm_command: string;
		TTY: string;
		PWD: string;
		HOMEBREW_INSTALL_CLEANUP: string;
		LANG: string;
		HOMEBREW_AUTOREMOVE: string;
		SRC_ACCESS_TOKEN: string;
		ITERM_PROFILE: string;
		NODE_PATH: string;
		HOMEBREW_CLEANUP_MAX_AGE_DAYS: string;
		XPC_FLAGS: string;
		XPC_SERVICE_NAME: string;
		GPG_TTY: string;
		FIG_PARENT: string;
		MANPAGER: string;
		SHLVL: string;
		HOME: string;
		COLORFGBG: string;
		_ZPM_DIR: string;
		GOROOT: string;
		LC_TERMINAL_VERSION: string;
		HOMEBREW_PREFIX: string;
		ZSH_CACHE_DIR: string;
		FIG_SET_PARENT: string;
		ITERM_SESSION_ID: string;
		STARSHIP_SESSION_KEY: string;
		LOGNAME: string;
		LESS: string;
		PNPM_PACKAGE_NAME: string;
		HOMEBREW_CLEANUP_PERIODIC_FULL_DAYS: string;
		NVM_BIN: string;
		GOPATH: string;
		npm_config_user_agent: string;
		LC_TERMINAL: string;
		DISPLAY: string;
		SECURITYSESSIONID: string;
		HOMEBREW_NO_ENV_HINTS: string;
		FIG_TERM: string;
		COLORTERM: string;
		[key: `PUBLIC_${string}`]: undefined;
		[key: string]: string | undefined;
	}
}

/**
 * Similar to [`$env/dynamic/private`](https://kit.svelte.dev/docs/modules#$env-dynamic-private), but only includes variables that begin with [`config.kit.env.publicPrefix`](https://kit.svelte.dev/docs/configuration#env) (which defaults to `PUBLIC_`), and can therefore safely be exposed to client-side code.
 * 
 * Note that public dynamic environment variables must all be sent from the server to the client, causing larger network requests — when possible, use `$env/static/public` instead.
 * 
 * ```ts
 * import { env } from '$env/dynamic/public';
 * console.log(env.PUBLIC_DEPLOYMENT_SPECIFIC_VARIABLE);
 * ```
 */
declare module '$env/dynamic/public' {
	export const env: {
		[key: `PUBLIC_${string}`]: string | undefined;
	}
}
