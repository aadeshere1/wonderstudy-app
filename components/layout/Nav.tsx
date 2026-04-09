"use client";

import Link from "next/link";
import { useState } from "react";

export interface NavTab {
  id: string;
  label: string;
  icon?: string;
  href?: string;
  onClick?: () => void;
}

export interface NavProps {
  title: string;
  tabs?: NavTab[];
  activeTab?: string;
  onTabChange?: (tabId: string) => void;
  showSettings?: boolean;
  onSettingsClick?: () => void;
}

export const Nav = ({
  title,
  tabs = [],
  activeTab,
  onTabChange,
  showSettings = false,
  onSettingsClick,
}: NavProps) => {
  return (
    <nav className="sticky top-0 z-40 bg-bg/90 backdrop-blur-2xl border-b border-white/7 px-5 py-3 flex items-center justify-between">
      {/* Title */}
      <Link href="/" className="font-display text-2xl bg-gradient-to-r from-gold to-coral bg-clip-text text-transparent font-bold hover:opacity-80 transition">
        ⭐ {title}
      </Link>

      {/* Tabs */}
      {tabs.length > 0 && (
        <div className="flex gap-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => {
                onTabChange?.(tab.id);
                tab.onClick?.();
              }}
              className={`px-3.5 py-1.5 rounded-xl border-none cursor-pointer font-body font-black text-xs transition-all duration-200 ${
                activeTab === tab.id
                  ? "bg-purple/20 text-purple"
                  : "bg-transparent text-muted hover:text-white"
              }`}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </div>
      )}

      {/* Settings Button */}
      {showSettings && (
        <button
          onClick={onSettingsClick}
          className="px-3 py-2 rounded-lg bg-card2 hover:bg-card hover:border-purple border border-white/10 text-white transition-all cursor-pointer"
          title="Settings"
        >
          ⚙️
        </button>
      )}
    </nav>
  );
};
