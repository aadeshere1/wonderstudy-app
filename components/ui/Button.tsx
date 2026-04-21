import { ReactNode } from "react";

export interface ButtonProps {
  children: ReactNode;
  onClick?: () => void;
  className?: string;
  variant?: "primary" | "secondary" | "gold" | "ghost";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  type?: "button" | "submit" | "reset";
}

export const Button = ({
  children,
  onClick,
  className = "",
  variant = "primary",
  size = "md",
  disabled = false,
  type = "button",
}: ButtonProps) => {
  const baseStyles =
    "inline-flex items-center justify-center gap-2 rounded-lg border-none cursor-pointer font-body font-bold transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed";

  const sizeStyles = {
    sm: "px-3 py-2 text-sm",
    md: "px-5 py-3 text-base",
    lg: "px-6 py-4 text-lg",
  };

  const variantStyles = {
    primary:
      "bg-gradient-to-r from-purple to-coral text-white shadow-glow hover:shadow-lg hover:scale-105 disabled:hover:scale-100",
    secondary:
      "bg-card2 text-theme border border-border hover:border-purple hover:text-purple disabled:hover:text-theme disabled:hover:border-border",
    gold: "bg-gradient-to-r from-gold to-orange-400 text-black font-black hover:shadow-lg hover:scale-105 disabled:hover:scale-100",
    ghost: "bg-transparent text-theme hover:bg-black/5 dark:hover:bg-white/10 disabled:hover:bg-transparent",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}
    >
      {children}
    </button>
  );
};
