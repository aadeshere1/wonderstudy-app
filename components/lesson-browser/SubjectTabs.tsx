export interface SubjectTabsProps {
  selectedSubject: string | null;
  onSelect: (subject: string) => void;
  subjects?: Array<{ id: string; name: string; icon: string }>;
}

const DEFAULT_SUBJECTS = [
  { id: 'math', name: 'Math', icon: '🔢' },
  { id: 'english', name: 'English', icon: '📚' },
  { id: 'science', name: 'Science', icon: '🔬' },
];

export const SubjectTabs = ({
  selectedSubject,
  onSelect,
  subjects = DEFAULT_SUBJECTS,
}: SubjectTabsProps) => {
  return (
    <div className="flex gap-2 flex-wrap">
      {subjects.map((subject) => (
        <button
          key={subject.id}
          type="button"
          onClick={() => onSelect(subject.id)}
          className={`px-5 py-2.5 rounded-3xl font-black text-sm border-2 transition-all duration-200 cursor-pointer ${
            selectedSubject === subject.id
              ? 'bg-gradient-to-r from-mint to-cyan-600 border-mint text-black scale-105 shadow-correct'
              : 'bg-card2 border-white/10 text-white hover:border-mint hover:scale-105'
          }`}
        >
          <span className="mr-1.5">{subject.icon}</span>
          {subject.name}
        </button>
      ))}
    </div>
  );
};
