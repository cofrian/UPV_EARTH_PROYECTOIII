import "./globals.css";
import type { Metadata } from "next";

import { Nav } from "@/components/Nav";

export const metadata: Metadata = {
  title: "UPV-EARTH",
  description: "Plataforma de analitica de Planetary Boundaries",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <Nav />
        <main className="mx-auto max-w-7xl px-5 py-8">{children}</main>
      </body>
    </html>
  );
}
