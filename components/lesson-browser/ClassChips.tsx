import { Chip } from '@/components/ui';

export interface ClassChipsProps {
  selectedClass: number | null;
  onSelect: (classNum: number) => void;
  maxClass?: number;
}

export const ClassChips = ({
  selectedClass,
  onSelect,
  maxClass = 10,
}: ClassChipsProps) => {
  const classes = Array.from({ length: maxClass }, (_, i) => i + 1);

  return (
    <div className="flex flex-wrap gap-2 justify-center">
      {classes.map((num) => (
        <Chip
          key={num}
          active={selectedClass === num}
          onClick={() => onSelect(num)}
        >
          {num}
        </Chip>
      ))}
    </div>
  );
};
