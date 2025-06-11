// src/app/layout.tsx

import './globals.css';
import Link from 'next/link';

export const metadata = {
  title: 'Financial Report QA',
  description: 'Hybrid RAG System for Financial Documents',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav style={styles.navbar}>
          <Link href="/" style={styles.navLink}>Chat</Link>
          <Link href="/upload" style={styles.navLink}>Upload</Link>
          <Link href="/insights" style={styles.navLink}>Insights</Link>
        </nav>

        <main style={styles.main}>
          {children}
        </main>
      </body>
    </html>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  navbar: {
    display: 'flex',
    justifyContent: 'flex-start',
    alignItems: 'center',
    padding: '1rem 2rem',
    backgroundColor: '#f9f9f9',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
    position: 'sticky',   // STICKY at top
    top: 0,
    zIndex: 100,
    gap: '2rem',
    fontSize: '1.1rem',
  },
  navLink: {
    color: '#333',
    textDecoration: 'none',
    fontWeight: 'bold',
  },
  main: {
    padding: '2rem',
  },
};