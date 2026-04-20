"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/papers", label: "Explorar" },
  { href: "/upload", label: "Nuevo PDF" },
];

export function Nav() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-10 border-b border-line bg-bg/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
        <div>
          <h1 className="text-xl font-semibold">UPV-EARTH</h1>
          <p className="muted text-sm">Planetary Boundaries Analytics Platform</p>
        </div>
        <nav className="flex gap-2">
          {links.map((item) => {
            const active = pathname.startsWith(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`rounded-md px-3 py-2 text-sm transition ${
                  active ? "bg-accent text-black" : "bg-panelSoft text-textMain hover:bg-accentSoft"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
