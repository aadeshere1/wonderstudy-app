"use client";

import Link from "next/link";
import { AuthButton } from "@/components/auth/AuthButton";
import { useTheme } from "@/contexts/ThemeContext";
import XPBar from "@/components/gamification/XPBar";

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
  const { theme, toggle } = useTheme();

  return (
    <nav
      className="sticky top-0 z-40 backdrop-blur-2xl px-5 py-3 flex items-center justify-between"
      style={{
        background: 'var(--ws-nav-bg)',
        borderBottom: '1px solid var(--ws-nav-border)',
      }}
    >
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
                  : "bg-transparent hover:text-purple"
              }`}
              style={{ color: activeTab === tab.id ? undefined : 'var(--ws-text-muted)' }}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </div>
      )}

      {/* Right side: XP + Theme toggle + Settings + Auth */}
      <div className="flex items-center gap-2">
        <XPBar />
        {/* Theme toggle */}
        <button
          onClick={toggle}
          title={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
          style={{
            width: 36,
            height: 36,
            borderRadius: 10,
            border: '1px solid var(--ws-border)',
            background: 'var(--ws-card2)',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.1rem',
            transition: 'all 0.2s',
            flexShrink: 0,
          }}
        >
          {theme === 'light' ? '🌙' : '☀️'}
        </button>

        {showSettings && (
          <button
            onClick={onSettingsClick}
            style={{
              width: 36,
              height: 36,
              borderRadius: 10,
              border: '1px solid var(--ws-border)',
              background: 'var(--ws-card2)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1rem',
              transition: 'all 0.2s',
            }}
            title="Settings"
          >
            ⚙️
          </button>
        )}
        <AuthButton />
      </div>
    </nav>
  );
};
