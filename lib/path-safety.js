import { isAbsolute, relative, resolve } from 'node:path';

const SAFE_SKILL_ID = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;

/**
 * Validate and return a skill id safe to use as one directory name.
 * @param {unknown} id
 * @returns {string}
 */
export function assertSafeSkillId(id) {
  if (typeof id !== 'string' || !SAFE_SKILL_ID.test(id) || id === '.' || id === '..') {
    throw new Error(`Unsafe skill id: ${String(id)}`);
  }
  return id;
}

/**
 * Resolve path segments and ensure result remains under root.
 * @param {string} root
 * @param {...string} segments
 * @returns {string}
 */
export function resolveWithin(root, ...segments) {
  const resolvedRoot = resolve(root);
  const resolvedPath = resolve(resolvedRoot, ...segments);
  const rel = relative(resolvedRoot, resolvedPath);
  if (isAbsolute(rel) || rel === '..' || rel.startsWith(`..${requireSeparator()}`)) {
    throw new Error(`Path escapes root: ${resolvedPath}`);
  }
  return resolvedPath;
}

function requireSeparator() {
  return process.platform === 'win32' ? '\\' : '/';
}
