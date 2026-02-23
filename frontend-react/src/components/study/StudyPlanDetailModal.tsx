import type { StudyPlan } from '../../types/index';

interface Props {
  plan: StudyPlan;
  onClose: () => void;
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mb-6">
      <h4 className="text-sm font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400 mb-2">{title}</h4>
      {children}
    </div>
  );
}

function BulletList({ items, emptyMsg }: { items?: string[]; emptyMsg: string }) {
  if (!items || items.length === 0)
    return <p className="text-sm text-gray-400 dark:text-gray-500 italic">{emptyMsg}</p>;
  return (
    <ul className="space-y-1">
      {items.map((item, i) => (
        <li key={i} className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-300">
          <span className="mt-1 shrink-0 w-1.5 h-1.5 rounded-full bg-blue-400 dark:bg-blue-500" />
          {item}
        </li>
      ))}
    </ul>
  );
}

export default function StudyPlanDetailModal({ plan, onClose }: Props) {
  const m = plan.study_materials;
  const s = plan.schedule;
  const ms = plan.milestones;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" onClick={onClose}>
      <div
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col"
        onClick={e => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start justify-between gap-4 p-6 border-b border-gray-100 dark:border-gray-700">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wide text-blue-600 dark:text-blue-400">{plan.subject}</span>
            <h2 className="text-xl font-bold text-gray-800 dark:text-white mt-0.5">{plan.title}</h2>
            {plan.description && (
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{plan.description}</p>
            )}
            <div className="flex items-center gap-3 mt-2 text-xs text-gray-500 dark:text-gray-400">
              <span className={`px-2 py-0.5 rounded-full font-medium ${
                plan.difficulty_level === 'beginner' ? 'bg-green-100 text-green-700' :
                plan.difficulty_level === 'advanced' ? 'bg-red-100 text-red-700' :
                'bg-yellow-100 text-yellow-700'
              }`}>{plan.difficulty_level}</span>
              <span>📅 {new Date(plan.created_at).toLocaleDateString()}</span>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-2xl leading-none shrink-0"
            aria-label="Close"
          >
            ×
          </button>
        </div>

        {/* Scrollable body */}
        <div className="overflow-y-auto p-6 space-y-0">

          {/* Subjects to Study */}
          <Section title="📚 Subjects to Study">
            <BulletList items={m?.subjects} emptyMsg="No subjects recorded." />
          </Section>

          {/* Skills to Develop */}
          <Section title="🛠 Skills to Develop">
            <BulletList items={m?.skills} emptyMsg="No skills recorded." />
          </Section>

          {/* Resources */}
          {m?.resources && m.resources.length > 0 && (
            <Section title="🔗 Recommended Resources">
              <div className="flex flex-wrap gap-2">
                {m.resources.map((r, i) => (
                  <span key={i} className="text-sm px-3 py-1 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full">
                    {r}
                  </span>
                ))}
              </div>
            </Section>
          )}

          {/* Milestones */}
          {(ms?.short_term?.length || ms?.medium_term?.length || ms?.long_term?.length) ? (
            <Section title="🎯 Milestones">
              <div className="space-y-4">
                {ms?.short_term && ms.short_term.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold text-green-600 dark:text-green-400 mb-1">Short-term (0–6 months)</p>
                    <BulletList items={ms.short_term} emptyMsg="" />
                  </div>
                )}
                {ms?.medium_term && ms.medium_term.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold text-yellow-600 dark:text-yellow-400 mb-1">Medium-term (6–18 months)</p>
                    <BulletList items={ms.medium_term} emptyMsg="" />
                  </div>
                )}
                {ms?.long_term && ms.long_term.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold text-red-600 dark:text-red-400 mb-1">Long-term (18+ months)</p>
                    <BulletList items={ms.long_term} emptyMsg="" />
                  </div>
                )}
              </div>
            </Section>
          ) : (
            <Section title="🎯 Milestones">
              <p className="text-sm text-gray-400 italic">No milestones recorded.</p>
            </Section>
          )}

          {/* Weekly Tasks */}
          {s?.weekly_tasks && s.weekly_tasks.length > 0 && (
            <Section title="📆 Weekly Learning Tasks">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-xs text-gray-500 dark:text-gray-400 border-b border-gray-100 dark:border-gray-700">
                      <th className="pb-2 pr-4 font-semibold">Task</th>
                      <th className="pb-2 pr-4 font-semibold">Duration</th>
                      <th className="pb-2 font-semibold">Priority</th>
                    </tr>
                  </thead>
                  <tbody>
                    {s.weekly_tasks.map((t, i) => (
                      <tr key={i} className="border-b border-gray-50 dark:border-gray-700/50">
                        <td className="py-2 pr-4 text-gray-700 dark:text-gray-300">{t.task}</td>
                        <td className="py-2 pr-4 text-gray-500 dark:text-gray-400">{t.duration}</td>
                        <td className="py-2">
                          <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                            t.priority === 'high' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300'
                          }`}>{t.priority}</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Section>
          )}

          {/* Daily Activities */}
          {s?.daily_activities && s.daily_activities.length > 0 && (
            <Section title="🌅 Suggested Daily Activities">
              <ul className="space-y-2">
                {s.daily_activities.map((a, i) => (
                  <li key={i} className="flex items-center justify-between text-sm bg-gray-50 dark:bg-gray-700/50 rounded-lg px-3 py-2">
                    <span className="text-gray-700 dark:text-gray-300">{a.activity}</span>
                    <span className="text-xs text-gray-500 dark:text-gray-400 shrink-0 ml-2">{a.duration} min</span>
                  </li>
                ))}
              </ul>
            </Section>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-100 dark:border-gray-700 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
