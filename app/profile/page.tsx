'use client';

import dynamic from 'next/dynamic';

// Client-only since it reads Firebase/localStorage
const ProfileClient = dynamic(() => import('./ProfileClient'), { ssr: false });

export default function ProfilePage() {
  return <ProfileClient />;
}
