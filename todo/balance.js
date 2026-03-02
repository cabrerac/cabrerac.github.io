/**
 * Balance algorithm: from full task list, produce "Today's plan" (ordered subset).
 * Rules: deadline soon first; cap admin; ensure min research & studying; fill by score + diversity.
 *
 * Usage:
 *   const { today, all } = balance(data, { maxTotal: 8, daysAhead: 7 });
 */

const URGENCY_SCORE = { immediate: 3, soon: 2, flexible: 1 };
const REWARD_SCORE = { high: 3, medium: 2, low: 1 };
const DEFAULT_MAX_TOTAL = 8;
const DEFAULT_DAYS_AHEAD = 7;
const MAX_ADMIN = 2;
const MIN_RESEARCH = 1;
const MIN_STUDYING = 1;

function parseDate(s) {
  if (!s) return null;
  const d = new Date(s);
  return isNaN(d.getTime()) ? null : d;
}

function daysFromToday(date, today) {
  if (!date) return null;
  const t = today ? new Date(today) : new Date();
  t.setHours(0, 0, 0, 0);
  const d = new Date(date);
  d.setHours(0, 0, 0, 0);
  return Math.floor((d - t) / (24 * 60 * 60 * 1000));
}

function taskScore(task) {
  const u = (task.urgency && URGENCY_SCORE[task.urgency]) || 1;
  const r = (task.reward && REWARD_SCORE[task.reward]) || 1;
  return u + r;
}

function getEarliestDeadline(task, venues) {
  const taskDay = parseDate(task.deadline);
  let venueDay = null;
  if (Array.isArray(task.venues) && Array.isArray(venues)) {
    for (const vid of task.venues) {
      const v = venues.find((x) => x.id === vid);
      if (v && v.deadline) {
        const d = parseDate(v.deadline);
        if (d && (!venueDay || d < venueDay)) venueDay = d;
      }
      if (v && v.deadlines && v.deadlines.length) {
        for (const dStr of v.deadlines) {
          const d = parseDate(dStr);
          if (d && (!venueDay || d < venueDay)) venueDay = d;
        }
      }
    }
  }
  if (taskDay && venueDay) return taskDay < venueDay ? taskDay : venueDay;
  return taskDay || venueDay;
}

/**
 * @param {{ tasks: any[], venues?: any[] }} data - Parsed tasks.yaml content (tasks + venues)
 * @param {{ maxTotal?: number, daysAhead?: number, today?: string }} options
 * @returns {{ today: any[], all: any[] }}
 */
function balance(data, options = {}) {
  const maxTotal = options.maxTotal ?? DEFAULT_MAX_TOTAL;
  const daysAhead = options.daysAhead ?? DEFAULT_DAYS_AHEAD;
  const todayStr = options.today || new Date().toISOString().slice(0, 10);
  const tasks = Array.isArray(data.tasks) ? data.tasks : [];
  const venues = Array.isArray(data.venues) ? data.venues : [];

  // 1) Deadline in next N days: sort by deadline, take all (up to maxTotal)
  const deadlineTasks = [];
  const rest = [];
  for (const t of tasks) {
    const ed = getEarliestDeadline(t, venues);
    const days = ed ? daysFromToday(ed, todayStr) : null;
    if (days != null && days >= 0 && days <= daysAhead) {
      deadlineTasks.push({ task: t, days, date: ed });
    } else {
      rest.push(t);
    }
  }
  deadlineTasks.sort((a, b) => a.days - b.days);
  const picked = deadlineTasks.map((x) => x.task);
  const pickedIds = new Set(picked.map((t) => t.id || t.title));
  let adminCount = picked.filter((t) => t.category === 'admin').length;

  // 2) Ensure min 1 research, 1 studying (if any exist)
  const hasResearch = picked.some((t) => t.category === 'research');
  const hasStudying = picked.some((t) => t.category === 'studying');
  const researchCandidates = rest.filter((t) => t.category === 'research' && !pickedIds.has(t.id || t.title));
  const studyingCandidates = rest.filter((t) => t.category === 'studying' && !pickedIds.has(t.id || t.title));
  if (!hasResearch && researchCandidates.length) {
    researchCandidates.sort((a, b) => taskScore(b) - taskScore(a));
    const add = researchCandidates[0];
    picked.push(add);
    pickedIds.add(add.id || add.title);
    rest.splice(rest.indexOf(add), 1);
  }
  if (!hasStudying && studyingCandidates.length) {
    studyingCandidates.sort((a, b) => taskScore(b) - taskScore(a));
    const add = studyingCandidates[0];
    picked.push(add);
    pickedIds.add(add.id || add.title);
    rest.splice(rest.indexOf(add), 1);
  }

  // 3) Fill remaining by score; cap admin at MAX_ADMIN; prefer diversity
  const remaining = rest.filter((t) => !pickedIds.has(t.id || t.title));
  remaining.sort((a, b) => taskScore(b) - taskScore(a));

  for (const t of remaining) {
    if (picked.length >= maxTotal) break;
    if (t.category === 'admin' && adminCount >= MAX_ADMIN) continue;
    picked.push(t);
    pickedIds.add(t.id || t.title);
    if (t.category === 'admin') adminCount++;
  }

  return { today: picked, all: tasks };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { balance };
}
if (typeof self !== 'undefined') {
  self.TODO_balance = { balance };
}

