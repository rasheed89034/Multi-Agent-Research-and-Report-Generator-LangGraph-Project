import type { Metadata } from "next";
import { Schibsted_Grotesk } from "next/font/google";
import Link from "next/link";
import { FlaskConical, History, Plus } from "lucide-react";
import "./globals.css";

const font = Schibsted_Grotesk({ subsets: ["latin"], variable: "--font-body" });
export const metadata: Metadata = { title: "Research Desk", description: "Multi-agent research and report generator" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={font.variable}>
      <body className="min-h-screen md:flex">
        <nav className="glass m-3 flex gap-2 p-3 md:w-56 md:flex-col md:self-start md:sticky md:top-3">
          <Link href="/" className="mb-2 flex items-center gap-2 px-2 font-semibold"><FlaskConical className="text-indigo-400" size={20} />Research Desk</Link>
          <Link href="/" className="flex items-center gap-2 rounded-lg px-2 py-2 text-sm hover:bg-white/5"><Plus size={16} />New research</Link>
          <Link href="/history" className="flex items-center gap-2 rounded-lg px-2 py-2 text-sm hover:bg-white/5"><History size={16} />History</Link>
        </nav>
        <main className="flex-1 p-3 md:p-6">{children}</main>
      </body>
    </html>
  );
}
