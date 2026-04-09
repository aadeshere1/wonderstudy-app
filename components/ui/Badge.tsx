import { ReactNode } from "react";

export interface BadgeProps {
  children: ReactNode;
  variant?: "success" | "warning" | "error" | "info" | "new";
  className?: string;
}

export const Badge = ({
  children,
  variant = "info",
  className = "",
}: BadgeProps) => {
  const variantStyles = {
    success:
      "inline-block px-3 py-1 rounded-full text-xs font-black bg-mint/20 text-mint",
    warning:
      "inline-block px-3 py-1 rounded-full text-xs font-black bg-gold/20 text-gold",
    error:
      "inline-block px-3 py-1 rounded-full text-xs font-black bg-coral/20 text-coral",
    info: "inline-block px-3 py-1 rounded-full text-xs font-black bg-blue/20 text-blue",
    new: "inline-block px-2 py-0.5 rounded-full text-xs font-black bg-coral text-white",
  };

  return (
    <span className={`${variantStyles[variant]} ${className}`}>{children}</span>
  );
};
