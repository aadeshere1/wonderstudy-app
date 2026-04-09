import { ReactNode } from "react";

export interface CardProps {
  children: ReactNode;
  className?: string;
  variant?: "default" | "dark" | "interactive";
  onClick?: () => void;
}

export const Card = ({
  children,
  className = "",
  variant = "default",
  onClick,
}: CardProps) => {
  const baseStyles = "rounded-2xl border border-white/7 transition-all duration-200";

  const variantStyles = {
    default: "bg-card p-5",
    dark: "bg-card2 p-5",
    interactive:
      "bg-card p-5 cursor-pointer hover:border-purple hover:shadow-glow hover:-translate-y-0.5 active:translate-y-0",
  };

  return (
    <div
      className={`${baseStyles} ${variantStyles[variant]} ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
};
