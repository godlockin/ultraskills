import { lstat, realpath } from 'node:fs/promises';
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
  assertContained(resolvedRoot, resolvedPath);
  return resolvedPath;
}

/**
 * Verify an existing-root write target has no symlink components and that its
 * real parent remains below the real root. Missing final components are valid.
 * @param {string} root
 * @param {string} target
 * @returns {Promise<string>}
 */
export async function assertSafeWriteTarget(root, target) {
  const resolvedRoot = resolve(root);
  const resolvedTarget = resolve(target);
  assertContained(resolvedRoot, resolvedTarget);

  const rootStat = await lstat(resolvedRoot);
  if (rootStat.isSymbolicLink()) {
    throw new Error(`Refusing symlinked skills root: ${resolvedRoot}`);
  }
  const realRoot = await realpath(resolvedRoot);
  await assertExistingComponents(realRoot, resolvedRoot, resolvedTarget);

  const parent = resolve(resolvedTarget, '..');
  const realParent = await realpath(parent);
  assertContained(realRoot, realParent);
  return resolvedTarget;
}

async function assertExistingComponents(realRoot, root, target) {
  const rel = relative(root, target);
  let current = root;
  for (const component of rel ? rel.split(requireSeparator()) : []) {
    current = resolve(current, component);
    try {
      const stat = await lstat(current);
      if (stat.isSymbolicLink()) {
        throw new Error(`Refusing symlinked write component: ${current}`);
      }
      const realCurrent = await realpath(current);
      assertContained(realRoot, realCurrent);
    } catch (error) {
      if (isMissingPath(error)) break;
      throw error;
    }
  }
}

function assertContained(root, target) {
  const rel = relative(root, target);
  if (isAbsolute(rel) || rel === '..' || rel.startsWith(`..${requireSeparator()}`)) {
    throw new Error(`Path escapes root: ${target}`);
  }
}

function isMissingPath(error) {
  return typeof error === 'object' && error !== null && 'code' in error && error.code === 'ENOENT';
}

function requireSeparator() {
  return process.platform === 'win32' ? '\\' : '/';
}
