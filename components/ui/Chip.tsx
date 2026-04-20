import { ReactNode } from "react";

export interface ChipProps {
  children: ReactNode;
  onClick?: () => void;
  active?: boolean;
  variant?: "default" | "pill";
  className?: string;
  disabled?: boolean;
}

export const Chip = ({
  children,
  onClick,
  active = false,
  variant = "default",
  className = "",
  disabled = false,
}: ChipProps) => {
  const baseStyles =
    "cursor-pointer font-body font-bold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed";

  const variantStyles = {
    default: active
      ? "w-11 h-11 rounded-2xl bg-gradient-to-br from-mint to-cyan-600 border-2 border-mint text-white shadow-correct scale-110"
      : "w-11 h-11 rounded-2xl border-2 bg-card2 text-theme hover:border-mint hover:scale-110",
    pill: active
      ? "px-5 py-2 rounded-full bg-gradient-to-r from-gold to-orange-400 border-2 border-gold text-black"
      : "px-5 py-2 rounded-full border-2 bg-card2 text-theme hover:border-purple",
  };

  // Use inline style for border color so it responds to CSS theme vars
  const borderStyle = !active ? { borderColor: 'var(--ws-border)' } : undefined;

  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      style={borderStyle}
      className={`${baseStyles} ${variantStyles[variant]} ${className} flex items-center justify-center`}
    >
      {children}
    </button>
  );
};
