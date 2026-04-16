import { test } from 'node:test';
import assert from 'node:assert/strict';
import { resolveSkill, searchSkills } from '../lib/search.js';

const skills = [
  { id: 'code-review', name: 'Code Review', description: 'Review pull requests for quality', tags: ['engineering'], arena: { score: 9.0 } },
  { id: 'code-quality', name: 'Code Quality', description: 'Static analysis and linting', tags: ['engineering'], arena: { score: 8.5 } },
  { id: 'page-cro', name: 'Page CRO', description: 'Optimize landing pages for conversion', tags: ['marketing'], arena: { score: 7.0 } },
  { id: 'seo-audit', name: 'SEO Audit', description: 'Technical SEO review and fixes', tags: ['marketing', 'seo'], arena: { score: 6.5 } },
  { id: 'video-editing', name: 'Video Editing', description: 'Cut and export video content', tags: ['video'], arena: { score: 8.0 } },
];

test('exact id match — returns that skill only', () => {
  const r = resolveSkill('code-review', skills);
  assert.equal(r.length, 1);
  assert.equal(r[0].id, 'code-review');
});

test('exact match is case-insensitive', () => {
  const r = resolveSkill('CODE-REVIEW', skills);
  assert.equal(r.length, 1);
  assert.equal(r[0].id, 'code-review');
});

test('id prefix match — sorted by score desc', () => {
  const r = resolveSkill('code', skills);
  assert.equal(r[0].id, 'code-review'); // score 9.0
  assert.equal(r[1].id, 'code-quality'); // score 8.5
});

test('description substring match', () => {
  const r = resolveSkill('landing page', skills);
  assert.equal(r[0].id, 'page-cro');
});

test('tag match', () => {
  const r = resolveSkill('seo', skills);
  assert.ok(r.some(s => s.id === 'seo-audit'));
});

test('no match returns empty array', () => {
  const r = resolveSkill('xyznonexistent', skills);
  assert.equal(r.length, 0);
});

test('returns max 5 results', () => {
  const many = Array.from({ length: 10 }, (_, i) => ({
    id: `skill-${i}`, name: `Skill ${i}`, description: 'common word test', tags: [], arena: { score: i }
  }));
  const r = resolveSkill('common', many);
  assert.ok(r.length <= 5);
});

test('searchSkills — returns across all fields top-10', () => {
  const r = searchSkills('review', skills);
  assert.ok(r.some(s => s.id === 'code-review'));
  assert.ok(r.some(s => s.id === 'seo-audit')); // description contains "review"
});

test('searchSkills — sorted by score', () => {
  const r = searchSkills('review', skills);
  for (let i = 1; i < r.length; i++) {
    assert.ok((r[i-1].arena?.score ?? 0) >= (r[i].arena?.score ?? 0));
  }
});
