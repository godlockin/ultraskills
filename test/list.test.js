import { test } from 'node:test';
import assert from 'node:assert/strict';
import { listSkills } from '../lib/list.js';

const skills = [
  { id: 'code-review', name: 'Code Review', description: 'Review PRs', source_dir: 'community', tags: ['engineering'], arena: { score: 9.0, category: 'eng-code', is_winner: true } },
  { id: 'page-cro', name: 'Page CRO', description: 'Landing page optimization', source_dir: 'community', tags: ['marketing'], arena: { score: 7.0, category: 'cro-landing', is_winner: false } },
  { id: 'seo-audit', name: 'SEO Audit', description: 'SEO review', source_dir: 'community', tags: ['marketing', 'seo'], arena: { score: 6.5, category: 'seo-technical', is_winner: true } },
];

test('list all — no category — prints all skills', () => {
  let output = '';
  const orig = console.log;
  console.log = (...args) => { output += args.join(' ') + '\n'; };
  listSkills('', skills);
  console.log = orig;
  assert.ok(output.includes('code-review'));
  assert.ok(output.includes('page-cro'));
  assert.ok(output.includes('seo-audit'));
});

test('category filter — returns matching only', () => {
  let output = '';
  const orig = console.log;
  console.log = (...args) => { output += args.join(' ') + '\n'; };
  listSkills('cro', skills);
  console.log = orig;
  assert.ok(output.includes('page-cro'));
  assert.ok(!output.includes('seo-audit'));
});

test('sorted by score desc', () => {
  const lines = [];
  const orig = console.log;
  console.log = (...args) => { lines.push(args.join(' ')); };
  listSkills('', skills);
  console.log = orig;
  const dataLines = lines.filter(l => l.includes('code-review') || l.includes('page-cro') || l.includes('seo-audit'));
  const codeReviewIdx = dataLines.findIndex(l => l.includes('code-review'));
  const pageIdx = dataLines.findIndex(l => l.includes('page-cro'));
  assert.ok(codeReviewIdx < pageIdx); // code-review (9.0) before page-cro (7.0)
});

test('winner marked with ★', () => {
  let output = '';
  const orig = console.log;
  console.log = (...args) => { output += args.join(' ') + '\n'; };
  listSkills('', skills);
  console.log = orig;
  const reviewLine = output.split('\n').find(l => l.includes('code-review'));
  assert.ok(reviewLine?.includes('★'));
});

test('empty index — prints no skills message', () => {
  let output = '';
  const orig = console.log;
  console.log = (...args) => { output += args.join(' ') + '\n'; };
  listSkills('', []);
  console.log = orig;
  assert.ok(output.includes('No skills'));
});
