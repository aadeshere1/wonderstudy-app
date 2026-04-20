/** UIDs / emails that are allowed to access the admin dashboard */
export const ADMIN_EMAILS: string[] = [
  'aadeshere1@gmail.com',
];

export function isAdmin(email: string | null | undefined): boolean {
  if (!email) return false;
  return ADMIN_EMAILS.includes(email.toLowerCase());
}
