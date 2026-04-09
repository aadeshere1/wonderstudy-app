import { ReactNode } from "react";

export interface TagProps {
  children: ReactNode;
  color?: "purple" | "gold" | "coral" | "mint";
  className?: string;
}

export const Tag = ({
  children,
  color = "purple",
  className = "",
}: TagProps) => {
  const colorStyles = {
    purple: "bg-purple/20 text-purple",
    gold: "bg-gold/20 text-gold",
    coral: "bg-coral/20 text-coral",
    mint: "bg-mint/20 text-mint",
  };

  return (
    <span
      className={`inline-block px-3 py-1 rounded-full text-xs font-black text-uppercase tracking-wider ${colorStyles[color]} ${className}`}
    >
      {children}
    </span>
  );
};
