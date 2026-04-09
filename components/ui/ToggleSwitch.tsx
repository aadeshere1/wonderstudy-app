"use client";

import { useState, useEffect } from "react";

export interface ToggleSwitchProps {
  checked?: boolean;
  onChange?: (checked: boolean) => void;
  className?: string;
  disabled?: boolean;
}

export const ToggleSwitch = ({
  checked = false,
  onChange,
  className = "",
  disabled = false,
}: ToggleSwitchProps) => {
  const [isChecked, setIsChecked] = useState(checked);

  useEffect(() => {
    setIsChecked(checked);
  }, [checked]);

  const handleToggle = () => {
    if (disabled) return;
    const newState = !isChecked;
    setIsChecked(newState);
    onChange?.(newState);
  };

  return (
    <button
      type="button"
      onClick={handleToggle}
      disabled={disabled}
      className={`relative w-12 h-7 rounded-full transition-all duration-300 flex-shrink-0 ${
        isChecked ? "bg-purple" : "bg-card2"
      } ${disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"} ${className}`}
      aria-pressed={isChecked}
    >
      {/* Slider dot */}
      <div
        className={`absolute top-1 left-1 w-5 h-5 bg-white rounded-full transition-transform duration-300 ${
          isChecked ? "translate-x-5" : "translate-x-0"
        }`}
      />
    </button>
  );
};
